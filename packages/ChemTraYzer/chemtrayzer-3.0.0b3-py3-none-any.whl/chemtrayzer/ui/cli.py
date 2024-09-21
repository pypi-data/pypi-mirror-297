"""Main command line interface

To add a new command to the chemtrayzer command, add it to the _COMMANDS
dictionary. The key is the name of the command and the value is either a
CommandLineInterface class or a function that is called with the parsed
arguments.
"""
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
import sys

from chemtrayzer.engine.cmdtools import CommandLineInterface
from chemtrayzer.reaction_sampling.reaction_sampling_investigation import AnalyzeTrajCLI, RunMDCLI

# to enable the test command, we need to ensure that pytest is installed
try:
    import pytest
except ImportError:
    _pytest = False
else:
    _pytest = True
    from chemtrayzer.engine.testing import BatchCLI


class Command(ABC):
    '''Abstract base class for commands that can be called with the
    chemtrayzer command'''

    def __init__(self, name: str, subparser: ArgumentParser):
        self.name = name
        self.subparser = subparser

    @abstractmethod
    def __call__(self, args: Namespace):
        pass

class CliCommand(Command):
    """Command that simply wraps a CommandLineInterface"""

    def __init__(self, name: str, subparser: ArgumentParser,
                 cli_type: type[CommandLineInterface]):
        super().__init__(name, subparser)

        # When restarting, the CLI will create a bash script that executes the
        # following statenent: "script" "args[1]" "args[2]" "args[3]" ... where
        # args is the list of arguments that are passed. When using a subparser
        # and since the CLI does not know it uses a subparser, the above
        # statement would be missing the command (args[0] is the
        # command/`name'). Thus, we have to pass the name as additional argument
        self.cli = cli_type(script=__file__,
                            add_restart_argv=[name],
                            arg_parser=self.subparser)

    def __call__(self, args: Namespace):
        # The CLI does not know that the subparser it has is not the main
        # parser. The class was designed in such a way, that it assumes all of
        # argv[1:] to be arguemnts. But when using a subparser/command, only
        # argv[2:] are the arguments. Thus, we have to remove argv[0] and pass
        # the command as additional argument when restarting as explained above
        self.cli.start(argv=sys.argv[1:])


def hello_world(args: Namespace):
    '''test function that is called with the chemtrayzer test command'''
    print('Hello world!')


# The chemtrayzer command can be called with subcommands like this:
# `chemtrayzer test`. Here test is a subcommand of chemtrayzer.
# Each subcommand has its own parser, function and name. The name and function
# have to be registered here while the parser will be created automatically.
_COMMANDS = {
    'analyze': AnalyzeTrajCLI,
    'runmd': RunMDCLI,
    'hello': hello_world,
}

if _pytest:
    _COMMANDS['test'] = BatchCLI


def main():
    '''main function that is called with the chemtrayzer command'''
    # set up basic parser
    parser = ArgumentParser()
    allowed_cmds_str = "'" + "', '".join(_COMMANDS.keys()) + "'"
    subparser_action = parser.add_subparsers(
        dest='__cmd__', # stores command name in __cmd__
        help=f'ChemTrayZer command (choose from {allowed_cmds_str}).'
             ' Use "%(prog)s COMMAND -h" for help.',
        metavar='COMMAND'
        )

    # add subparsers for each command
    callables = {}
    for name, thing in _COMMANDS.items():
        subparser = subparser_action.add_parser(name)

        if isinstance(thing, type) and issubclass(thing, CommandLineInterface):
            # the CLI commands may add their own arguments to the subparser
            callables[name] = CliCommand(name, subparser, thing)
        elif callable(thing):
            callables[name] = thing
        else:
            raise TypeError(f'Invalid type for command {name}: {type(thing)}')

    # parse arguments and execute the command
    args = parser.parse_args()
    command_called = args.__cmd__   # name of the subparser/command

    if command_called is None:
        parser.print_help()
        return

    # call the function that is registered for the subparser/command and pass
    # the parsed arguments to it.
    callables[command_called](args)

if __name__ == '__main__':
    main()