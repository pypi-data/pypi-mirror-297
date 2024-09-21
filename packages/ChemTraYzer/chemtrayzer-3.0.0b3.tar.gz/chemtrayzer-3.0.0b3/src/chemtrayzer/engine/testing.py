"""
This module contains functionality for testing investigations and jobs.
"""
import argparse
import functools
import importlib
import logging
import os
import pathlib
import shutil
import pickle
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from datetime import timedelta
from difflib import Differ
from distutils.dir_util import copy_tree
from os import PathLike
from types import ModuleType
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from chemtrayzer.engine._event import EventDispatcher
from chemtrayzer.engine._submittable import Failure, State, Submittable
from chemtrayzer.engine.cmdtools import CommandLineInterface, IllegalCmdArgsError
from chemtrayzer.engine.investigation import (
    BatchInvestigation,
    Investigation,
    InvestigationContext,
    InvestigationError,
)
from chemtrayzer.engine.jobsystem import Job, JobSystem, Memory, _JobFinishedEvent

__all__ = ['JobTester', 'InvestigationTestCase', 'MockJob', 'DummyJob',
           'DummyInvestigation', 'BatchCLI']

class DummyJob(Job):
    ''' a simple dummy job with some arbitrary default values

    :param parse_result_state: state to which the job is set upon
            calling parse_result()
    '''

    def __init__(self, parse_result_state: State = None, name="job name",
            n_tasks=3, n_cpus=2, memory=Memory(140), account=None,
            runtime=timedelta(days=3, minutes=10), command='my_programm.exe',
            id = None, state=State.PENDING) -> None:
        super().__init__(name=name, n_tasks=n_tasks, n_cpus=n_cpus,
            memory=memory, runtime=runtime, account=account)

        self._id = id
        self._cmd = command
        self._state = state
        self._final_state = parse_result_state
        self._parse_result_calls = [] # list of arguments passed to pass_result
        self._gen_input_calls = []

    @property
    def command(self):
        return self._cmd

    def gen_input(self, path):
        self._gen_input_calls.append(path)

    def parse_result(self, path):
        self._parse_result_calls.append(path)

        if self._final_state is not None:
            if self._final_state == State.FAILED:
                self.fail(Failure())
            elif self._final_state == State.SUCCESSFUL:
                # allow setting a result beforehand for test purposes
                if self.result is None:
                    self.result = self.Result()
                self.succeed()
            else:
                self._state = self._final_state

    def assert_parse_result_not_called(self):
        assert len(self._parse_result_calls) == 0

    def assert_parse_result_called_once_with(self, args):
        n_calls = len(self._parse_result_calls)
        if n_calls != 1 or self._parse_result_calls[0] != args:
            raise AssertionError(f'parse_result called {n_calls} times with '
                f'arguments {self._parse_result_calls}')

    def assert_gen_input_called_once_with(self, args):
        n_calls = len(self._gen_input_calls)
        if n_calls != 1 or self._gen_input_calls[0] != args:
            raise AssertionError(f'gen_input called {n_calls} times with '
                f'arguments {self._gen_input_calls}')

    def finish_successfully(self):
        self.succeed()
        # usually the job system would to this, but we are not using it here
        EventDispatcher().trigger(_JobFinishedEvent(job_id=self.id,
                                                   job=self))

