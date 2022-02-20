from copy import deepcopy


class GraphException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Graph:
    """An undirected graph, represented as a map,
    one from each vertex to the set of neighbours"""

    def __init__(self, n):
        """Creates a graph with n vertices (numbered from 0 to n-1)
        and no edges"""
        self._dict = {}
        for i in range(n):
            self._dict[i] = []

        # Mark all the vertices as not visited
        self._visited = None

    def get_number_vertices(self):
        """Returns the number of vertices"""
        return len(self._dict.keys())

    def parse_vertices(self):
        """Returns an iterable containing all the vertices"""
        return iter(self._dict.keys())

    def is_edge(self, x, y):
        """Returns True if there is an edge from x to y, False otherwise
        Condition: x and y must be valid vertices, else raise exception"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if y in self._dict[x]:
            return True
        else:
            return False

    def degree(self, x):
        """Returns the out degree of a specified vertex
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return len(self._dict[x])

    def parse_vertex(self, x):
        """Returns an iterable containing the neighbours of x
        Condition: x must be a valid vertex, else raise exception"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        return iter(self._dict[x])

    def add_edge(self, x, y):
        """Adds an edge from x to y.
        Conditions: x, y must be valid vertices and the edge must not exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if self.is_edge(x, y):
            raise GraphException("!!! The edge already exists")

        self._dict[x].append(y)
        self._dict[y].append(x)

    def add_edge_no_condition(self, x, y):
        """
        Adds an edge from x to y. We assume the input is correct. We use it for reading from a file
        """
        self._dict[x].append(y)
        self._dict[y].append(x)

    def remove_edge(self, x, y):
        """Removes an edge from x to y.
        Conditions: x, y must be valid vertices and the edge must exist"""
        if x not in self.parse_vertices() or y not in self.parse_vertices():
            raise GraphException("!!! Invalid vertex")
        if not self.is_edge(x, y):
            raise GraphException("!!! The edge does not exist")

        self._dict[x].remove(y)
        self._dict[y].remove(x)

    def add_vertex(self, x):
        """Add vertex.
        Condition: the vertex must not exist and must be valid(non-negative)"""
        if x in self.parse_vertices():
            raise GraphException("!!! Vertex already exists")
        if x < 0:
            raise GraphException("!!! Invalid vertex")
        self._dict[x] = []

    def remove_vertex(self, x):
        """Remove vertex.
        Condition: the vertex must exist"""
        if x not in self.parse_vertices():
            raise GraphException("!!! Vertex does not exist")

        # remove traces from dict
        for vertex in self._dict[x]:
            self._dict[vertex].remove(x)

        # remove dict
        del self._dict[x]

    def copy_graph(self):
        """Makes a copy of the graph"""
        return deepcopy(self)

    def connected_components(self):
        """
        Returns a list with the connected components.
        """
        cc = []
        self._visited = []
        for v in self.parse_vertices():
            if v not in self._visited:
                # if not visited => we found a connected component
                bfs = self.BFS(v)
                cc.append(bfs)
                self._visited.extend(bfs.parse_vertices())
        return cc

    def BFS(self, s):
        """Returns the set of vertices of the graph g that are accessible
            from the vertex s"""

        # Connected components list
        cc = list()
        cc.append(s)

        # create graph object
        graph = Graph(0)
        graph.add_vertex(s)

        # Queue
        queue = [s]

        # Start going through the queue
        while len(queue) > 0:
            x = queue[0]  # get elem from queue
            queue = queue[1:]
            for y in self.parse_vertex(x):
                if y not in cc:  # if it's not visited, add the vertex to queue anc connected component's elem
                    graph.add_vertex(y)
                    cc.append(y)
                    queue.append(y)
                try:
                    graph.add_edge(x, y)
                except GraphException:
                    pass
        return graph

    def print_dict(self):
        """ Additional function, role: to see if other functions are working.
        Prints all 3 dictionaries.
        """
        print(self._dict, "\n")

    def __repr__(self):
        return str(self)

    def __str__(self):
        vertices = self.parse_vertices()
        edges = []
        result = ''
        for vertex in vertices:
            # get the list of outbound edges
            vertices_out = list(self.parse_vertex(vertex))

            # check if it's isolated
            if len(vertices_out) == 0:
                result += str(vertex) + "\n"
                continue

            # if it's not isolated
            for vertex_out in vertices_out:
                edge = (min(vertex, vertex_out), max(vertex, vertex_out))
                if edge not in edges:
                    result += str(edge[0]) + " " + str(edge[1]) + "\n"
                    edges.append(edge)
        return result
