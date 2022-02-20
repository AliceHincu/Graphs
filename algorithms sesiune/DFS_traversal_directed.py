from collections import defaultdict
from copy import deepcopy
from prettytable import PrettyTable


# This class represents a directed graph using adjacency list representation
class Graph:
    def __init__(self, nr_vertices):
        # default dictionary to store graph
        self.graph = defaultdict(list)
        # Mark all the vertices as not visited
        self.visited = [False] * nr_vertices
        for i in range(nr_vertices):
            self.graph[i] = []

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a DFS of graph
    def DFSUtil(self, parent, v, acc, t):

        # Mark the source node as
        # visited and enqueue it
        acc.append(v)
        # acc = [s]

        print(v, end=" ")
        if parent!=v:
            t.add_row([parent, v, deepcopy(acc), deepcopy(self.visited)])

        for neighbour in self.graph[v]:
            if neighbour not in acc:
                self.visited[neighbour] = True

                self.DFSUtil(v, neighbour, acc, t)

    def DFS(self, v):
        print(f"call dfs({v})")
        self.visited[v] = True
        # Create a set to store visited vertices
        acc = list()
        t = PrettyTable(['parent', 'child', 'acc', 'visited'])
        t.add_row([v, "", deepcopy(acc), deepcopy(self.visited)])
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, v, acc, t)
        print("\n")
        print(t)


def DFS_traversal_directed():
    # Driver code

    # Create a graph given in
    # the above diagram
    nr_vertices = 8
    g = Graph(nr_vertices)
    g.addEdge(1, 4)
    g.addEdge(1, 3)
    g.addEdge(1, 2)
    g.addEdge(2, 3)
    g.addEdge(2, 5)
    g.addEdge(3, 4)
    g.addEdge(3, 5)
    g.addEdge(4, 7)
    g.addEdge(7, 5)
    g.addEdge(6, 2)
    g.addEdge(6, 5)
    g.DFS(1)
    print("\nFollowing is Depth First Traversal")
    """
    for i in range(nr_vertices):
        if not g.visited[i]:
            print("--Component: ")
            g.DFS(i)
"""