class JobTester:
    ''' Provides some utility functions to test Job classes
    '''

    def __init__(self, tmp_path_factory):
        # do not use the tmp_path fixture, because it may be used by tests for
        # other purposes
        self.tmp_path_factory = tmp_path_factory

    def test_gen_input_writes_files(self, job: Job,
            contents: Dict[str, str] = None,
            expected_files: Union[Dict[str, str], os.PathLike, str] = None):
        '''
        Calls job.gen_input(tmp_path) and asserts that all files defined in
        contents have been written.

        :param job: job object to test
        :param contents: dictionary whose keys are file names and whose values
                         are the expected contents of the file after gen_input()
                         has been called
        :param expected_files: alternative/addition to "contents".
                               If this is a dictionary, the keys are the names
                               of files that ``gen_input()`` is supposed to
                               generate in the job folder and the values are
                               paths to files that contain the expected input of
                               those files.
                               If it is a path or string, it should point to a
                               folder containing all the files that are supposed
                               to be generated with the correct name.
        '''
        # ARANGE
        path = pathlib.Path(self.tmp_path_factory.mktemp('JobTester_dir',
                                                         numbered=True))

        # ACT
        job.gen_input(path)

        # ASSERT
        self.assert_job_dir_contains_expected_files(path, contents,
            expected_files)


    @classmethod
    def assert_job_dir_contains_expected_files(cls, job_dir: os.PathLike,
            contents: Dict[str, str] = None,
            expected_files: Union[Dict[str, os.PathLike], os.PathLike] = None):
        '''
        :job_dir: directory in which ``gen_input()`` was supposed to generate
                  the files whose contents and file names will be checked
        :param contents: dictionary whose keys are file names and whose values
                         are the expected contents of the file after gen_input()
                         has been called
        :param expected_files: alternative/addition to "contents".
                               If this is a dictionary, the keys are the names
                               of files, that ``gen_input()`` is supposed to
                               generate in the job folder and the values are
                               paths to files that contain the expected input of
                               those files.
                               If it is a path or string, it should point to a
                               folder containing all the files that are supposed
                               to be generated with the correct name.
        '''
        job_dir = pathlib.Path(job_dir)

        # add stuff from expected files to contents
        if contents is None:
            contents = {}

        if expected_files is not None:
            if isinstance(expected_files, dict):
                for name, in_path in expected_files.items():
                    assert name not in contents
                    with open(in_path, 'r', encoding='utf-8') as file:
                        contents[name] = file.read()
            elif pathlib.Path(expected_files).is_dir():
                files = os.listdir(expected_files)
                if len(files) == 0:
                    logging.warning(f'Path for expected files "{expected_files}" '
                        'is empty.')

                for fname in files:
                    if fname in contents:
                        raise ValueError(f'File "{fname}" is defined in '
                            'both "contents" and via "expected_files".')
                    # when an empty folder should be commited to git, you
                    # typically create an empty file ".gitkeep" in it. We want
                    # to ignore those files
                    if fname == '.gitkeep':
                        continue

                    with open(pathlib.Path(expected_files)/fname, 'r',
                            encoding='utf-8') as file:
                        contents[fname] = file.read()
            else:
                raise ValueError('expected_files must be a dictionary or an '
                    'existing directory')


        # do assertion for the whole content of each expected file
        for f_name, expected_content in contents.items():
            f_path = job_dir / f_name

            if not f_path.is_file():
                raise AssertionError(f'File {f_name} was not generated by the '
                                     'job')

            with open(f_path, encoding='utf-8', mode='r') as f:
                actual_content = f.read()

            if expected_content != actual_content:
                d = Differ()
                diff = list(d.compare(expected_content.splitlines(),
                          actual_content.splitlines()))

                raise AssertionError(f'Contents of {f_name} not as expected:\n'
                    + '\n'.join(diff))

    def _write_fake_job_output(self, tmp_path: str, contents: Dict[str, str],
            out_files: Dict[str, Union[str, os.PathLike]]):
        tmp_path = pathlib.Path(tmp_path)

        for f_name, content in contents.items():
            path = tmp_path / f_name

            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

        for f_name, path in out_files.items():
            shutil.copy(path, tmp_path / f_name)

    def test_parse_result(self, job: Job,
            contents: Dict[str, str],
            out_files: Dict[str, Union[str, os.PathLike]],
            expected_result: Dict,
            atol = 0.0,
            rtol = 1e-8,
            checkers: Dict[str, Callable] = None):
        '''used to check if the output is parsed correctly

        :param job: job object to test
        :param tmp_path: temporary path, usually tmp_path fixture
        :param contents: dictionary, where the keys are file names of the output
                        files which should be parsed and the values are their
                        contents
        :param out_files: output files which are too large to provide as string
                          in `contents`, can be copied from the source path
                          defined by the values of this dictionary. The keys are
                          the file names, that the job expects.
        :param expected_result: expected contents of job.result after
                                job.parse_result() has been called.
        :param atol: absolute tolerance for numerical values (incl. ndarrays)
        :param rtol: relative tolerance for numerical values (incl. ndarrays)
        :param checkers: If values in job.results should be checked with
                         something other than an equality assertion, one may
                         provide a function to perform the check via this dict.
                         Using the same key as the to-be-tested value in
                         job.results has, one can provide a callable which
                         returns True if the value passes the test and false if
                         it does not.
                         E.g. if job.results['message'] is expected to contain a string starting with 'Hello', this dictionary could
                         look like this: `checkers = {'message': lambda val :
                         val.startswith('Hello)}`
        '''
        # arrange
        tmp_path = self.tmp_path_factory.mktemp('JobTester_dir', numbered=True)
        self._write_fake_job_output(tmp_path, contents, out_files)
        job.id = 1
        job._state = State.RUNNING

        # act
        job.parse_result(tmp_path)

        # assert
        assert isinstance(job.result, Job.Result), 'job.result is not a Job.Result object'
        for key, expected_data in expected_result.items():
            if not hasattr(job.result, key):
                raise AssertionError(f'job.result does not contain key "{key}"')

            data = job.result[key]

            if isinstance(data, (np.ndarray, np.dtype, int, float, complex)):
                if data != pytest.approx(expected_data, rel=rtol, abs=atol):
                    raise AssertionError(f'job.result["{key}"] != '
                        f'pytest.approx(expected_result["{key}"], rel={rtol}, '
                        f'abs={atol})\n where job.result["{key}"]='
                        f'\n{job.result[key]}\n and expected_result["{key}"]='
                        f'\n{expected_data}')
            else:
                if data != expected_data:
                    raise AssertionError(f'job.result["{key}"] != '
                        f'expected_result["{key}"]\n where job.result["{key}"]='
                        f'\n{job.result[key]}\n and expected_result["{key}"]='
                        f'\n{expected_data}')

        # complex check for single attribute using 'checkers' functions
        if checkers is not None:
            for key, checker in checkers.items():
                if not checker(job.result[key]):
                    raise AssertionError(f'Result with key "{key}" failed '
                        f'check. Current value: {job.result[key]}')

        # test the job result object:
        result = job.result

        # the result of any job should be a job.Result object
        assert isinstance(result, Job.Result), f"Invalid type: Expected job.Result, got {type(result).__name__}."


        # check if the result object is picklable
        try:
            _ = pickle.dumps(result)
        except pickle.PickleError as e:
            raise AssertionError("The result object of the job is not picklable") from e

