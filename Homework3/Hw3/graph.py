from copy import deepcopy
import math


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

    def print_path(self, P, d):
        if P[d] != -1:  # if parent exists
            self.print_path(P, P[d])
        print(d, end=" ")

    def matrix_multiplication(self, D, A, P):
        nrV = self.get_number_vertices()
        for i in range(nrV):
            for j in range(nrV):
                for k in range(nrV):
                    # if we found a vertex between i and j and the 2 edges summed have a lowe cost than the edge (i,j)
                    # save it. Also save the vertex between i and j in the parent matrix
                    if D[i][k] + A[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + A[k][j]
                        P[i][j] = k

        # return matrix of cost
        return D

    def find_cost_matrix(self):
        nrV = self.get_number_vertices()
        A = [[math.inf for i in range(nrV)] for j in range(nrV)]  # matrix
        P = [[-1 for i in range(nrV)] for j in range(nrV)]  # parent matrix
        steps = []  # save steps

        # the matrix has initially 0 diagonally, the cost where is an edge, or infinite if there is not an edge
        for i in range(nrV):
            for j in range(nrV):
                if i == j:
                    A[i][j] = 0
                elif self.is_edge(i, j):
                    A[i][j] = self._dictCost[(i, j)]
                    P[i][j] = i
        D = deepcopy(A)
        steps.append(deepcopy(D))

        # start the algorithm
        for m in range(2, nrV):
            D = self.matrix_multiplication(D, A, P)
            steps.append(deepcopy(D))

        # return matrix of costs, parent matrix and the steps
        return D, P, steps
