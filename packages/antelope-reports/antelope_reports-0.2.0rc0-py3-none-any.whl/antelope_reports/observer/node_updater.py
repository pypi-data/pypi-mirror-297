"""
The Upgrade Manager is a bit too heavy-handed and it violates some good design principles.

This tool is meant to perform an update of a single node in a few different ways.
"""
from antelope import enum


class NodeUpdater:
    _strategy = 'match_name_and_spatial_scope'

    _strategies = ('match_name_and_spatial_scope',
                   'match_name',
                   'same_id',
                   'targets',
                   'node_targets')

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        if value is not None:
            if value in self._strategies:
                print('setting strategy "%s"' % value)
                self._strategy = value
            else:
                print('ignoring unrecognized strategy "%s"' % value)

    def __init__(self, branch, query, strategy=None):
        """
        This accepts a single FragmentBranch, which includes a node (FragmentRef) and an anchor (Anchor), with
        a scenario name.  This branch is SUPPOSED to represent an existing termination.
        :param branch:
        :param query: used to obtain upgrade targets
        """
        self._branch = branch
        self._q = query
        self.strategy = strategy
        self._candidates = self._exception = self._rx = self._rxs = None

    @property
    def current(self):
        return self._branch

    """
    different upgrade strategies
    """
    def match_name(self):
        """
        Match the name of the current anchor
        :return:
        """
        return self._q.processes(name='^%s$' % self.current.anchor.term_node['name'])

    def match_name_and_spatial_scope(self):
        """
        Match the name and spatial scope of the current anchor
        :return:
        """
        return self._q.processes(name='^%s$' % self.current.anchor.term_node['name'],
                                 spatialscope='^%s$' % self.current.anchor.term_node['spatialscope'])

    def same_id(self):
        """
        Retrieve the process with the same external_ref from a different query
        :return:
        """
        return [self._q.get(self.current.anchor.term_node.external_ref)]

    def targets(self):
        """
        Retrieve targets that match the current anchor (flow and direction)
        :return:
        """
        return self._q.targets(self.current.anchor.term_flow, direction=self.current.anchor.direction)

    def node_targets(self):
        """
        Retrieve targets that match the current node (flow, disregarding direction)
        :return:
        """
        return self._q.targets(self.current.node.flow)

    def _run_attempt(self, strategy):
        """
        :return:
        """
        if strategy is None:
            strategy = self.strategy
        self._candidates = enum(getattr(self, strategy)())

