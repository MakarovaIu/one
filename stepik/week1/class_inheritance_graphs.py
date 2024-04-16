class Node:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self.name


class Edge:
    def __init__(self, src, dest):
        if type(src) is not Node and type(dest) is not Node:
            raise ValueError("Values must be Nodes")
        self._src = src
        self._dest = dest

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest

    def __str__(self):
        return self.src + " is a child of " + self.dest


class Digraph:
    def __init__(self):
        self.edges = {}  # dict, mapping each node to a list of its parents

    def add_node(self, node):
        if type(node) is not Node:
            raise ValueError("Value must be a node")
        if self.has_node_name(node.name):
            pass
        else:
            self.edges[node] = []

    def add_edge(self, edge):
        if type(edge) is not Edge:
            raise ValueError("Value needs to be an edge")
        src = edge.src
        dest = edge.dest
        if src not in self.edges and dest not in self.edges:
            raise ValueError("Node is not found")
        self.edges[src].append(dest)

    def parents_of(self, node):
        return self.edges[node]

    def has_node(self, node):
        return node in self.edges

    def has_node_name(self, name):
        for node in self.edges:
            if node.name == name:
                return True
        return False

    def get_node(self, name):
        for node in self.edges:
            if node.name == name:
                return node
        raise NameError(name)

    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.name + " is a child of " + dest.name + '\n'
        return result[:-1]  # omit last new line

    def display_edges(self):
        for src in self.edges:
            dest_list = []
            for dest in self.edges[src]:
                dest_list.append(dest.name)
            print(f"{src.name}: {dest_list}")


class BuildGraph:
    def __init__(self):
        self.graph = Digraph()
        self.inputs = None

    def fill_graph(self, src: str, dest: list):
        self.graph.add_node(Node(src))
        for node in dest:
            self.graph.add_node(Node(node))
            self.graph.add_edge(Edge(self.graph.get_node(src), (self.graph.get_node(node))))

    @staticmethod
    def get_number_of_inputs(input_text):
        while True:
            inputs = input(input_text)
            if inputs.isdigit():
                inputs = int(inputs)
                return inputs
            else:
                print("Try again")

    def get_inputs_from_user(self):
        """ First enter a number of inputs. Then sumbit child parents info in a format
        child : parent1 parent2 etc
        without any commas. """
        self.inputs = self.get_number_of_inputs(input_text="Enter a number: ")
        for _ in range(self.inputs):
            src, *dest = input().replace(':', ' ').split()
            self.fill_graph(src, dest)
        return self.graph

    def get_list_inputs(self):
        """ Submit an input as a list to a terminal. Copy example list as a test. """
        self.input_list = input("Enter a list: ")[1:-1].split(',')  # omits [] and splits an input as a list of strings
        for sublist in self.input_list:
            sublist = sublist.rstrip("\'").lstrip(" \'")
            src, *dest = sublist.replace(':', ' ').split()
            self.fill_graph(src, dest)
        return self.graph


