"""
This module contains the core functionality to implement, manage and run
investigations. For most people, only the
:class:`Investigation<chemtrayzer.engine.investigation.Investigation>` class
is relevant and everything else can be considered technical details
"""
from __future__ import annotations

import functools
import logging
import pickle
import traceback
from abc import ABC
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import (Callable, ContextManager, Iterable, List, Mapping, Optional, Set,
                    Tuple, Type, Union)
import warnings

from chemtrayzer.engine._event import Event, EventDispatcher, Listener
from chemtrayzer.engine.errors import ProgrammingError
from chemtrayzer.engine.jobsystem import (Job, _JobFinishedEvent,
                                          JobSystem)
from chemtrayzer.engine._serialization import PickyPickler, PickyUnpickler
from chemtrayzer.engine._submittable import Submittable, State, Failure

class DependencyFailure(Failure):
    r"""indicates that an investigation failed because a job or an other investigation it waited for failed

    .. note:: This is different from the :class:`DependencyError` which is
              raised when an investigation is submitted that has a dependency
              that is not met.

    :param msg: message used in logging
    :param dependencies: list of other failed investigations or jobs. Their
                        failure reasons will be extracted and put into the
                        causes list of this failure
    :param causes: list of failures that caused the current failure. Strings will
                   be converted to Failure objects.
    :ivar submittable_id: identifier of the submittable that failed. Will be set
                         by the fail() method of the submittable
    :ivar causes: list of causes for the failure
    :vartype causes: List[Reason|Exception]

    """

    def __init__(self, msg: str = None, *,
                 failed: Iterable[Submittable]|Submittable = None,
                 causes: Failure|str|Exception|Iterable[Failure|Exception|str]
                        = None,
                **kwargs) -> None:
        if failed is not None:
            if isinstance(failed, Submittable):
                    failed = [failed]

            if causes is None:
                causes = [dep.result.reason for dep in failed]
            elif isinstance(causes, (str, Exception, Failure)):
                causes = [causes] + [dep.result.reason for dep in failed]
            else: # assume causes is iterable of valid causes
                causes = [cause for cause in causes] + \
                        [dep.result.reason for dep in failed]

        super().__init__(msg, causes=causes, **kwargs)

class _InvestigationStateChanged(Event):
    ''' Triggered by an investigation on itself, when its state changes '''

    def __init__(self, inves: Investigation, new_state: State)\
            -> None:
        self.investigation = inves
        self.inves_id = inves.id

        if inves.id is None:
            raise ValueError('Investigation needs an id to define the event')

        super().__init__(self.gen_spec(inves.id, new_state))

    @classmethod
    def gen_spec(cls, inves_id: int, new_state: State):
        ''' generates the specification string for a given investigation id and
        expected state.
        '''
        return f'{inves_id:d}:{new_state}'

class InvestigationError(Exception):
    '''Base class for all investigation related exceptions'''

class DependencyError(InvestigationError):
    '''Raised when the dependencies of an investigation are not met.'''

def _ensure_submission(method):
    '''decorator that checks if the investigation's id was set

    :raises: ProgrammingErro if id was not set on the call'''

    @functools.wraps(method)
    def wrapper(self: Investigation, *args, **kwargs):
        if self.id is None:
            raise ProgrammingError(f'{method.__name__}() was called before the '
                                   'investigation was submitted. You cannot '
                                   'submit jobs/investigations in the'
                                   ' constructor.')

        return method(self, *args, **kwargs)

    return wrapper