class _DummyJobSystem(JobSystem):
    """Very basic job system where every job finishes immediately

    You can provide a hook that is called on submission after the id is set.

    :param on_submit: functino that is called with job and wait_for on submission
    """

    def __init__(self, dir: os.PathLike,
                 on_submit: Optional[Callable[[JobSystem, Job, Optional[Iterable[int]]], Any]]
                 ) -> None:
        super().__init__(dir)

        self.on_submit = on_submit

    def submit(self, job: Job, wait_for: Optional[Iterable[int]] = None) -> int:
        job_id = self._job_db.save_job(job)

        job_dir = pathlib.Path(self.get_job_dir(job_id))
        os.mkdir(job_dir)   # raises error if job_dir already exists

        job.gen_input(job_dir)

        job._state = State.RUNNING
        self._job_db.update_job(job_id=job_id, job=job)

        if self.on_submit is not None:
            self.on_submit(self, job, wait_for)

        return job_id

    def _check_finished(self, ids: Iterable[int])\
            -> list[tuple[bool, Failure | None]]:
        # all jobs are already done, so always return True
        return [(True, None) for job_id in ids]

    def _save_resources(self, job: Job):
        job.resources.cpu_time = None
        job.resources.memory = None
        job.resources.n_cpus = None

# define T as general type that can be any subtype of Investigation
T = TypeVar('T', bound=Investigation)