class GraphSearch:
    def __init__(self, graph):
        self.graph = graph
        self.parent, self.child = None, None
        self.path = None

    def DFS_call_and_output(self, method_called, output_method, to_print=False, to_print_inner=False):
        self.inputs = BuildGraph.get_number_of_inputs(input_text="Enter a number")
        for _ in range(self.inputs):
            self.parent, self.child = input().split()
            self.path = method_called(
                self.graph, graph.get_node(self.child), graph.get_node(self.parent), [], to_print=to_print_inner)
            if to_print:
                output_method(self.path) if self.path else print("No path found")

    def DFS_inheritance_check(self, to_print, to_print_inner=False):
        print("\n   Inheritance check...")
        self.DFS_call_and_output(self.DFS, self.inheritance_check_output, to_print, to_print_inner)

    def inheritance_check_output(self, path):
        print("Yes" if path else "No")

    def find_all_paths(self, to_print=False, to_print_inner=False):
        print("\n   Finding all paths...")
        self.DFS_call_and_output(self.DFS_all_paths, self.all_paths_output, to_print, to_print_inner)

    def all_paths_output(self, paths):
        print("Paths are:")
        for path in paths:
            self.print_path(path)

    def find_shortest_path(self, to_print=False, to_print_inner=False):
        print("\n Finding shortest path via all paths...")
        self.DFS_call_and_output(self.shortest_path_via_all_paths, self.print_path, to_print, to_print_inner)

    def find_shortest_path_via_DFS(self, to_print=False, to_print_inner=False):
        print("\n Finding shortest path via DFS...")
        self.DFS_call_and_output(self.DFS_shortest_path, self.print_path, to_print)

    def find_path_BFS(self, to_print=False, to_print_inner=False):
        print("\n Finding path via BFS...")
        self.DFS_call_and_output(self.BFS, self.print_path, to_print, to_print_inner)

    def print_path(self, path):
        for node in path:
            if type(node) is not Node:
                raise ValueError("Path mush consist of nodes")
        result = ''
        last_node = path[-1]
        for node in path:
            result = result + str(node)
            if node != last_node:
                result = result + '->'
        print(result)

    def DFS(self, graph, start, end, path=None, to_print=False):
        """ Finds first path if any exists. """
        path = path + [start]
        if to_print:
            print(f"Current path: ", end=''), self.print_path(path)
        if start == end:
            return path
        for node in graph.parents_of(start):
            if node not in path:
                new_path = self.DFS(graph, node, end, path, to_print)
                if new_path:
                    return new_path
        return None

    def DFS_all_paths(self, graph, start, end, path, shortest=None, to_print=False):
        path = path + [start]
        if to_print:
            print(f"Current path: ", end=''), self.print_path(path)
        paths = []
        # if not paths:
        #     print('Paths are none')
        if start == end:
            return [path]
        for node in graph.parents_of(start):
            if node not in path:
                new_paths = self.DFS_all_paths(graph, node, end, path, shortest, to_print)
                # print(len(new_paths))
                for new_path in new_paths:
                    # print("Path updated")
                    paths.append(new_path)
                    # print(f"Len paths: {len(paths)}")
                    # print(f"Path {self.print_path(new_path)} added")
            elif to_print:
                print("Already visited ", node)
        return paths

    def shortest_path_via_all_paths(self, graph, start, end, path, shortest=None, to_print=False):
        paths = self.DFS_all_paths(graph, start, end, path, shortest=None, to_print=False)
        if paths:
            dict_of_paths = {tuple(path): len(path) for path in paths}
            if to_print:
                print("Paths are:")
                for path, length in dict_of_paths.items():
                    self.print_path(path), print(f"length: {length}")
            return min(dict_of_paths, key=dict_of_paths.get)
        return None

    def DFS_shortest_path(self, graph, start, end, path=None, shortest=None, to_print=False):
        path = path + [start]
        if to_print:
            print(f"Current path: ", end=''), self.print_path(path)
        if start == end:
            return path
        for node in graph.parents_of(start):
            if node not in path:
                if shortest is None or len(path) < len(shortest):
                    new_path = self.DFS_shortest_path(graph, node, end, path, shortest)
                    if new_path:
                        shortest = new_path
        return shortest

    def BFS(self, graph, start, end, temp=None, to_print=False):
        """Assumes graph is a Digraph; start and end are nodes
           Returns a shortest path from start to end in graph"""
        init_path = [start]
        path_queue = [init_path]
        while len(path_queue) != 0:
            # Get and remove oldest element in pathQueue
            tmp_path = path_queue.pop(0)
            if to_print:
                print('Current BFS path:',), self.print_path(tmp_path)
            last_node = tmp_path[-1]
            if last_node == end:
                return tmp_path
            for next_node in graph.parents_of(last_node):
                if next_node not in tmp_path:
                    new_path = tmp_path + [next_node]
                    path_queue.append(new_path)
        return None

# example lists are
# ['classA : classB classC classD classG classH', 'classB : classC classE classG classH classK classL', 'classC : classE classD classH classK classL', 'classE : classD classF classK classL', 'classD : classG classH', 'classF : classK', 'classG : classF', 'classH : classL', 'classK : classH classL', 'classL']
# ['G : F E','A','B : A','C : A','D : B C','E : D','F : D','Y : X A','Z : X', 'V : Z Y', 'W : V']


if __name__ == "__main__":
    to_print_state = True
    graph = BuildGraph().get_list_inputs()
    # graph.display_edges()
    b = GraphSearch(graph)
    b.DFS_inheritance_check(to_print_state)
    # b.find_all_paths(to_print_state, to_print_state)
    # b.find_shortest_path(to_print_state, to_print_state)
    # b.find_shortest_path_via_DFS(to_print_state, to_print_state)
    b.find_path_BFS(to_print_state, to_print_state)
