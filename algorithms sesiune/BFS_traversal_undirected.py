# Python3 Program to print BFS traversal from a given source vertex. BFS(int s) traverses vertices reachable from s.
from collections import defaultdict
from copy import deepcopy

from prettytable import PrettyTable


# This class represents a directed graph using adjacency list representation
class Graph:
    def __init__(self, nr_vertices):
        self.dict = {}
        for i in range(nr_vertices):
            self.dict[i] = []

        # Mark all the vertices as not visited
        self.visited = [False] * nr_vertices

    # function to add an edge to graph
    def addEdge(self, x, y):
        self.dict[x].append(y)
        self.dict[y].append(x)

    # Function to print a BFS of graph
    def BFS(self, s):
        print(f"call bfs({s})")
        t = PrettyTable(['x', 'y', 'queue', 'acc', 'visited'])

        # Create a queue for BFS
        queue = [s]

        # Mark the source node as
        # visited and enqueue it
        self.visited[s] = True
        acc = [s]

        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print(s, end=" ")
            t.add_row([s, "", deepcopy(queue), deepcopy(acc), deepcopy(self.visited)])
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it

            for i in self.dict[s]:
                if not self.visited[i]:
                    queue.append(i)
                    acc.append(i)
                    self.visited[i] = True
                t.add_row(["", i, deepcopy(queue), deepcopy(acc), deepcopy(self.visited)])
        print("\n")
        print(t)


def BFS_traversal_undirected():
    # Driver code

    # Create a graph given in
    # the above diagram
    nr_vertices = 11
    g = Graph(nr_vertices)
    g.addEdge(0, 6)
    g.addEdge(1, 2)
    g.addEdge(2, 6)
    g.addEdge(2, 4)
    g.addEdge(3, 5)
    g.addEdge(3, 7)
    g.addEdge(3, 10)
    g.addEdge(5, 8)
    g.addEdge(5, 10)
    g.addEdge(7, 10)

    print("\nFollowing is Breadth First Traversal")
    for i in range(nr_vertices):
        if not g.visited[i]:
            print("--Component: ")
            g.BFS(i)
