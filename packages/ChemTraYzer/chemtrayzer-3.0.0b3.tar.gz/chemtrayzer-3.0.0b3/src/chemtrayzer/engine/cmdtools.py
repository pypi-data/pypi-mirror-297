'''
Contains classes/functions used with the command line interface of this package.
'''
from __future__ import annotations

import argparse
from collections.abc import Iterable
import dataclasses
import importlib
import logging
import os
import shutil
import sys
import traceback
import typing
from typing import Literal
import warnings
from abc import ABC, abstractmethod
from argparse import ArgumentError, ArgumentParser, Namespace
from datetime import timedelta
from pathlib import Path
from time import sleep
from types import ModuleType, UnionType
from typing import (
    ContextManager,
    Generic,
    Mapping,
    TypeVar,
    Union,
    get_origin,
)

import numpy as np
from numpy.typing import ArrayLike

if sys.version_info[:2] < (3, 11):
    import tomli as tomllib
else:
    import tomllib  # added in 3.11

from chemtrayzer.engine.errors import ProgrammingError
from chemtrayzer.engine.investigation import (
    Investigation,
    InvestigationContext,
)
from chemtrayzer.engine.jobsystem import BlockingJobSystem, JobSystem, SlurmJobSystem, PythonScriptJob

T = TypeVar('T', bound=Investigation)
'''investigation type'''
ConfigT = TypeVar('ConfigT', ModuleType, dict)
'''type of the configuration that is passed to create_investigation(), etc.'''

class UserError(Exception):
    '''base exception meant to be used, when the user can fix the error

    Inherit from this class to indicate that the exception should be considered
    a message to the user and not, e.g., a programming error/bug. The message
    should be a bit more verbose and aimed at the user.'''

class IllegalCmdArgsError(UserError):
    '''raised when the check of the command line arguments fails.'''

class IllegalConfigError(UserError):
    '''raised when the config file is not valid'''

class ConfigLoaderError(UserError):
    '''raised when the config file could not be loaded'''

class WorkspaceNotEmptyError(UserError):
    '''raised when the workspace is not empty, but does not contain an
    investigation file either'''

class _ConfigLoader(ABC):
    """Functionality to load configuration file
    """

    @abstractmethod
    def load(self) -> tuple[ConfigT, str]:
        """method to load the configuration (which may be empty, e.g. if no path
        is supplied)

        :raise: ConfigLoaderError if the config file could not be loaded
        :return: (config, python_exec) where config contains the content file and python_exec is a string containing the python executable to restart the investigation or None if it is not supplied"""

class _PythonConfigLoader(_ConfigLoader):
    """Loader for python configuration files

    :param path: Path to python file. If None, an empty module is returned by
                 load()"""

    def __init__(self, path: str|None) -> None:
        super().__init__()
        self.path = path

    def load(self) -> tuple[ModuleType, str]:
        if self.path is None:
            return ModuleType('__empty__', doc='No config file supplied'), None

        spec = importlib.util.spec_from_file_location('config', self.path)
        if spec is None:
            raise ConfigLoaderError(f'Could not import *.py config file "'
                                    f'{self.path}"')
        try:
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
        except ConfigLoaderError as err:
            raise ValueError(f'Could not import *.py config file '
                             f'"{self.path}"') from err

        if hasattr(config_module, 'python_exec'):
            python_exec = config_module.python_exec
            logging.debug('Using python_exec from config file for restarting '
                         'investigations: %s', python_exec)
        else:
            python_exec = None
            logging.debug('Could not find python_exec in config file.')

        return config_module, python_exec

class _TomlConfigLoader(_ConfigLoader):
    """Loader for toml configuration files

    :param path: Path to toml file. If None, an empty module is returned by
                 load()
    """

    def __init__(self, path: str|None) -> None:
        super().__init__()
        self.path = path

    def load(self) -> tuple[dict, str]:
        if self.path is None:
            return dict(), None

        try:
            with open(self.path, 'rb') as fp:
                config = tomllib.load(fp)
        except FileNotFoundError as err:
            raise ConfigLoaderError(f'Could not find config file "{self.path}"')\
                    from err
        except tomllib.TOMLDecodeError as err:
            raise ConfigLoaderError('Error reading toml file: '
                                    f'"{self.path}": {err}')\
                    from err

        python_exec = config['python_exec'] if 'python_exec' in config else None

        return config, python_exec

