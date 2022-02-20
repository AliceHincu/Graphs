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
        self._file_name = "graph-simple.txt"
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
                degree = self._graph.degree(x)
                print("The degree is ", colored(degree, "blue"))
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "5":
            x = int(input("\nInput the vertex: "))
            try:
                vertices_out = self._graph.parse_vertex(x)
                string = ""
                print("The edges of the vertex are:")
                for vertex in vertices_out:
                    string += str(vertex) + ", "
                if string == "":
                    print(colored("The vertex doesn't have any edges", "blue"))
                else:
                    print(colored(string[:-2], "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"))

        elif command == "6":
            print("\nInput the 2 vertices:")
            x = int(input("x= "))
            y = int(input("y= "))
            try:
                self._graph.add_edge(x, y)
                print(colored("Edge added!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "7":
            print("\nInput the 2 vertices of the edge:")
            x = int(input("x= "))
            y = int(input("y= "))
            try:
                self._graph.remove_edge(x, y)
                print(colored("Edge removed!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "8":
            print("\nInput the vertex that you want to add:")
            x = int(input("x= "))
            try:
                self._graph.add_vertex(x)
                print(colored("Vertex added!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

            pass

        elif command == "9":
            print("\nInput the vertex that you want to remove:")
            x = int(input("x= "))
            try:
                self._graph.remove_vertex(x)
                print(colored("Vertex removed!", "blue"), "\n")
            except GraphException as e:
                print(colored(e, "red"), "\n")

        elif command == "10":
            self.save()

        elif command == "11":
            cc = self._graph.connected_components()
            for i in range(len(cc)):
                print(f"Connected component nr {i + 1}:\n{cc[i]}")

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
            edges = []
            for vertex in vertices:
                # get the list of outbound edges
                vertices_out = list(self._graph.parse_vertex(vertex))

                # check if it's isolated
                if len(vertices_out) == 0:
                    file.write(str(vertex) + "\n")
                    continue

                # if it's not isolated
                for vertex_out in vertices_out:
                    edge = (min(vertex, vertex_out), max(vertex, vertex_out))
                    if edge not in edges:
                        line = str(edge[0]) + " " + str(edge[1])
                        file.write(line + "\n")
                        edges.append(edge)
            file.close()

    def read_file(self):
        """
        # On the first line, the number n of vertices and the number m of edges;
        # On each of the following m lines, two numbers(x, y describing an edge:
        # the origin and the target), or one number (isolated vertex).
        """
        try:
            if "modified" not in self._file_name:
                with open(self._file_name, "r") as file:
                    lines = [data.split(' ') for data in file.read().split('\n')]
                    # a line is saved as a list. example: ['0', '0']

                    n = int(lines[0][0])
                    m = int(lines[0][1])
                    self._graph = Graph(n)

                    for line in lines[1:]:
                        if line == [''] or line == ['\n']:
                            continue
                        if len(line) != 1:
                            self._graph.add_edge_no_condition(int(line[0]), int(line[1]))
                            continue
            else:
                with open(self._file_name, "r") as file:
                    lines = [data.split(' ') for data in file.read().split('\n')]
                    self._graph = Graph(0)

                    for line in lines:
                        if line == [''] or line == ['\n']:
                            continue
                        if len(line) == 1:
                            self._graph.add_vertex(int(line[0]))
                            continue
                        x = int(line[0])
                        y = int(line[1])

                        try:
                            self._graph.add_vertex(x)
                        except GraphException:
                            pass

                        try:
                            self._graph.add_vertex(y)
                        except GraphException:
                            pass

                        self._graph.add_edge_no_condition(x, y)

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
                self._graph.add_edge(edge[0], edge[1])
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
            "\n\t4. Get the degree of a vertex"
            "\n\t5. Get the set of edges of a specified vertex"
            "\n\t6. Add edge"
            "\n\t7. Remove edge"
            "\n\t8. Add vertex"
            "\n\t9. Remove vertex"
            "\n\t10. Save"
            "\n\t11. Connected components"
            "\n\t0. Exit"
        )