class InvestigationTestCase(ABC, Generic[T]):
    """
    Utility class to simplify testing investigations. This function adds
    additional functionality into certain methods in the investigation and job
    mechanism to insert tests automatically.

    To create a test case for your investigation, simply create a Test... class
    and inherit from InvestigationTestCase. Then you need to set the class
    variables ``JOB_INPUT_PATH``, ``JOB_OUTPUT_PATH`` and ``STEPS``. In addition,
    you need to provide the fixture ``investigation``. ``investigation`` creates
    and returns the investigation that should be tested. A fixture called
    ``inves_context`` is provided by InvestigationTestCase and returns the
    InvestigationContext instance.
    The fixture ``context_managers`` is optional and can be overridden if the
    specific test case requires it. By default, it returns an empty dictionary.

    .. code::

        class TestMyInvestigation(InvestigationTestCase[MyInvestigation]):
            JOB_INPUT_PATH =  'path/to/job/input/files'
            JOB_OUTPUT_PATH = 'path/to/job/output/files'
            STEPS = ['do_some_thing', 'do_next_thing']

            @pytest.fixture
            def context_managers(self, tmp_path) -> Mapping[ContextManager]:
                return {'species_db': SpeciesDB(tmp_path/'db.sqlite')}

            @pytest.fixture
            def investigation(self, inves_context: InvestigationContext)\\
                    -> MyInvestigation:
                return MyInvestigation(initial_data=42)


    The investigation is run almost like in a real system, only that no jobs are
    submitted. Instead, the job input files that are created can be compared to
    expected input files and the output files that are provided are copied into
    the right folder for the investigation to work.
    All you need to do is to supply the expected job input files and the needed
    output generated by the jobs.
    The investigation will be started automatically and it is checked whether the
    steps in ``STEPS`` are executed in the given order. Furthermore, you can add
    functions following the naming scheme: ``step_X(self, investigation)``. If
    such a function exists, it is executed after step number X (starting at zero)
    and can be used to assert that the member variables of the tested
    investigation were set correctly.

    .. code::

        class TestMyInvestigation(InvestigationTestCase[MyInvestigation]):
            ...

            def step_1(self, inves: MyInvestigation):
                \'\'\'will be run after the second step is run.\'\'\'
                assert inves.some_property == 10.0

    """

    @classmethod
    @property
    def JOB_INPUT_PATH(cls) -> os.PathLike | None:
        '''Path to the directory containing the expected input files.

        "expected files" means that the investigation is expected to create
        those files by submitting jobs. The content of the expected files is checked against
        the actual files that are created by the investigation.
        The directory must be structured as follows:

            JOB_INPUT_PATH/
                step_0/
                    job_0/
                    job_1/
                step_1/
                    job_0/
                    ...

        Here, step_X/job_Y contains the expected files for the Y-th job that is
        submitted during the X-th step of the investigation test case.
        '''
        return None

    @classmethod
    @property
    def JOB_OUTPUT_PATH(cls) -> os.PathLike | None:
        '''Path to the directory containing the job output files.

        Since the jobs are not actually executed during testing, the output
        files are not generated. Hence they have to be supplied via this
        directory. They will be parsed by the respective job objects s.t. the
        investigation being tested can simply access the job objects result
        member variable to get the correct data for the test case.
        The directory must be structured as follows:

            JOB_OUTPUT_PATH/
                step_0/
                    job_0/
                    job_1/
                step_1/
                    job_0/
                    ...

        Here, step_X/job_Y contains the output files for the Y-th job that is
        submitted during the X-th step of the investigation test case.
        '''
        return None

    WORKSPACE: Union[str, os.PathLike] = '__tmp__'
    '''Directory in which the investigations and jobs are stored and executed, when this test
    case is run. By default, a temporary directory is created and will be deleted after testing. But when
    this variable points to a path, that path will be used allowing the
    developer to inspect the files creating during the test.'''

    @classmethod
    @property
    @abstractmethod
    def STEPS(cls) -> List[str]:
        '''list of function names of the tested investigations in the order they are executed for this test case'''
        raise NotImplementedError('Your test case does not implement STEPS.')

    _MAX_JOBSYS_REFRESH: int = 50
    '''When executing the test case, jobsystem.refresh() will be called in a loop that does at most this many interations. This number should be big enough for most investigations. For very large investigations, this number can be increased.'''

    TMP_PATH_FACTORY = None
    '''variable that is set by pytest to a function that creates a temporary directory once the test session begins'''


    def run_next_step_decorator(self, run_next_step_func):
        @functools.wraps(run_next_step_func)
        def wrapper(*args, **kwargs):
            try:
                expected_name, assertion = self._steps[self._current_step]

            # the current step counter is increased after each step, so a
            # value error will be raised when executing more steps than
            # defined in self._steps (or STEPS, respectively)
            except ValueError:
                raise AssertionError(
                    'The investigation is trying to execute step '
                    f'{self._current_step}, but only {len(self._steps)} steps '
                    'were defined for this test case in self.STEPS.')

            # steps should be methods of the investigations that use them
            investigation: Investigation = run_next_step_func.__self__

            # check name
            actual_next_step = investigation.tell_next_step()
            if actual_next_step != expected_name:
                raise AssertionError('Unexpected next step.\nExpected: '
                    f'{expected_name}\nActual: {actual_next_step}')

            # run the actual _run_next_step()
            run_next_step_func(*args)


            if assertion is not None:
                assertion(investigation)
                investigation._logger.debug('No assertion failed for step'
                    ' %d "%s"', self._current_step, expected_name)

            self._current_step += 1
            self._current_job = 0

        return wrapper

    def jobsystem_on_submit(self, jobsys: JobSystem, job: Job, *args, **kwargs):
        '''used to decorate JobSystem.submit() to add testing functionality.'''

        logging.debug('Submitted %s with job id = %d',
                        type(job).__name__, job.id)


        # check that it created the input files as expected
        job_dir = pathlib.Path(jobsys.get_job_dir(job.id))
        expected_files = pathlib.Path(self.JOB_INPUT_PATH,
                                        f'step_{self._current_step}',
                                        f'job_{self._current_job}')

        if expected_files.exists():
            JobTester.assert_job_dir_contains_expected_files(job_dir,
                expected_files=expected_files)
        else:
            logging.debug('No expected input files for job %d. Directory'
                            'JOB_INPUT_PATH/step_%d/job_%d not found.',
                            job.id, self._current_step, self._current_job)

        # create the output as if the job did it:
        output_files = pathlib.Path(self.JOB_OUTPUT_PATH,
                                    f'step_{self._current_step}',
                                    f'job_{self._current_job}')

        if output_files.exists():
            copy_tree(str(output_files), str(job_dir), verbose=False)
        else:
            logging.debug('No output files for job %d supplied. Directory '
                            'JOB_OUTPUT_PATH/step_%d/job_%d not found.',
                            job.id, self._current_step, self._current_job)

        self._current_job += 1


    @pytest.fixture
    def _set_up(self, tmp_path_factory):
        self._current_job = 0 # counts jobs submitted during the current step
        self._current_step = 0
        self._steps: List[Tuple[str, Callable[[T], None]]] = []
        # store this as attribute, so that others can access it more easily:
        self.tmp_path_factory = tmp_path_factory

        self.JOB_OUTPUT_PATH = tmp_path_factory.mktemp('job_output') \
            if self.JOB_OUTPUT_PATH is None else self.JOB_OUTPUT_PATH

        self.JOB_INPUT_PATH = tmp_path_factory.mktemp('job_input') \
            if self.JOB_INPUT_PATH is None else self.JOB_INPUT_PATH


        user_defined_assertions = {attr for attr in dir(self)
                  if attr.startswith('step_') and callable(getattr(self, attr))}

        # fill _steps with tuples containing the name of the method of the
        # investigation object and an assertion function (that can be defined by
        # the user)
        for i, step in enumerate(self.STEPS):
            if f'step_{i}' in user_defined_assertions:
                self._steps.append((step, getattr(self, f'step_{i}')))
            else:
                self._steps.append((step, None))

    @pytest.fixture()
    def inves_context(self, context_managers, tmp_path_factory) \
            -> InvestigationContext:

        if self.WORKSPACE == '__tmp__':
            path: pathlib.Path = tmp_path_factory.mktemp('tmp')
        else:
            path = pathlib.Path(self.WORKSPACE)
            if not any(path.iterdir()):
                raise FileExistsError(
                    'The test case workspace directory is not empty: '+
                    str(path))

        with InvestigationContext(path=path/ 'investigations.pickle',
                    jobsystem=_DummyJobSystem(
                                    path/'jobs',
                                    on_submit=self.jobsystem_on_submit),
                    context_mgrs=context_managers,
                    # let all exceptions pass through instead of just failing
                    # failing the investigation
                    fail_deadly=True) as context:
            yield context

    def test_investigation(self, _set_up, inves_context: InvestigationContext,
                           investigation: Investigation, request):
        '''this is the test function that will be executed by pytest'''
        context = inves_context

        # decorate the investigations _run_next_step method
        original_run_func = investigation.run_next_step
        investigation.run_next_step = self.run_next_step_decorator(
                                                original_run_func)

        try:
            context.inves_mgr.submit(investigation)

            i = 0
            while(investigation.is_running):
                if i >= self._MAX_JOBSYS_REFRESH:
                    raise AssertionError(f'Maximum number of iterations reached: {self._MAX_JOBSYS_REFRESH}.\nIf this error is raised, because your investigation contains a lot of steps, you could increase _MAX_JOBSYS_REFRESH, but you should also consider splitting the investigation into several smaller ones.')

                context.jobsystem.refresh()

                i += 1

            if self._current_step < len(self.STEPS):
                raise AssertionError(f'Investigation finished, but not all steps have been executed. The next expected step is "{self.STEPS[self._current_step]}".')

        # undo everything to the context can be closed witout problems
        finally:
            investigation.run_next_step = original_run_func

    @pytest.fixture
    def context_managers(self) -> Dict[str, Any]:
        '''returns a dictionary with the context managers that the investigation
        needs'''
        return {}