class CommandLineInterface(Generic[T], ABC):
    '''
    Helper class to create a command line interface that starts a main investigation.
    This class defines what the "main" investigation looks like. It is used by
    the main.py script.

    It is supposed to be run in a directory called workspace where it first
    checks if there are already investigations in this workspace. If not, a new
    main investigation is created and submitted. If there are already
    investigations in this workspace, the jobsystem is checked for new jobs.

    :param script: script to execute when all jobs are done in the "restart
                   strategy"
    :param debug_mode: if True, an uncaught exception in an investigation will
                       not be caught (which would lead to the investigation
                       failing, but other, dependent investigations would be
                       executed). If False, investigations will fail with an
                       ErrorCausedFailure and other exceptions occuring outside
                       of investigaitons will be caught and lead to a programm
                       exit with nonzero exit code.
    :param add_restart_argv: arguments that should be passed to the script (in
                             addition to the current arguvemnts)
                             when it is restarted.
    :param arg_parser: Argument parser that should be used. By
                       default, one is created.
    '''
    INVESTIGATIONS_FILE = 'investigations.pickle'
    '''name of the file that is created in the workspace which contains
    the serialized investigations'''
    JOB_DIR = 'jobs'
    '''subdirectory of workspace containing all jobs submitted by the
    investigations'''
    DESCRIPTION = ''
    '''Text shown before the help texts of the arguments & options'''
    SLEEP_TIMER = 3
    '''time in seconds to wait between checking if new jobs are finished'''
    CONFIG_TYPE = 'python'
    '''Format of the config file. Allowed values are "python"  and "toml"'''

    POSITIONAL_ARGUMENTS = []
    '''deprecated. list of positional arguments and their description for the help text'''

    LOG_LEVELS = {
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }

    def __init__(self, script: Union[os.PathLike, str],
                 debug_mode: bool = False,
                 add_restart_argv: list[str] = None,
                 arg_parser: ArgumentParser = None) -> None:
        super().__init__()

        self.script = script
        self.__fail_deadly = debug_mode
        self.__exit_gracefully = not debug_mode
        # used for raising error in start():
        self.__init_called = True

        self.add_restart_argv = add_restart_argv

        if arg_parser is None:
            arg_parser = ArgumentParser(description=self.DESCRIPTION)
        else:
            arg_parser.description = self.DESCRIPTION

        self.__parser = arg_parser
        self.__add_args()

    def get_context_managers(self, config: ConfigT,
                             cmd_args: argparse.Namespace)\
                                -> Mapping[str, ContextManager]:
        '''can be overridden to supply context managers for the investigation

        .. note::

            This method will be called on every execution of the program, thus,
            it may be called multiple times, if the program is resumed after
            waiting for a job to finish. The contents of the config file and the
            command line arguments may change between calls, if the user passes
            different arguments or changes the config file.

        :param config: Contents of the loaded configuration file. If the config
                        file is a python file, this is the module object. If the
                        config file is a TOML file, this is a dictionary.
        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        '''
        return {}

    def _create_slurm_jobsystem(self, job_dir: os.PathLike,
                            account: str, sbatch_cmd: str) -> SlurmJobSystem:
        return SlurmJobSystem(dir=job_dir,
                         account=account,
                         sbatch_cmd=sbatch_cmd)

    def _create_blocking_jobsystem(self, job_dir: os.PathLike)\
            -> BlockingJobSystem:
        logging.info('With the blocking job system jobs will be run directly as'
                     ' subprocesses. This means that the program '
                     'will wait for each job to finish before starting the '
                     'next one.\nOnly waiting mode is possible now, --restart/'
                     '--no-wait will be ignored.')
        return BlockingJobSystem(dir=job_dir)

    def create_jobsystem(self, job_dir: os.PathLike,
                         account: str, sbatch_cmd: str, args) -> JobSystem:
        '''returns the job system that should be used

        .. note::

            This method will be called on every execution of the program, thus,
            it may be called multiple times, if the program is resumed after
            waiting for a job to finish. The contents of the config file and the
            command line arguments may change between calls, if the user passes
            different arguments or changes the config file.
        '''
        jobsystem = args.jobsystem
        if jobsystem == 'blocking':
            return self._create_blocking_jobsystem(job_dir)
        elif os.name == 'nt' and jobsystem == 'slurm':
            logging.info('SLURM not supported on Windows. Using blocking job.')
            return self._create_blocking_jobsystem(job_dir)
        elif os.name == 'posix' and jobsystem == 'slurm':
            # to determine if SLURM is installed/available, we just check,
            # if the sbatch command is available
            if shutil.which(sbatch_cmd) is not None:
                return self._create_slurm_jobsystem(job_dir, account,
                                                    sbatch_cmd)
            else:
                logging.info('sbatch not found. Using blocking job system.')
                return self._create_blocking_jobsystem(job_dir)
        elif jobsystem != 'slurm' and jobsystem != 'blocking':
            raise ValueError(f'Unknown job system "{jobsystem}"')
        else:
            raise NotImplementedError('Unsupported operating system '
                                      f'"{os.name}"')

    @abstractmethod
    def create_investigation(self, context: InvestigationContext,
                             config: ConfigT,
                             cmd_args: argparse.Namespace) -> T:
        '''This method is called, when no investigation has been submitted yet.
        It should create and return the main investigation object.

        .. note::

            This method is called only once per workspace. If the program is
            resumed after waiting for jobs to finish, this method is not called.

        :param config: Contents of the loaded configuration file. If the config
                        file is a python file, this is the module object. If the
                        config file is a TOML file, this is a dictionary.
        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        '''

    def postprocessing(self, inves: T, cmd_args: argparse.Namespace):
        '''can be overridden to deal with the investion after it is finished,
        e.g. for printing results, etc.

        .. note::

            The program may be restarted after waiting on a job to finish. If
            the user changes the configuration file or command line arguments,
            they may be different from what was used when setting up the
            investigation!

        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        '''

    def check_cmd_args(self, cmd_args: argparse.Namespace):
        '''Can be overridden to perform checks on the provided cmd_args.

        .. note::

            Don't forget to call `super.check_cmd_args(cmd_args)` to perform
            default checks!

        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        :raise: IllegalCmdArgsError if the check fails. The mesage is shown to
                the user.'''
        workspace = Path(cmd_args.workspace).resolve()
        if workspace.exists():
            if not workspace.is_dir():
                raise IllegalCmdArgsError(f'{cmd_args:f} must be a directory.')

    def add_cmd_args(self, parser: ArgumentParser):
        '''can be overridden to add additional command line arguments

        .. note::

            This method will be called on every execution of the program, thus,
            it may be called multiple times, if the program is resumed after
            waiting for a job to finish.
        '''
        pass

    def start(self, argv:list[str] = None):
        '''set up the command line interface and run the investigations

        :param argv: alternative command line arguments. If None, the arguments
                     from sys.argv are used. This is only used for testing.
        '''
        if self.__exit_gracefully:
            self.__handle_errors(self.__start, argv)
        else:
            return self.__start(argv)

    def __start(self, argv: list[str]):
        if hasattr(self, '__init_called'):
            # simplify debugging by printing error message for this common error
            raise ProgrammingError('super().__init__() was not called in the '
                                   'CommandLineInterface child class')

        argv = sys.argv if argv is None else argv
        args = self.__parse_args(argv)

        # set up logging as early as possible (errors in parse_args can
        # unfortunately not be redirected to the correct file)
        logging.basicConfig(
            filename=args.log_file,
            format='%(levelname)s:%(message)s',
            level=self.LOG_LEVELS[args.log_level])

        workspace = Path(args.workspace).resolve()
        self.__prepare_workspace(workspace)
        is_conti = self.__is_continuation(workspace)

        # cmd args are only checked, if the program is executed for the first
        # time in this workspace (i.e., not in continuation mode). This is
        # because programmers may choose to create certain objects already in
        # in check_cmd_args or read inf files that are later not available
        # anymore.
        if not is_conti:
            self.check_cmd_args(args)

        config, python_exec = self.__load_config(args.config)

        # also calls create_jobsystem() and get_context_managers()
        context, jobsystem = self.__create_inves_context(workspace, args,
                                                         config)
        with context:
            if not is_conti:    # create investigation only once
                self.__setup_and_run(context, config, args)
            is_finished = self.__refresh(context)

        if is_finished:
            logging.info('Main investigation is finished.')
            self.__postprocessing(context, args)
        else:
            # If the blocking job system is used, we have to use the wait
            # strategy
            if args.wait or isinstance(jobsystem, BlockingJobSystem):
                self.__wait(context)
                self.__postprocessing(context, args)
            else:
                self.__schedule_restart(jobsystem, workspace=workspace,
                                       python_exec=python_exec,
                                       max_autosubmit=args.max_autosubmit,
                                       argv=argv)

    def __parse_args(self, argv) -> Namespace:
        '''parse the command line, check the arguemnts and return them

        :raise: IllegalCmdArgsError if the check fails'''
        try:
            args = self.__parser.parse_args(argv[1:])
        except argparse.ArgumentError as err:
            raise IllegalCmdArgsError(f'Could not parse command line arguments: '
                                    f'{str(err)}') from err

        return args

    def __add_args(self):
        self.__add_default_args(self.__parser)

        # add POSITIONAL ARGUMENTS to the parser
        if len(self.POSITIONAL_ARGUMENTS) > 1:
            warnings.warn('The POSITIONAL_ARGUMENTS attribute of the command '
                          'line interface class will be removed in the future.'
                          'Use parse_cmd_args() instead.', DeprecationWarning,
                          stacklevel=2)

            for arg_name, arg_descr in self.POSITIONAL_ARGUMENTS:
                if arg_name.startswith('-'):
                    raise ProgrammingError('Positional arguments must not '
                                           'start with a dash ("-")')

                try:
                    self.__parser.add_argument(arg_name, help=arg_descr)
                except argparse.ArgumentError as err:
                    raise ProgrammingError('Could not add positional argument '
                                           f'"{arg_name}": {str(err)}') from err

        try:
            self.add_cmd_args(self.__parser)
        except argparse.ArgumentError as err:
            raise ProgrammingError('Could not add command line argument: '
                                   f'{str(err)}') from err

    def __add_default_args(self, parser: ArgumentParser):
        '''add default arguments used for all investigaitons to the parser'''
        parser.add_argument(
            'workspace',
            help='workspace directory in which the data is stored',
            metavar='WORKSPACE'
        )
        parser.add_argument(
            '--restart', '--no-wait',
            action='store_false',
            dest='wait',
            default=False,
            help='do not keep the Python process alive and restart this script '
                 'once all jobs are finished. [default]'
        )
        parser.add_argument(
            '--wait', '--no-restart',
            action='store_true',
            dest='wait',
            default=False,    # wait==False, if --wait not added
            help='keep the Python process alive and check for finished jobs'
        )
        parser.add_argument(
            '--max_autosubmit',
            dest='max_autosubmit',
            type=int,
            help='number of times this script should be restarted, if --wait is'
                 ' not set. [default: %(default)d]',
            metavar='N_CALLS',
            default=25
        )
        # base example in help text on self.CONFIG_TYPE
        _example_file_endings = {'python': 'py', 'toml': 'toml'}
        parser.add_argument(
            '--config',
            dest='config',
            help='configuration file, e.g., '
                 f'config.{_example_file_endings[self.CONFIG_TYPE]} '
                 '[default: %(default)s]',
            metavar='CONFIG_FILE',
            default=None
        )
        parser.add_argument(
            '--loglevel',
            dest='log_level',
            help='Set the logging level. Choices are: "' +
                 '", "'.join(self.LOG_LEVELS.keys()) + '". '
                 '[default: %(default)s]',
            default='debug',
            choices=tuple(self.LOG_LEVELS.keys())
        )
        parser.add_argument(
            '-l', '--log',
            dest='log_file',
            help='path to the LOG_FILE. [default: %(default)s]',
            default='log'
        )
        parser.add_argument(
            '--jobsystem',
            help='Name of the job system to use. [default: blocking]',
            action='store',
            type=str,
            default='slurm',
            choices=('blocking', 'slurm'),
            dest='jobsystem'
            )
        slurm_args = parser.add_argument_group(
            title='SLURM options',
            description='Options for SLURM Workload Manager'
        )
        slurm_args.add_argument(
            '--sbatch',
            dest='sbatch_cmd',
            help='SLURM\'s sbatch command. [default: %(default)s]',
            metavar='CMD',
            default='sbatch'
        )
        slurm_args.add_argument(
            '--account',
            dest='slurm_account',
            help='SLURM account that should be used',
            metavar='ACCOUNT'
        )

        return parser

    def __handle_errors(self, func, *args, **kwargs):
        '''decorator that catches all exceptions

        :param func: function to decorate
        :param args: arguments for the function
        :param kwargs: keyword arguments for the function'''
        try:
            return func(*args, **kwargs)
        except (ArgumentError, UserError) as err:
            # For the kind of errors that are meant to be shown to the
            # user  we usually do not need the stacktrace
            logging.debug('User error:\n' +
                          ''.join(traceback.format_exception(err)))

            self.__error(msg=str(err), exit_code=1)
        except Exception as err: # pylint: disable=broad-except
            # All non-user errors should have been caught before, so
            # these errors are unexpected and should be logged properly
            logging.error('A fatal error occured:\n' +
                          ''.join(traceback.format_exception(err)))
            self.__error(msg=f'A fatal error occured: {str(err)}\nCheck the log'
                             ' for more information.',
                         exit_code=1)

    def __error(self, msg: str, print_usage: bool = True, exit_code: int = 1):
        '''print an error message and exit the program'''
        if print_usage:
            msg = self.__parser.format_usage() + '\n' + msg

        sys.stderr.write(msg + '\n')
        sys.exit(exit_code)

    def __load_config(self, config_path) -> tuple[ConfigT, str|None]:
        if self.CONFIG_TYPE == 'python':
            loader = _PythonConfigLoader(config_path)
            config, python_exec = loader.load()
        elif self.CONFIG_TYPE == 'toml':
            loader = _TomlConfigLoader(config_path)
            config, python_exec = loader.load()
        else:
            raise ValueError(f'Unknown config type "{self.CONFIG_TYPE}"')

        if python_exec is None:
            python_exec = sys.executable
            logging.debug('Using sys.executable="%s" as python_exec',
                          python_exec)

        return config, python_exec

    def __prepare_workspace(self, workspace: Path):
        if not workspace.exists():
            logging.debug('Creating workspace directory "%s"', workspace)
            workspace.mkdir(parents=True)
        elif not workspace.is_dir():
            raise NotADirectoryError(f'{workspace} is not a directory')

    def __is_continuation(self, workspace: Path) -> bool:
        """
        :return: True, if the workspace contains an investigation file, False,
                 if the workspace is empty
        :raise: WorkspaceNotEmptyError if the workspace is not empty, but does
                not contain an investigation file either"""
        inves_file = workspace/self.INVESTIGATIONS_FILE
        if len(os.listdir(workspace)) > 0:
            if inves_file.exists():
                logging.debug('Workspace seems to contain pickled investigations'
                              '. Trying to continue...')
                return True

            raise WorkspaceNotEmptyError(
                        f'{workspace} is not empty, but does not contain an '
                        f'investigation either (File '
                        f'"{self.INVESTIGATIONS_FILE}" not found). To avoid '
                        'overriding files or using a corrupted workspace, the '
                        'program will exit now.')
        else:
            return False

    def __create_inves_context(self, workspace, args, config)\
            -> tuple[InvestigationContext, JobSystem]:
        jobsystem = self.create_jobsystem(job_dir=workspace/self.JOB_DIR,
                                          account=args.slurm_account,
                                          sbatch_cmd=args.sbatch_cmd,
                                          args=args)
        context = InvestigationContext(path=workspace/self.INVESTIGATIONS_FILE,
                                       jobsystem=jobsystem,
                                       context_mgrs=self.get_context_managers(
                                                        config, args),
                                       fail_deadly=self.__fail_deadly)
        return context, jobsystem

    def __setup_and_run(self, opened_context: InvestigationContext,
                       config: ArgumentParser, cmd_args)-> bool:
        """ create and submit the main investigation

        :raise: ProgrammingError if no investigation is found in the context
        """
        if opened_context.inves_mgr.n_investigations == 0:
            inves = self.create_investigation(opened_context, config,
                                                cmd_args)

            inves_id = opened_context.inves_mgr.submit(inves)

            logging.info('Submitted main investigation with id %d',
                            inves_id)
            assert inves_id == 0
        else:
            raise ProgrammingError('The program is in continuation mode, '
                                    'but no investigation was found in the '
                                    'context. This should not happen.')

    def __refresh(self, opened_context: InvestigationContext) -> bool:
        """refresh the jobsystem and check if the main investigation is finished

        :return: True, if the main investigation is finished, False otherwise
        """
        inves: T = opened_context.inves_mgr.get_investigation_by_id(0)

        if inves is None:
            raise UserError(
                "No investigation found. The workspace may be corrupted."
            )

        # check if new jobs are finished
        opened_context.jobsystem.refresh()

        return not inves.is_running


    def __wait(self, context: InvestigationContext):
        while True:
            sleep(self.SLEEP_TIMER)

            # open and close the context manager inside the loop to store
            # all progress on disk each time sth changes although this is
            # computationally more expensive
            with context:
                # check if new jobs are finished
                context.jobsystem.refresh()

                inves: T = context.inves_mgr.get_investigation_by_id(0)

                if not inves.is_running:
                    return

    def __schedule_restart(self, jobsystem: JobSystem, workspace: Path,
                          python_exec: str, max_autosubmit: int,
                          argv: list):
        with jobsystem:
            if self.__count_calls(workspace) < max_autosubmit:
                cwd = Path(os.getcwd()).resolve()
                if self.add_restart_argv is None:
                    args = argv[1:]
                else:
                    args = self.add_restart_argv + argv[1:]

                logging.debug('The program is scheduled for restart with the '
                              'following script '
                              'cmd: %s %s in %s', self.script, ' '.join(args), str(cwd))

                job = PythonScriptJob(script=self.script,
                                      arguments=args,
                                      working_dir=cwd,
                                      python=python_exec,
                                      runtime=timedelta(hours=5))

                running_job_ids = jobsystem._get_running_ids()

                # submit this script as a job and execute it after all current
                # jobs are done
                jobsystem.submit(job, wait_for=running_job_ids)
            else:
                logging.info('The investigation is not finished, but the limit'
                             ' of automatic restarts (%d) was '
                             'reached. If you would like to continue, increase '
                             'the limit with the --max_autosubmit option.',
                             max_autosubmit)

    def __count_calls(self, workspace: Path) -> int:
        '''keeps track how often this function was called by using a counter in
        a file in the workspace. If this function is called once per execution
        of this script, it can be used to count how often the script is executed
        with the workspace.'''

        counter_file = workspace/'__counter__'

        if counter_file.exists():
            with open(counter_file, encoding='utf-8') as fp:
                counter = int(fp.read())

        else:
            counter = 0

        with open(counter_file, 'w', encoding='utf-8') as fp:
            fp.write(str(counter+1))

        return counter

    def __postprocessing(self, context: InvestigationContext,
                         cmd_args: Namespace):
        with context:
            inves: T = context.inves_mgr.get_investigation_by_id(0)
            self.postprocessing(inves, cmd_args)