class Investigation(ABC, Submittable):
    '''
    Abstract investigation. To implement your own investigation simply inherit
    from this class, add the first step in the __init__ function and call
    start.

    :param context: the context in which the investigation is run
                    deprecated: the context is now set on submission
    :param id: unique id of this investigation (usually set by the investgaiton
               manager). The id can e.g. be used to register for an event
               that is triggered when the state of this specific investigation
               changes
    :param target: string describing what the investigation is looking for in a
                   reproducible way (e.g. a species id); used for searching/
                   filtering investigaitons
    :ivar result: Investigations will put information in this member
                   variable after finishing.
    :ivar state: current state of the investigation.
    '''

    DEPENDENCIES = {}
    _LOG_TEMPLATE = 'investigation ${id}: ${msg}'
    _LOG_TEMPLATE_NO_ID = 'invesitgation (no id):${msg}'

    def __init__(self,
                 context: Optional[InvestigationContext] = None,
                 target: Optional[str] = None):
        super().__init__()

        # contains the types of waitables (Job or Investigation) and ids
        # that this investigation is waiting for
        self.__waiting_for: List[Tuple[type, int]] = []

        # stores function handles that are called upon calling start()/update()
        self.__steps = []
        self.__n_steps_executed = 0

        if context is not None:
            warnings.warn(
                'The investigation context does not need to be provided at'
                ' creation time, anymore. This functionality will be removed '
                'in the future', DeprecationWarning, stacklevel=2)
        # usually set by Investigation manager on submission
        self.context: InvestigationContext = context

        self._dispatcher = EventDispatcher()

        self._target: str = target

    def _set_state_hook(self, current: State, new: State):
        if current != new:
            self._dispatcher.trigger(_InvestigationStateChanged(self, new))

    @property
    def target(self) -> str:
        return self._target

    @target.setter
    def target(self, val: str):
        if self._state == State.PENDING:
            self._target = val
        else:
            raise AttributeError('target can only be changed before submission')

    def tell_next_step(self) -> str:
        '''
        :return: method name of the step that will be executed next or
                 an empty string if no step is to be executed next.
        '''

        if len(self.__steps) == 0:
            return ''
        else:
            return self.__steps[0].__name__

    def run_next_step(self):
        '''Executes the next step'''
        if len(self.__steps) == 0:
            raise ProgrammingError('No next step to run.')

        # get all arguemts from their ids
        # arguements to the call of the next step
        args = []
        # loop over __waiting_for because it contains the correct order
        for cls, id in self.__waiting_for:
            if cls == Investigation:
                job_inves = self.context.inves_mgr.get_investigation_by_id(id)
            elif cls == Job:
                job_inves = self.context.jobsystem.get_job_by_id(id)
            else: # sanity check
                raise RuntimeError('Something went horribly wrong :(')

            # since the queue keeps track of what is waiting for what, this
            # just serves as a sanity check:
            if not job_inves.is_finished:
                raise InvestigationError('run_next_step() was called before all'
                                         ' jobs/other investigations that were '
                                         'waited for finished.')

            args.append(job_inves)
        self.__waiting_for = []

        step_name = self.tell_next_step()

        self._logger.debug('Executing step %d "%s"', self.__n_steps_executed,
                            self.tell_next_step())
        next_step = self.__steps.pop(0)

        try:
            next_step(*args)

        except Exception as err:
            if self.context.fail_deadly:
                raise
            else:
                err_tb = ''.join(traceback.format_exception(
                                                type(err),
                                                err,
                                                err.__traceback__))
                self._logger.error(
                    'Investigation failed because an error occured while '
                    'executing step "%s".\n%s', step_name, err_tb)

                self.fail(reason=err)
        else:
            self._logger.debug('Finished step %d', self.__n_steps_executed)
            self.__n_steps_executed += 1

            if len(self.__steps) == 0:
                if self.result is None:
                    self._logger.warning('Investigation finished but its '
                    'result variable was not set!')

                # to make it easier to debug for Investigation developers
                if not self.is_finished:
                    raise ProgrammingError('Investigation finished (no steps '
                    'left), but its state is still set to "running". State '
                    'should be "failed" or "successful".')

    def __get_waitable_type(self, job_or_inves: Union[Job, Investigation])\
            -> Type[Union[Job, Investigation]]:
        if isinstance(job_or_inves, Job):
            obs_type = Job
        elif isinstance(job_or_inves, Investigation):
            obs_type = Investigation
        else:
            raise TypeError('object must be either a job or an investigaiton')

        return obs_type

    @_ensure_submission
    def wait_for_and_submit(self, waitable : Union[Job, Investigation]):
        '''
        Shortcut method to submit a job or another investigation and register
        the investigation to wait for the waitable to finish.

        :param waitable: job or other investigation for which this
                           investigation should wait
        :return: id assigned to the submitted job or investigation
        '''
        if isinstance(waitable, Investigation):
            id = self.context.inves_mgr.submit(waitable)
        elif isinstance(waitable, Job):
            id = self.context.jobsystem.submit(waitable)
        else:
            raise ProgrammingError('wait_for_and_submit() can only be called '
                                   'with jobs and investigations')

        self.wait_for(waitable)

        return id

    @_ensure_submission
    def wait_for(self, waitable: Union[Job, Investigation]):
        '''register self to wait for a job or another investigation to finish.

        :param waitable: job or other investigaiton
        '''
        self.context.inves_mgr.queue.wait_for(self, waitable)
        self.__waiting_for.append((self.__get_waitable_type(waitable),
                                   waitable.id))

    def add_step(self, step : Callable):
        '''
        Add the function that should be called next, i.e. when start() or
        update() is called.

        :param step: member function of the investigation
        '''
        if (not hasattr(step, '__call__')
            or not hasattr(step, '__self__')
            or not step.__self__ == self):
            raise ProgrammingError(
                '"step" needs to be a member function.\nRemember to pass '
                'the function handle to add_step(). Do not call the function '
                'and pass its result.')

        self.__steps =  self.__steps + [step]

    def __repr__(self) -> str:
        return f'<{type(self).__name__} id={self.id}>'