class DummyInvestigation(Investigation):
    """
    Helper class for testing the investigation mechanism.

    Provides a basic implementation of the Investigation class that can be
    customized for each test case by adding the predefined steps. All steps
    log their arguments to the history attribute.

    .. code::python
        def test_my_investigation():
            mock_job = MockJob()
            inves= DummyInvestigation(waitables=[mock_job])

            # an investigation with three teps
            inves.add_step(inves.do_nothing)
            inves.add_step(inves.submit_waitables)
            inves.add_step(inves.finish_by_failing)

            # now you can use inves in your tests
            ...

            # after the test, you can check the history of the investigation
            assert inves.history == [('do_nothing', ()),
                                     ('submit_waitables', ()),
                                     ('finish_by_failing', (mock_job,))]

    :param waitables: jobs or investigations that will be submitted by
                      submit_waitables()
    :param mock_job_factory: mock_job_factory fixture
    :param provided_result: result that will be set by the set_result() step,
                            If not set, DummyInvestigation.Result will be
                            initialized with default values
    :ivar history: stores the steps that were called and the arguments
    :type history: Tuple[str, Tuple(Any)]
    """

    class Result(Investigation.Result):
        '''dummy result class'''
        answer: str = '42'
        '''answer to life, the universe and everything'''

    def __init__(self,
                 waitables: Iterable[Union[Job, Investigation]]= None,
                 provided_result: Result = None,
                 target: str = None) -> None:
        super().__init__(target=target)

        self.provided_result = provided_result
        if provided_result is None:
            self.provided_result = DummyInvestigation.Result()

        # stores the steps that were called and the arguments
        self.history: Tuple[str, Tuple(Any)] = []

        if waitables is not None:
            self.waitables = waitables
        else:
            self.waitables = []

    def update(self, event):
        '''just used for logging incoming events'''
        self._logger.debug(f'Update called with event: {event}')
        return super().update(event)

    def set_result(self, *args):
        '''sets the result to the provided result'''
        self.history.append(('set_result', args))

        self.result = self.provided_result

    def finish_successfully(self, *args):
        '''finishes the investigation successfully'''
        self.history.append(('finish_successfully', args))

        self._state = State.SUCCESSFUL

    def finish_by_failing(self, *args):
        '''finishes the investigation by failing'''
        self.history.append(('finish_by_failing', args))

        self.fail('Test failure')

    def do_nothing(self, *args):
        '''just an empty step that logs its arguments'''
        self.history.append(('do_nothing', args))

    def submit_waitables(self, *args):
        '''submits all waitables passed to the constructor'''
        self.history.append(('submit_waitables', args))

        for obs in self.waitables:
            self.wait_for_and_submit(obs)

    def raise_error(self, *args):
        '''raises an error'''
        self.history.append(('raise_error', args))

        raise InvestigationError('Hi, I am an error :)')

    def submit_waitables_but_finish(self, *args):
        '''
        Submits all waitables passed to the constructor and then finishes.
        Only used to test that this behavior is not allowed.'''
        self.history.append(('submit_waitables_but_finish', args))

        for obs in self.waitables:
            self.wait_for_and_submit(obs)

        self.succeed()

    def wait_forever(self, *args):
        '''appends '''
        self.history.append(('wait_forever', args))

        # submit a mock job, that never finishes
        self.wait_for_and_submit(DummyJob())

