from BFS_traversal_directed import BFS_traversal_directed
from BFS_traversal_undirected import BFS_traversal_undirected
from DFS_traversal_directed import DFS_traversal_directed
from DFS_traversal_undirected import DFS_traversal_undirected
from BFS_undirected_lowestPath_forwardSearch import BFS_undirected_lowestPath_forwardSearch
from Tarjan import Tarjan

def print_menu():
    print("DACA E undirected, la add edge sunt 2 dictionare, daca e directed atunci un dictionar!!!!"
          "\nBaga debugger ul si modifica in functia respectiva in functie de ce date ai"
          "\nIdk de ce scrie none la sfarsit")
    print("---CONNECTED COMPONENTS---")
    print("1. BFS traversal directed connected components")
    print("2. DFS traversal directed connected components")
    print("3. BFS traversal undirected connected components")
    print("4. DFS traversal undirected connected components")
    print("6. SCC(Strongly-connected components) of a directed graph in O(n+m) (n=no. of vertices, m=no. of arcs)"
          "**TARJAN ALGORITHM, using DFS**")

    print("5. Finds a lowest length path between 2vertices using a forward breadth-first search "
          "from the starting vertex, BFS undirected")


if __name__ == '__main__':
    print_menu()
    command = int(input(">>> "))
    switch = {
        1: BFS_traversal_directed,
        2: DFS_traversal_directed,
        3: BFS_traversal_undirected,
        4: DFS_traversal_undirected,
        5: BFS_undirected_lowestPath_forwardSearch,
        6: Tarjan
    }
    func = switch.get(command)
    print(func())