class BatchInvestigation(Investigation):
    """
    Submit a bunch of jobs or investigations simultaneously.

    This investigation submits a list of investigations or jobs and harvests
    their results. Optionally, the results can be pickled. This investigation
    succeeds, if all investigations or jobs are successful. Otherwise, it fails.
    :ivar inves_and_job_list: list of investigations or jobs
    :ivar pickle_results: whether to pickle the results
    :type pickle_results: bool, optional
    :ivar pickle_path: path to pickle the results
    :type pickle_path: Path, optional
    :ivar result: result of the investigation
    :type result: BatchInvestigation.Result
    """
    inves_and_job_list: Iterable[Submittable]
    pickle_results: bool
    pickle_path: Optional[Path]

    @dataclass
    class Result(Submittable.Result):
        """
        :ivar results_list: list of all investigations results
        :type results_list: List[Investigation.Result], optional
        :ivar success_list: indicates success or failure of each investigation
                            or job
        """
        results_list: List[Submittable.Result] = field(default_factory=list)
        success_list: List[bool] = field(default_factory=list)

    def __init__(
        self,
        inves_and_job_list: Iterable[Submittable],
        pickle_results: bool = False,
        pickle_path: Path = None,
    ) -> None:

        super().__init__()
        self.inves_and_job_list = inves_and_job_list

        if pickle_results is True and pickle_path is None:
            raise ValueError('pickle_results is True but no pickle_path is '
                             'provided.')
        elif pickle_results is True:
            self.pickle_results = True
            self.pickle_path = Path(pickle_path)
        else:
            self.pickle_results = False

        self.result = BatchInvestigation.Result()
        self.add_step(self.submit)

    def submit(self):
        for inves_or_job in self.inves_and_job_list:
            self.wait_for_and_submit(inves_or_job)

        self.add_step(self.harvest_results)
        self._logger.debug(
            f"BatchInvestigation: {len(self.inves_and_job_list)} "
            "Job(s)/Investigation(s) have been submitted.")

    def harvest_results(self, *submitted):
        for submittable in submitted:
            self.result.results_list.append(submittable.result)
            if submittable.is_successful is True:
                self.result.success_list.append(True)
            elif submittable.is_failed is True:
                self.result.success_list.append(False)

            # The investigation engine ensures that a finished job is either
            # successful or failed. Therefore, the following else statement
            # should never be reached.
            else:
                raise InvestigationError(
                    'Investigation is neither successful nor failed.')

        if self.pickle_results is True:
            with open(self.pickle_path, 'wb') as pickle_db:
                pickle.dump(self.result.results_list, pickle_db, pickle.HIGHEST_PROTOCOL)
                self._logger.debug(f'Result of {self.__class__.__name__} '
                                   f'saved in {self.pickle_path}.')

        if all(self.result.success_list) is True:
            self.succeed()
        else:
            failed_ids_str = ', '.join(
                [str(submitted[i].id)
                 for i, is_success in enumerate(self.result.success_list)
                 if not is_success])
            self.fail(f'Investigations {failed_ids_str} failed.')

