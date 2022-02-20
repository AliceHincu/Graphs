import math

from graph import Graph, GraphException
from termcolor import colored
from pathlib import Path
import random


class ConsoleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ConsoleUI:
    def __init__(self):
        self._unicorns_exist = True
        self._file_name = "graph2.txt"
        self._graph = None
        self.main_loop()

    def main_loop(self):
        while self._unicorns_exist:
            self.print_menu()
            command = input(">command: ")
            try:
                self.handle_command(command)
                pass
            except ConsoleException as e:
                print(e)

    def main_loop_read(self):
        self.print_menu_read()
        while self._unicorns_exist:
            command = input(">command: ")
            try:
                self.handle_command_read(command)
            except ConsoleException as e:
                print(e)

    def handle_command(self, command: str):
        """
        The beginning of the program. You can exit, read a file or generate a graph
        """
        command = command.strip()
        if command == "0":
            self._unicorns_exist = False
        elif command == "1":
            file = input("Name of file: ")
            my_file = Path(file)
            if my_file.is_file():
                self._file_name = file
                self.read_file()
                self.main_loop_read()
            else:
                print(colored("The file doesn't exist", "red"))
        elif command == "2":
            nr_vertices = int(input("Nr vertices= "))
            nr_edges = int(input("Nr edges= "))
            self._file_name = "random.txt"
            self.generate_graph(nr_vertices, nr_edges)
        elif command == "3":
            self._file_name = "random_graph1.txt"
            self.generate_graph(7, 20)
            self._file_name = "random_graph2.txt"
            self.generate_graph(6, 40)
        else:
            raise ConsoleException("Wrong command!")

    def handle_command_read(self, command: str):
        command = command.strip()

        if command == "0":
            self._unicorns_exist = False

        elif command == "1":
            number = self._graph.get_number_vertices()
            print("\nThe number of vertices is ", colored(number, "blue"), "\n")

        elif command == "2":
            vertices = self._graph.parse_vertices()
            print("\nThe vertices are: ")
            string = ""
            for vertex in vertices:
                string += str(vertex) + " "
            print(colored(string, "blue"), "\n")

        elif command == "3":
            print("\nInput the 2 vertices:")
            x = int(input("x= "))
            y = int(input("y= "))
            try:
                rez = self._graph.is_edge(x, y)
                if rez:
                    print(colored("There is an edge between them\n", "blue"))
                else:
                    print(colored("There is not an edge between them\n", "blue"))
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "4":
            x = int(input("\nInput the vertex: "))
            try:
                degree = self._graph.in_degree(x)
                print("The in degree is ", colored(degree, "blue"))
                degree = self._graph.out_degree(x)
                print("The out degree is ", colored(degree, "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "5":
            x = int(input("\nInput the vertex: "))
            try:
                vertices_out = self._graph.parse_vertex_out(x)
                string = ""
                print("The outbound edges of the vertex are:")
                for vertex in vertices_out:
                    string += str(vertex) + ", "
                if string == "":
                    print(colored("The vertex doesn't have any outbound edges", "blue"))
                else:
                    print(colored(string[:-2], "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "6":
            x = int(input("\nInput the vertex: "))
            try:
                vertices_in = self._graph.parse_vertex_in(x)
                string = ""
                for vertex in vertices_in:
                    string += str(vertex) + ", "
                if string == "":
                    print(colored("The vertex doesn't have any inbound edges", "blue"))
                else:
                    print(colored(string[:-2], "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "7":
            print("\nInput the 2 vertices:")
            x = int(input("x= "))
            y = int(input("y= "))
            try:
                cost = self._graph.get_cost(x, y)
                print("The cost of the edge is " + colored(cost, "blue") + "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "8":
            print("\nInput the 2 vertices and new cost:")
            x = int(input("x= "))
            y = int(input("y= "))
            c = int(input("new cost= "))
            try:
                self._graph.modify_cost(x, y, c)
                print(colored("The cost has been modified!", "blue") + "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "9":
            print("\nInput the 2 vertices and the cost:")
            x = int(input("x= "))
            y = int(input("y= "))
            c = int(input("new cost= "))
            try:
                self._graph.add_edge(x, y, c)
                print(colored("Edge added!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "10":
            print("\nInput the 2 vertices of the edge:")
            x = int(input("x= "))
            y = int(input("y= "))
            try:
                self._graph.remove_edge(x, y)
                print(colored("Edge removed!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "11":
            print("\nInput the vertex that you want to add:")
            x = int(input("x= "))
            try:
                self._graph.add_vertex(x)
                print(colored("Vertex added!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

            pass

        elif command == "12":
            print("\nInput the vertex that you want to remove:")
            x = int(input("x= "))
            try:
                self._graph.remove_vertex(x)
                print(colored("Vertex removed!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "13":
            self.save()
        elif command == "14":
            vertex1 = int(input("first vertex: "))
            vertex2 = int(input("second vertex: "))
            cost_matrix, parent_matrix, steps = self._graph.find_cost_matrix()

            negative_cycles = False
            is_path = True

            for i in range(self._graph.get_number_vertices()):
                if cost_matrix[i][i] < 0 and not negative_cycles:
                    print(colored("\nThere are negative cost cycles...", "red"))
                    negative_cycles = True
            if steps[-1][vertex1][vertex2] == math.inf:
                print(colored("\nThere is no path between them...", "red"))
                is_path = False
            if not negative_cycles and is_path:
                print(colored("\nSteps:", "blue"))
                p = 1
                for matrix in steps:
                    print(colored(f"A{p}", "blue"))
                    for line in matrix:
                        print(line)
                    p *= 2
                print("We can see the last 2 matrices are equal.")
                print(colored("Minimum cost path between two vertices and the corresponding cost:", "blue"))
                self._graph.print_path(parent_matrix[vertex1], vertex2)
                print("with the cost", steps[-1][vertex1][vertex2])

        elif command == "*":
            self._graph.print_dict()
            pass
        else:
            raise ConsoleException("Wrong command!")

    def save(self):
        if "modified" not in self._file_name and "random" not in self._file_name:
            filename = self._file_name[:-4] + "-modified.txt"
        else:
            filename = self._file_name
        # self._graph.sort_dictionaries()
        with open(filename, "w") as file:
            vertices = self._graph.parse_vertices()
            for vertex in vertices:
                # get the list of outbound edges
                vertices_out = list(self._graph.parse_vertex_out(vertex))

                # check if it's isolated
                if len(vertices_out) == 0:
                    vertices_in = list(self._graph.parse_vertex_in(vertex))
                    if len(vertices_in) == 0:
                        file.write(str(vertex) + "\n")
                        continue

                # if it's not isolated
                for vertex_out in vertices_out:
                    line = str(vertex) + " " + str(vertex_out) + " " + str(self._graph.get_cost(vertex, vertex_out))
                    file.write(line + "\n")
            file.close()

    def read_file(self):
        """
        # On the first line, the number n of vertices and the number m of edges;
        # On each of the following m lines, three numbers, x, y and c, describing an edge:
        # the origin, the target and the cost of that edge.
        """
        try:
            with open(self._file_name, "r") as file:
                lines = [data.split(' ') for data in file.read().split('\n')]
                n = int(lines[0][0])
                m = int(lines[0][1])
                self._graph = Graph(n)

                for line in lines[1:]:
                    if line == [''] or line == ['\n']:
                        continue
                    if len(line) == 1:
                        # self._graph.add_vertex(int(line[0]))
                        continue
                    else:
                        self._graph.add_edge_no_condition(int(line[0]), int(line[1]), int(line[2]))

        except FileNotFoundError as e:
            raise FileNotFoundError()

    def generate_graph(self, nr_vertices, nr_edges):
        # maximum nr of edges (without loops): n(n-1)
        # maximum nr of edges (with loops): n^2

        self._graph = Graph(nr_vertices)

        if nr_edges > nr_vertices*nr_vertices:
            print(colored(f"Data is not correct for file {self._file_name} with {nr_vertices} "
                          f"vertices and {nr_edges} edges, too many edges!", "red"))
        else:
            added_edges = 0
            possibilities = [(x, y) for x in range(nr_vertices) for y in range(nr_vertices)]
            while added_edges < nr_edges:
                index = random.randrange(len(possibilities))
                edge = possibilities[index]
                possibilities.pop(index)
                self._graph.add_edge(edge[0], edge[1], random.randint(-100, 100))
                added_edges += 1
            self.save()


    @staticmethod
    def print_menu():
        print(
            "✨ Menu ✨"
            "\n\t1. Read graph"
            "\n\t2. Generate graph"
            "\n\t3. Generate graph in random_graph1.txt and random_graph2.txt"
            "\n\t0. Exit"
        )

    @staticmethod
    def print_menu_read():
        print(
            "✨ Menu - read ✨"
            "\n\t1. Get the number of vertices"
            "\n\t2. The set of vertices"
            "\n\t3. Check if there is an edge between 2 vertices"
            "\n\t4. Get the in & out degree of a vertex"
            "\n\t5. Get the set of outbound edges of a specified vertex"
            "\n\t6. Get the set of inbound edges of a specified vertex"
            "\n\t7. Get cost of edge"
            "\n\t8. Modify cost of edge"
            "\n\t9. Add edge"
            "\n\t10. Remove edge"
            "\n\t11. Add vertex"
            "\n\t12. Remove vertex"
            "\n\t13. Save"
            "\n\t14. Minimum cost walk between all pairs of vertices(matrix multiplication)"
            "\n\t0. Exit"
        )