@pytest.fixture(scope='session')
def prepare_test_inves_class(tmp_path_factory):
    InvestigationTestCase.TMP_PATH_FACTORY = tmp_path_factory

class BatchCLI(CommandLineInterface):
    """Executes one or more jobs or investigations.

    This class is meant to be used for testing purposes. The user needs to
    provide job or investigation objects in a Python file (here called
    `my_file.py`):

    .. code::python

        job1 = MyJob(some_arg=42)
        job2 = MyJob(some_arg=43)
        inves = MyInvestigation()

        SUBMITTABLES = [job1, job2, inves]
        ...

    All jobs and investigations in the SUBMITTABLES variable will be submitted
    and executed. The user can optionally provide a POSTPROCESSORS variable
    that contains a list of executables that will be executed after all
    submittables have finished.

    .. code::python

        ...
        # very simple example functions to print all of the results
        def print_job_output(is_successful, job_result):
            if is_successful:
                print('Job finished successfully')
            else:
                print('Job failed')
            print(job_result)

        def print_inves_output(is_successful: bool, inves_result):
            print(inves_result)

        # We need to supply three postprocessors for the three submittables
        POSTPROCESSORS = [print_job_output, print_job_output,
                          print_inves_output]
        ...

    Now, we can execute the two jobs and the investigation by calling
    ``chemtrayzer test my_file.py``. In addition, we can supply context_managers
    to the investigation, e.g., databases by adding the ``CONTEXT_MGRS``
    variable:

    .. code::python

        # if an investigation expects a SpeciesDB under the name "species_db"
        # we could supply it like this:
        CONTEXT_MGRS = {'species_db': SpeciesDB('path/to/dbfile')}
    """

    def __init__(self, script: PathLike | str, debug_mode: bool = False,
                 arg_parser: ArgumentParser = None,
                 add_restart_argv: list[str] = None) -> None:
        self.__imported: Mapping[str, ModuleType] = dict()
        super().__init__(script=script, debug_mode=debug_mode,
                         arg_parser=arg_parser,
                         add_restart_argv=add_restart_argv)

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'submittables_file',
            help='*.py file containing a SUBMITTABLES variable which is an '
                 'iterable of jobs or investigations that should be submitted.'
                 'Optionally, it can contain an iterable POSTPROCESSORS of '
                 'executables  that do the postprocessing of jobs and '
                 'investigaiton results.',
            action='store',
            metavar='SUBMITTABLES_FILE',
            type=pathlib.Path)
        parser.add_argument(
            '--pickle-path',
            help='Path to the pickle file that stores the results of the '
                 'submittables. If not given, the results will not be stored.',
            action='store',
            type=pathlib.Path,
            default=None,
            dest='pickle_path')

    def check_cmd_args(self, cmd_args: Namespace):
        super().check_cmd_args(cmd_args)
        submittables_file = pathlib.Path(cmd_args.submittables_file).resolve()

        if not submittables_file.exists():
            raise IllegalCmdArgsError(f'"{submittables_file}" not found')
        if not submittables_file.is_file():
            raise IllegalCmdArgsError(f'"{submittables_file}" is not a file.')

    def get_context_managers(self, _: ModuleType, cmd_args: Namespace)\
            -> Mapping[str, ContextManager]:
        module = self.__import_module(cmd_args.submittables_file,
                                      'submittables')

        # check if the postprocessors are defined
        if not hasattr(module, 'CONTEXT_MGRS'):
            return {}
        else:
            return module.CONTEXT_MGRS

    def __import_module(self, module_path: pathlib.Path,
                        name: str) -> ModuleType:
        '''imports the module at the given path and returns it'''
        # all imported modules are stored by their name to not load them twice
        if name in self.__imported:
            return self.__imported[name]

        spec = importlib.util.spec_from_file_location(name,
                                                      module_path)
        if spec is None:
            raise ValueError(f'Could not find file "{module_path}".')
        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except FileNotFoundError as err:
            raise ValueError(f'Could not find file "{module_path}".') \
                from err

        self.__imported[name] = module
        return module

    def __import_submittables(self, submittables_file: pathlib.Path)\
            -> list[Job | Investigation]:
        """imports the submittables from the given file and returns them as a
        list

        :return: list of submittables"""
        module = self.__import_module(submittables_file, 'submittables')

        # check if the submittables are defined
        if not hasattr(module, 'SUBMITTABLES'):
            raise AttributeError(f"Module '{submittables_file.name}' has no "
                                 "attribute 'SUBMITTABLES'")
        submittables = list(module.SUBMITTABLES)

        # check if the submittables are valid
        for submittable in submittables:
            if not isinstance(submittable, Submittable):
                raise AttributeError('The SUBMITTABLES variable must contain '
                                 'instances of Job or Investigation.')

        return submittables

    def __import_postprocessors(self, submittables_file: pathlib.Path)\
            -> list[Callable] | None:
        """
        :return: list of postprocessors or None, if no postprocessors are
                    defined
        """
        module = self.__import_module(submittables_file, 'submittables')

        # check if the postprocessors are defined
        if not hasattr(module, 'POSTPROCESSORS'):
            return None
        else:
            return list(module.POSTPROCESSORS)

    def __check_postprocessors(self, submittables_file: pathlib.Path,
                               n_submittables: int):
        '''checks if the postprocessors are valid'''
        postprocessors = self.__import_postprocessors(submittables_file)
        if postprocessors is not None:
            if len(postprocessors) != n_submittables:
                raise ValueError('If defined, the POSTPROCESSORS variable must '
                                'contain as many elements as the SUBMITTABLES '
                                'variable.')

            # check if the postprocessor takes two arguemnts and the first one
            # is a bool
            for postprocessor in postprocessors:
                if not callable(postprocessor):
                    raise ValueError('The POSTPROCESSORS variable must contain '
                                     'callable objects.')
                if not callable(postprocessor):
                    raise ValueError('The POSTPROCESSORS variable must contain '
                                     'callable objects that take two arguments '
                                     'of type bool and a job or investigation.')

    def create_investigation(self, context: InvestigationContext,
                             config: ModuleType, cmd_args: Namespace) -> Any:
        submittables = self.__import_submittables(cmd_args.submittables_file)

        # fail early (before submitting)
        self.__check_postprocessors(cmd_args.submittables_file,
                                    len(submittables))

        inves = BatchInvestigation(inves_and_job_list=submittables,
                           pickle_path=cmd_args.pickle_path,
                           pickle_results=cmd_args.pickle_path is not None
                           )

        return inves

    def postprocessing(self, inves: BatchInvestigation, cmd_args: Namespace):
        postprocessors = self.__import_postprocessors(
            cmd_args.submittables_file)

        if postprocessors:
            for postprocessor, is_successful, result in zip(postprocessors,
                                                    inves.result.success_list,
                                                    inves.result.results_list):
                postprocessor(is_successful, result)