# nodes are stored in sets and dicts which need to hash them -> freeze
@dataclass(frozen=True)
class _Node:
    '''a node in the graph representing the blocker-blockee relationships'''
    type: Type[Union[Job, Investigation]]
    id: int

class _InvestigationQueue(Listener):
    '''Keeps track of what each investigation is waiting for.

    Internally, it tracks what job/investigation is blocking other
    investigations, i.e. those that are waiting, by maintaining a directed graph
    containing the blocker-"blockee" relationship. Similar to Kahn's algorithm
    for topolocial sorting, the class also keeps track of those nodes that are
    not blocked.

    You can loop over the queue to get the next investigation that is not
    waiting for anything until no more "unblocked" investigations are available:

    .. code::

        # execute steps until all investigations wait for something or until
        # there are no more investigations
        for inves in queue:
            inves.run_next_step()
    '''

    def __init__(self, mgr: 'InvestigationManager') -> None:
        super().__init__()

        self.mgr = mgr
        self._not_blocked: Set[int] = set()
        '''ids of investigations that are not waiting on anything'''

        # used for storing the blocker-blockee graph
        self._graph: Mapping[_Node, Set[_Node]] = {}

        # although EventDispatcher is a singleton, using the same variable
        # everywhere allows for future changes
        self.__dispatcher = EventDispatcher()

    def update(self, event: Event):
        '''receives events about finished jobs/investigations and updates the queue accordingly'''

        # determine type
        if isinstance(event, _JobFinishedEvent):
            node = _Node(Job, event.job_id)
            self._unsubscribe_from_job(event.job_id)

        elif isinstance(event, _InvestigationStateChanged):
            node = _Node(Investigation, event.inves_id)
            self._unsubscribe_from_inves(event.inves_id)

            self._not_blocked.discard(event.inves_id)
        else:
            raise TypeError(f'Unexpected event: {event}')

        previously_blocked = self._remove_free_node(node)

        # check if an investigation is now unblocked
        for node in previously_blocked:
            if node.type == Investigation and self._is_free(node):
                self._not_blocked.add(node.id)

        # now with the updated blocking graph, we try to run more steps
        self.mgr.run()

    def wait_for(self, inves: Investigation,
                 blocker: Union[Job, Investigation]):
        '''define that an investigation is waiting for something (a blocker)'''
        assert inves.id is not None and blocker.id is not None

        if isinstance(blocker, Investigation):
            blocker_node = _Node(Investigation, blocker.id)
            self._subscribe_to_inves(blocker.id)

            # if the blocking investigation is new, we need to add it to the
            # list
            if self._is_free(blocker_node):
                self._not_blocked.add(blocker_node.id)
        elif isinstance(blocker, Job):
            blocker_node = _Node(Job, blocker.id)
            self._subscribe_to_job(blocker.id)
        else:
            raise TypeError(f'Unsupported type for blocker: {type(blocker)}.')

        # the blocked investigation (blockee) has to be removed from
        # _not_blocked, if present
        self._not_blocked.discard(inves.id)

        blockee_node = _Node(Investigation, inves.id)
        self._connect(blocker_node, blockee_node)

    def add_investigation(self, inves: Investigation):
        '''add an investigation to the queue'''
        node = _Node(Investigation, inves.id)

        # if the investigation were already done, it would never be removed and
        # lead to an infinite loop
        assert not inves.is_finished
        # by checking if the investigation is not already in the graph, we can
        # make sure that it is not already waiting on something
        assert node not in self._graph

        self._not_blocked.add(inves.id)
        self._subscribe_to_inves(inves.id)

        self._add_node(node)

    def _add_node(self, node: _Node):
        if node not in self._graph:
            self._graph[node] = set()

    def _connect(self, start: _Node, end: _Node):
        self._add_node(start)
        self._add_node(end)

        # avoid cyclic dependencies (which would block everything) by checking
        # that end is not connected to start with a breadth-first search
        current_nodes = {end}
        next_nodes = set()
        while True:
            for current_node in current_nodes:
                if current_node == start:
                    raise ProgrammingError(
                        'Cyclic dependency detected while making '
                        f'Investigation {end.id} wait for Investigation '
                        f'{start.id}: Investigation {start.id} already '
                        f'(indirectly) waits for {end.id}.')
                assert current_node != start

                next_nodes.update(self._graph[current_node])

            # current nodes are not connected to anything else -> leave
            if not next_nodes:
                break

            current_nodes = next_nodes
            next_nodes = set()

        self._graph[start].add(end)

    def _remove_free_node(self, node: _Node):
        '''allows you to remove nodes without an incoming edge

        :return: those other nodes that had incoming edges from node'''
        if not self._is_free(node):
            raise ProgrammingError('Investigation finished,'
                    ' but it is still waiting for other investigations '
                    'or jobs to finish.')

        points_to = self._graph[node]

        del self._graph[node]

        return points_to

    def _is_free(self, node: _Node) -> bool:
        ''':return: True, if node has no incoming edge'''
        for start, end in self._graph.items():
            if node in end:
                return False

        return True

    def _subscribe_to_job(self, job_id: int):
        '''subscribe to the event triggered when the job is done'''
        self.__dispatcher.register_listener(
                                    listener=self,
                                    event_type=_JobFinishedEvent,
                                    spec=_JobFinishedEvent.gen_spec(job_id))

    def _unsubscribe_from_job(self, job_id: int):
        '''stop listening for the event triggered when the job finishes'''
        self.__dispatcher.deregister_listener(
                                    listener=self,
                                    event_type=_JobFinishedEvent,
                                    spec=_JobFinishedEvent.gen_spec(job_id))

    def _subscribe_to_inves(self, inves_id: int):
        '''subscribe to events triggered when an investigaiton finishes'''
        self.__dispatcher.register_listener(
                                    listener=self,
                                    event_type=_InvestigationStateChanged,
                                    spec=_InvestigationStateChanged.gen_spec(
                                            inves_id,
                                            State.FAILED))
        self.__dispatcher.register_listener(
                                    listener=self,
                                    event_type=_InvestigationStateChanged,
                                    spec=_InvestigationStateChanged.gen_spec(
                                            inves_id,
                                            State.SUCCESSFUL))

    def _unsubscribe_from_inves(self, inves_id: int):
        '''remove subscription from InvestigationStateChanged events'''
        # deregister both events that the investigation manager subscribed
        # this investigation to
        self.__dispatcher.deregister_listener(
                                    listener=self,
                                    event_type=_InvestigationStateChanged,
                                    spec=_InvestigationStateChanged.gen_spec(
                                            inves_id,
                                            State.FAILED))
        self.__dispatcher.deregister_listener(
                                    listener=self,
                                    event_type=_InvestigationStateChanged,
                                    spec=_InvestigationStateChanged.gen_spec(
                                            inves_id,
                                            State.SUCCESSFUL))

    def __iter__(self):
        return self

    def __next__(self) -> int:
        # Keep returning objects from the list of not blocked investigations.
        # Create a new iterator over _not_blocked each call because is may
        # change between calls to __next__, e.g. when a new investigation is
        # added.
        return next(iter(self._not_blocked))