class TypeConversionError(Exception):
    """raised when a value could not be converted to the expected type"""

def dict2dataclass(dict_obj: dict, cls: type,
                   aliases: Mapping[str, str|Mapping[str, ]] = None):
    """Converts a dictionary to a dataclass instance.

    The keys of dict_obj must match the field names of cls. Additional values
    whose keys do not match any field of cls are ignored. If a mandatory field
    is not found in dict_obj, a KeyError is raised. Non-init fields are set
    after the initialization of the object, if they are present in dict_obj,
    otherwise, they are not set, but could still be set by __post_init__() of
    the dataclass.
    If the type of a field is another dataclass and the corresponding value in
    dict_obj is not already of that type, the function will recurse and
    expect the corresponding value in the dict to be another dict.

    This function expects each field to have a single type. Union types are not
    supported.

    .. code::python

        @dataclass
        class A:
            a: int
            b: int

        @dataclass
        class B:
            d: A
            c: int

        @dataclass
        class APlus(B):
            '''A with an additional field'''
            e: int

        dict_obj = {'z': 1, 'd': {'a': 2, 'B': 3}}

        b = dict2dataclass(
                dict_obj,
                B,
                # z -> c, d.B -> d.b, tpye(B.d) -> APlus
                aliases={'z':'c', 'd':{'B': 'b', '__type__': APlus}})

    :raise: TypeError if cls is not a dataclass
    :raise: TypeConversionError if a value in dict_obj does not match the type
            of the corresponding field in cls and cannot be cast. args will
            be (field_name, expected_type, actual_type)
    :raise: KeyError if a field is not found in dict_obj. args[0] will be the
            missing field name
    :raise: NotImplementedError, if a field has a Union type
    :param cls: dataclass, an instance of which is to be created
    :param dict_obj: dictionary with the same keys as the fields of cls
    :param aliases: mapping of aliases to field names. Aliases for nested
                    classes can be supplied as nested dict using the field name
                    as key.
    :return: instance of cls with data from dict_obj"""
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"cls ({cls}) must be a dataclass")

    if aliases is not None:
        field_names = {f.name for f in dataclasses.fields(cls)}

        # copy dict before replacing aliases with field names to keep the
        # original dict unchanged
        new_dict = {}
        for k, v in dict_obj.items():
            # if k is a field name, aliases could contain an entry for it,
            # i.e., in the case that k refers to a nested field
            if k not in field_names:
                new_dict[aliases.get(k, k)] = v
            else:
                new_dict[k] = v
        # aliases for nested dicts (i.e. where key in alias is also a
        # field name and the value is an alias dict) are stored separately
        nested_aliases = {k: v
                          for k, v in aliases.items()
                          if k in field_names}

        dict_obj = new_dict
    else:
        nested_aliases = {}

    values = {}
    non_init_values = {}

    # field.type will be a string in the future (or with from __future__ import
    # annotations). So we use get_type_hints to resolve the types
    types = typing.get_type_hints(cls)

    for field in dataclasses.fields(cls):
        field: dataclasses.Field

        if field.name not in dict_obj:
            if (field.default != dataclasses.MISSING
                    or field.default_factory != dataclasses.MISSING
                    or not field.init):
                # field has a default value
                continue
            else:
                raise KeyError(field.name)

        val = dict_obj[field.name]
        field_type = types[field.name]

        # since np.typing.ArrayLike is a Union, it needs special treatment
        field_type = np.ndarray if field_type == ArrayLike else field_type

        if isinstance(field_type, UnionType):
            raise NotImplementedError('Union types are not supported')

        # isinstance not supported for `list[int]`, so we convert it to `list`
        origin = get_origin(field_type)
        if origin is not None:  # no square brackets also means no origin
            field_type = origin

        # allow conversion of iterables (necessary, if the type hints are
        # very strict)
        if isinstance(val, Iterable) and not isinstance(val, str):
            if field_type in (list, tuple, set):
                val = field_type(val)
            if field_type == np.ndarray:
                val = np.array(val) # returns np.ndarray
        # also allow conversion of numeric types
        elif isinstance(val, (int, float)) and field_type == complex:
            val = complex(val)
        elif isinstance(val, int) and field_type == float:
            val = float(val)
        elif isinstance(val, float) and field_type == int:
            if val.is_integer():
                val = int(val)
        # and convert strings to Path objects
        elif isinstance(val, str) and field_type == Path:
            val = Path(val)

        if not isinstance(val, field_type):
            # recursion
            if isinstance(val, dict) and dataclasses.is_dataclass(field_type):
                inner_aliases = nested_aliases.get(field.name, None)
                if inner_aliases is not None:
                    field_type = inner_aliases.get('__type__', field_type)

                val = dict2dataclass(val, field_type, aliases=inner_aliases)
            else:
                # choose ValueError instead of type error to distinguish from
                # case above which is most likely a programming error whereas
                # this can also be a user error.
                raise TypeConversionError(field.name, field_type, type(val))

        if field.init:
            values[field.name] = val
        else:
            non_init_values[field.name] = val

    # create dataclass object
    obj = cls(**values)

    # fields where init=False need to be set after initialization
    for name, value in non_init_values.items():
        setattr(obj, name, value)

    return obj