from copy import deepcopy
from collections import deque


class GraphException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Graph:
    """A directed graph, represented as two maps,
    one from each vertex to the set of outbound neighbours,
    the other from each vertex to the set of inbound neighbours"""

    def __init__(self, n):
        """Creates a graph with n vertices (numbered from 0 to n-1)
        and no edges"""
        self._dictOut = {}
        self._dictIn = {}
        self._dictCost = {}
        self.duration = [] * n  # the duration of activity i
        self.tmb = [-999999] * n  # the earliest time when activity i begins
        self.tme = [-999999] * n  # the earliest time when activity i ends
        self.TMB = [999999] * n  # the time at the latest when activity i begins
        self.TME = [999999] * n  # the time at the latest when activity i ends
        for i in range(n):
            self._dictOut[i] = []
            self._dictIn[i] = []

    def get_number_vertices(self):
        """Returns the number of vertices"""
        return len(self._dictOut.keys())

    def parse_vertices(self):
        """Returns an iterable containing all the vertices"""
        return iter(self._dictOut.keys())

    def is_edge(self, x, y):
        """Returns True if there is an edge from x to y, False otherwise
        Condition: x and y must be valid vertices, else raise exception"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if y in self._dictOut[x]:
            return True
        else:
            return False

    def out_degree(self, x):
        """Returns the out degree of a specified vertex
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return len(self._dictOut[x])

    def parse_vertex_out(self, x):
        """Returns an iterable containing the outbound neighbours of x
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return iter(self._dictOut[x])

    def in_degree(self, x):
        """Returns the in degree of a specified vertex
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return len(self._dictIn[x])

    def parse_vertex_in(self, x):
        """Returns an iterable containing the inbound neighbours of x
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return iter(self._dictIn[x])

    def get_cost(self, x, y):
        """Get the cost of the edge
        Conditions: x, y must be valid vertices and the edge must exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if not self.is_edge(x, y):
            raise GraphException("!!! The edge does not exist")
        return self._dictCost[(x, y)]

    def modify_cost(self, x, y, v):
        """Modify the cost of an edge
        Conditions: x, y must be valid vertices and the edge must exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if not self.is_edge(x, y):
            raise GraphException("!!! The edge does not exist")
        self._dictCost[(x, y)] = v

    def add_edge(self, x, y, c):
        """Adds an edge from x to y.
        Conditions: x, y must be valid vertices and the edge must not exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if self.is_edge(x, y):
            raise GraphException("!!! The edge already exists")

        self._dictOut[x].append(y)
        self._dictIn[y].append(x)
        self._dictCost[(x, y)] = c

    def add_edge_no_condition(self, x, y, c):
        """
        Adds an edge from x to y. We assume the input is correct. We use it for reading from a file
        """
        self._dictOut[x].append(y)
        self._dictIn[y].append(x)
        self._dictCost[(x, y)] = c

    def remove_edge(self, x, y):
        """Removes an edge from x to y.
        Conditions: x, y must be valid vertices and the edge must exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if not self.is_edge(x, y):
            raise GraphException("!!! The edge does not exist")

        self._dictOut[x].remove(y)
        self._dictIn[y].remove(x)
        del self._dictCost[(x, y)]

    def add_vertex(self, x):
        """Add vertex.
        Condition: the vertex must not exist and must be valid(non-negative)"""
        if x in self.parse_vertices():
            raise GraphException("!!! Vertex already exists")
        if x < 0:
            raise GraphException("!!! Invalid vertex")
        self._dictOut[x] = []
        self._dictIn[x] = []

    def remove_vertex(self, x):
        """Remove vertex.
        Condition: the vertex must exist"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Vertex does not exist")

        # remove traces from dictIn and dictCost
        for vertex in self._dictOut[x]:
            self._dictIn[vertex].remove(x)
            del self._dictCost[(x, vertex)]

        # remove traces from dictOut and dictCost
        for vertex in self._dictIn[x]:
            self._dictOut[vertex].remove(x)
            del self._dictCost[(vertex, x)]

        # remove from dictIn
        del self._dictIn[x]

        # remove from dictOut
        del self._dictOut[x]

    def topological_sorting(self):
        """verify if the corresponding graph is a DAG and performs a topological sorting of the
        activities using the algorithm based on predecessor counters"""
        sorted = list()
        queue = deque()
        count = {}
        # see how many inbound edges each vertex has, if they don't have then add it to the queue
        for vertex in self.parse_vertices():
            count[vertex] = self.in_degree(vertex)
            if count[vertex] == 0:
                queue.append(vertex)

        # start algorithm
        # we take a vertex with no predecessors, we put it on the sorted list, and we eliminate it from the graph.
        # Then, we take a vertex with no predecessors from the remaining graph and continue the same way.
        while len(queue) != 0:
            vertex = queue.popleft()
            sorted.append(vertex)
            for y in self.parse_vertex_out(vertex):
                count[y] -= 1
                if count[y] == 0:
                    queue.append(y)

        # this mean we don;t have DAG
        if len(sorted) < self.get_number_vertices():
            sorted = []
        return sorted

    def get_times(self):
        """earliest and the latest starting time for each activity and the total time of the project"""
        sorted_list = self.topological_sorting()
        # earliest time when activity begins and ends
        for x in sorted_list:
            if self.in_degree(x) == 0:
                self.tmb[x] = 0
            else:
                # we check all the inbound vertexes and activity begins when all of them are done(max)
                for y in self.parse_vertex_in(x):
                    self.tmb[x] = max(self.tmb[x], self.tme[y])
            # activity ends = activity begins + duration
            self.tme[x] = self.tmb[x] + self.duration[x]

        # latest time when activity begins and ends
        sorted_list.reverse()
        for x in sorted_list:
            if self.out_degree(x) == 0:
                # TME[X] is the duration of the project
                self.TME[x] = self.tme[sorted_list[0]]
            for y in self.parse_vertex_out(x):
                # we check all the outbound vertexes and activity ends when one of them starts(min)
                self.TME[x] = min(self.TME[x], self.TMB[y])
            # activity begins = activity ends - duration
            self.TMB[x] = self.TME[x] - self.duration[x]

        # return the 4 lists and the duration
        if not sorted_list:
            return -1, -1, -1, -1, -1
        return self.tme, self.tmb, self.TMB, self.TME, self.TME[sorted_list[0]]

    def critical_activities(self):
        """A critical activity has a total time reserve of 0"""
        a = self.get_times()  # just to calculate
        arr = []
        for i in range(self.get_number_vertices()):
            # if latest time when activity begins is also the earliest time => critical activity
            if self.tmb[i] == self.TMB[i]:
                arr.append(i)
        return arr

    def distinct_paths(self, src, dest):
        """Finds the number of distinct paths between 2 vertices"""
        dp = [0] * self.get_number_vertices()
        dp[dest] = 1
        arr = self.topological_sorting()
        if not arr:
            return -1
        for i in reversed(arr):
            for j in self.parse_vertex_out(i):
                dp[i] = dp[i] + dp[j]
        return dp[src]

    def copy_graph(self):
        """Makes a copy of the graph"""
        return deepcopy(self)

    def print_dict(self):
        """ Additional function, role: to see if other functions are working.
        Prints all 3 dictionaries.
        """
        print(self._dictIn, "\n")
        print(self._dictOut, "\n")
        print(self._dictCost, "\n")

    def sort_dictionaries(self):
        """
        Sort dictionary when reading from a modified file
        """
        for i in self._dictIn.keys():  # sort values for each key
            self._dictIn[i].sort()
        self._dictIn = {key: self._dictIn[key] for key in sorted(self._dictIn.keys())}  # sort keys

        for i in self._dictOut.keys():  # sort values for each key
            self._dictOut[i].sort()
        self._dictOut = {key: self._dictOut[key] for key in sorted(self._dictOut.keys())}  # sort keys

        self._dictCost = {key: self._dictCost[key] for key in sorted(self._dictCost.keys())}  # sort keys

    def set_initial_time(self, times):
        self.duration = times