class InvestigationManager():
    '''
    Helper class that keeps track of all investigations and manages their
    execution. Each investigation is assigned a unique id when it is submitted.
    '''

    def __init__(self, context: 'InvestigationContext') -> None:
        self._investigations: List[Investigation] = []
        self.queue = _InvestigationQueue(self)
        self.context = context

        self._dispatcher = EventDispatcher()

        self._running = False

    def submit(self, inves: Investigation) -> int:
        '''
        start an investigation

        .. note:: The investigation may finish before submit() returns

        :param inves: investigation object to start
        :return: id of the investigation
        '''
        if inves.is_running or inves.is_finished:
            raise ProgrammingError('Investigation has already been started.')

        inves_id = self._determine_next_inves_id()
        inves.id = inves_id
        inves._state = State.RUNNING

        inves.context = self.context
        # raises an error if there is no species_db
        self.context.check_dependencies(inves.DEPENDENCIES)

        # append before starting, b/c the investigaiton may submit the next
        # investigation in the first step
        self._investigations.append(inves)
        self.queue.add_investigation(inves)

        self.run()

        return inves_id

    def run(self):
        '''run those investigations that are not waiting on
        anything. If the manager is already running this functions does nothing.
        '''
        # start may be called when an investigation submits another investig.
        # during execution, so we ignore any calls while it is running
        if self._running:
            return

        try:
            self._running = True

            for not_waiting in self.queue:
                inves = self.get_investigation_by_id(not_waiting)
                inves.run_next_step()
        finally:
            self._running = False

    def _determine_next_inves_id(self) -> int:
        '''get the id of the next investigaiton that is started'''
        return len(self._investigations)

    def _save_investigation(self, inves):
        '''stores a newly submitted investigaiton'''
        self._investigations.append(inves)

    @property
    def n_investigations(self):
        ''' the number of investigations that were submitted '''
        return len(self._investigations)

    def list_investigations(self) -> List[int]:
        ''':return: a list of all investigation ids '''
        return [i for i in range(self.n_investigations)]

    def get_investigations(self) -> List[Investigation]:
        ''':return: list of all investigations'''
        return [inves for inves in self._investigations]

    def get_investigation_by_id(self, id: int) -> Investigation:
        '''
        :param id: id of investigation to retrieve
        :return: investigation with id or None
        '''
        try:
            return self._investigations[id]
        except IndexError:
            return None

    def get_investigation_by_target(self, target: str,
                                    inves_type: Type[Investigation] = None)\
                                    -> List[Investigation]:
        '''
        :param target: target of the investigation
        :return: list of investigations with the correct type and the defined
                 target
        '''
        if inves_type is None:
            return [inves
                    for inves in self._investigations
                    if inves.target == target]
        else:
            return [inves
                    for inves in self._investigations
                    if inves.target == target and isinstance(inves, inves_type)]

