
class ErrorInheritance:
    def __init__(self):
        self.children = {}  # parents are values
        self.ancestors = {}  # values are lists of all ancestors
        self.parents_temp_set = set()
        self.list_of_inputs = []
        self.list_of_unnecessary_classes = []

    def child_parents_input(self, number_of_inputs, input_handling):
        """ Forms a dictionary of children (keys) and parents (values).
         Takes an inputs as lines of Child : Parent1 Parent2 with no commas"""
        for _ in range(number_of_inputs):
            a, *b = input_handling().rstrip().replace(":", " ").split()
            # if key doesn't exist then parent is an empty set, else append parents
            self.children[a] = self.children.get(a, set()) | set(b)
            for i in b:
                self.children[i] = self.children.get(i, set())

    def find_all_ancestors(self, child):
        """ recursively gathers parents of all parents in self.parents_temp """
        self.parents_temp_set.update(self.children[child])
        for parent in self.children[child]:
            self.find_all_ancestors(parent)

    def add_to_ancestors_dict(self, child):
        """ gets set of all ancestors(values) of child(key) to self.ancestors dict and clears self.parents_temp_set """
        self.find_all_ancestors(child)
        self.ancestors[child] = self.ancestors.get(child, set()) | self.parents_temp_set
        self.parents_temp_set = set()

    def gather_unnecessary_inputs(self, number_of_inputs, input_handling):
        """ checks if the class or its ancestor has already been input """
        for _ in range(number_of_inputs):
            i = input_handling().rstrip()
            if i in self.list_of_inputs or set(self.list_of_inputs) & self.ancestors[i]:
                self.list_of_unnecessary_classes.append(i)
                # print(f"{i} added")
            self.list_of_inputs.append(i)
            # print("Inputs so far", self.list_of_inputs)

    def main(self, number_of_inputs, input_handling, to_print=False):
        n = int(number_of_inputs())
        self.child_parents_input(n, input_handling)
        for child in self.children:
            self.add_to_ancestors_dict(child)
        if to_print:
            print(self.ancestors)
        n = int(number_of_inputs())
        self.gather_unnecessary_inputs(n, input_handling)
        return self.list_of_unnecessary_classes

    def launch_console_task(self):
        self.main(input, input)
        for i in self.list_of_unnecessary_classes:
            print(i)

    def run_test_from_file(self, file, to_print=False):
        with open(file) as f:
            self.main(f.readline, f.readline, to_print)
            return all([i == f.readline().rstrip() for i in self.list_of_unnecessary_classes])


if __name__ == "__main__":
    # ErrorInheritance().launch_console_task()

    if ErrorInheritance().run_test_from_file("example_for_error_inheritance.txt", to_print=False):
        print("Test passed")

    if ErrorInheritance().run_test_from_file("example_for_error_inheritance2.txt"):
        print("Test passed")
