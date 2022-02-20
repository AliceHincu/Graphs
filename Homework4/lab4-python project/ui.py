from graph import Graph, GraphException
from termcolor import colored
from pathlib import Path


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
            sorted_list = self._graph.topological_sorting()
            if len(sorted_list) == 0:
                print(colored("Graph is not DAG", "red"))
            else:
                print(colored("The topological sorting is:", "blue"))
                print(sorted_list)
        elif command == "15":
            tme, tmb, TMB, TME, duration = self._graph.get_times()
            if duration == -1:
                print(colored("Graph is not DAG", "red"))
            else:
                from texttable import Texttable
                t = Texttable()
                table_list = list()
                table_list.append(['Activity', 'Earlies', 'Latest'])

                for i in range(self._graph.get_number_vertices()):
                    table_list.append([str(i), str(tmb[i])+"-"+str(tme[i]), str(TMB[i])+"-"+str(TME[i])])

                t.add_rows(table_list)
                print(t.draw())
                print(colored("The project duration:" + str(duration), "blue"))
        elif command == "16":
            arr = self._graph.critical_activities()
            print(colored("The critical activities are:", "blue"))
            if not arr:
                print(colored("Graph is not DAG", "red"))
            else:
                for i in arr:
                    print(i, end=" ")
                print("\n")
        elif command == "17":
            sorted_list = self._graph.topological_sorting()
            if len(sorted_list) == 0:
                print(colored("Graph is not DAG", "red"))
            else:
                src = int(input("Source: "))
                dest = int(input("Destination: "))
                nr = self._graph.distinct_paths(src, dest)
                if nr != -1:
                    print("Number of distinct paths: ", nr)
                else:
                    print(colored("Graph is a DAG", "red"))
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
        # On each of the following lines: the activity, prerequisites and duration
        """
        try:
            with open(self._file_name, "r") as file:
                lines = [data.split(',') for data in file.read().split('\n')]
                n = int(lines[0][0])
                self._graph = Graph(n)
                times = [0] * n
                for line in lines[1:]:
                    activity = int(line[0])
                    duration = int(line[2])
                    prerequisites = list()
                    if line[1] != "-":
                        prerequisites = [vertex for vertex in line[1].split('+')]
                    times[activity] = duration
                    for vertex in prerequisites:
                        self._graph.add_edge_no_condition(int(vertex), activity, 0)
                self._graph.set_initial_time(times)
        except FileNotFoundError as e:
            raise FileNotFoundError()


    @staticmethod
    def print_menu():
        print(
            "✨ Menu ✨"
            "\n\t1. Read graph"
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
            "\n\t14. Topological sorting"
            "\n\t15. Earliest and the latest starting time for each activity and the total time of the project"
            "\n\t16. Critical activities"
            "\n\t17. Number of paths from v1 to v2"
            "\n\t0. Exit"
        )