class InvestigationContext():
    '''
    Investigations typically depend on several context managers like
    databases or a job system. This class collects all these context managers
    and the investigation manager and provides a single interface.
    It is a context manager itself.

    When in the context the values returned by the
    contextmanagers' __enter__ funnctions of all contextmanagers supplied to
    the constructor are accessible through this object.

    Furthermore, the investigation context provides an investigation manager
    which can be used to submit investigations. All submitted investigations
    are saved on disk when the context is exited.

    .. code::

        context = InvestigationContext('inves_file.pickle', jobsystem=sys,
            context_mgrs={'species_db':my_db})

        with context:
            # now we can access the contexts as members
            context['species_db'].load_geometry(geo_id)

    :arg path: path to which the submitted investigations are saved
    :param jobsystem: job system that the investigation should use to submit jobs
    :param inves_mgr: investigation manager that the investigation should use to
                      submit other investigations
    :param context_mgrs: map of context managers that an investigation can use.
                         They will be opened when the investigation context is
                         opened.
    :param fail_deadly: if True, errors are not caught during execution of an
                        investigation. Otherwise, errors will be caught and the
                        investigation will fail with an
                        :class:`ErrorCausedFailure` reason
    '''

    def __init__(self, path, *, jobsystem: JobSystem,
            context_mgrs: Mapping[str, ContextManager] = None,
            fail_deadly: bool = False) -> None:
        # reserve names with underscores for (future) internal functionality
        if context_mgrs is not None:
            for name in context_mgrs.keys():
                if name.startswith('__') and name.endswith('__'):
                    raise ValueError('Names starting and ending with a double '
                                    'underscore are reservered.')
        self.__path = Path(path)

        if not self.__path.exists() and not self.__path.parent.exists():
            raise FileNotFoundError('Parent directory of investigation file '
                                    f'"{self.__path}" does not exist.')

        # investigation manager and event dispatcher will be created/unpickled
        # after all contexts are dopened
        self.inves_mgr : InvestigationManager = None
        self._dispatcher = EventDispatcher()
        self.jobsystem = jobsystem
        self.fail_deadly = fail_deadly

        # add jobsystem to list of mgrs so it will be opened in __enter__()
        if context_mgrs is not None:
            self._context_managers = {
                '__jobsystem__': jobsystem,
                **context_mgrs
            }
        else:
            self._context_managers = {'__jobsystem__': jobsystem }

        self._stack = ExitStack()

        self._targets = {}


    def __enter__(self) -> 'InvestigationContext':
        self._stack.__enter__()

        # if an error occurs while entering the context mgrs, we close all
        # and always reraise (even if one context mgr. would supress the error)
        try:
            self._targets = {name: self._stack.enter_context(cm)
                             for name, cm in self._context_managers.items()}

            self.__load_and_register()
        except Exception:
            self._stack.close()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # check exception type to avoid catching the SystemExit exception
        if isinstance(exc_type, Exception):
            path = self.__path.with_suffix('.backup')
            self.__save_and_deregister(path)
            logging.error(
                'An exception occured in the investigation context. '
                'Changes in the investigations since opening the context were '
                'saved to %s.',
                path)
        else:
            self.__save_and_deregister(self.__path)

        self._targets = {}
        return self._stack.__exit__(exc_type, exc_value, traceback)

    def __getitem__(self, context_mgr_name):
        return self._targets[context_mgr_name]

    def __load_and_register(self):
        '''
        loads the investigation manager from file or creates a new one and
        resubscribe the invesitgation queue to all events
        '''
        if self.__path.exists():
            logging.debug('Loading investigations from disk...')

            with open(self.__path, mode='rb') as file:
                unpickler = PickyUnpickler(file,
                                           sep_objs={
                                               '__context__': self,
                                               **self._context_managers
                                           })

                self.inves_mgr, events = unpickler.load()

                for event in events:
                    event_type, spec = event
                    self._dispatcher.register_listener(
                                        listener=self.inves_mgr.queue,
                                        event_type=event_type, spec=spec)
        else:
            logging.debug('No investigations found (File "%s" does not exist). '
                          'Creating a new '
                          'investigation manager and event dispatcher...',
                          self.__path)
            self.inves_mgr = InvestigationManager(context=self)

    def __save_and_deregister(self, path):
        '''
        save the investigation manager and events to a file and unsubscribes
        the investigation queue from all events
        '''
        with open(path, mode='bw') as file:
            pickler = PickyPickler(file,
                                   sep_objs={'__context__': self,
                                             **self._context_managers})

            events = self._dispatcher.deregister_listener(
                                            listener=self.inves_mgr.queue)

            # The investigation manager and the events dictionary contain
            # references to the investigation objects. By pickling them as a
            # single tuple, the pickle module will figure out which
            # investigations are the same object and store them as such.
            # Also, the investigations contain references to the investigation
            # manager which pickle will also deal with correctly
            pickler.dump((self.inves_mgr, events))

    def check_dependencies(self, dependencies: Mapping[str, type]):
        '''
        checks if this context contains all dependencies with the correct name.
        Usually called by an investigaiton.

        :param dependencies: a map of the types of all the context managers an
                             investigation needs accessible by the names that
                             the investigation expects
        :raise: DependencyError if at least one dependency is not met.
        '''

        for name, mgr_type in dependencies.items():
            if name not in self._context_managers:
                raise DependencyError(f'Dependency cannot be satisfied: The '
                    'investigation context is missing a context manager of type'
                    f' {mgr_type.__name__} with name  "{name}".')

            actual_type = type(self._context_managers[name])
            if actual_type != mgr_type:
                raise DependencyError(f'Context manager "{name}" has wrong '
                    f'type: {actual_type}. Expected: {mgr_type}.')