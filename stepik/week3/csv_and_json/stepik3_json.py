import json


class Inheritance:
    def __init__(self):
        self.data = None  # dict object of input data
        self.children = {}  # keys are children, direct parents are values
        self.descendants = {}  # keys are descendants, values are all ancestors
        self.ancestors = {}  # keys are ancestors, values are all children
        self._parents_temp_set = set()

    def keyboard_input_handling(self):
        """ Takes json string as an input and stores it as a dict into self.data """
        data = input()
        self.data = json.loads(data)

    def form_children_dict(self, number_of_inputs, input_handling):
        """ Forms a dictionary of children (keys) and parents (values)."""
        for _ in range(number_of_inputs):
            a, *b = input_handling()
            # print(b)  # ['A', 'C']
            # print(*b)  # A C
            # if key doesn"t exist then parent is an empty set, else append parents
            self.children[a] = self.children.get(a, set()) | set(b)
            for i in b:
                self.children[i] = self.children.get(i, set())

    def run_form_children_dict(self):
        """ Specifies params needed to form self.children and runs self.form_children_dict """
        number_of_inputs = len(self.data)
        input_handling = ((dct["name"], *dct["parents"]) for dct in self.data)
        self.form_children_dict(number_of_inputs, input_handling.__next__)

    def find_all_ancestors(self, child):
        """ Recursively gathers parents of all parents in self.parents_temp.
         Does not support cycled inheritance. """
        self._parents_temp_set.update(self.children[child])
        for parent in self.children[child]:
            self.find_all_ancestors(parent)

    def add_to_descendants_dict(self, child):
        """ Adds info of all ancestors of a child and add it to self.descendants dict.
        Clears self.parents_temp_set """
        self.find_all_ancestors(child)
        # note that set("abc") is {'a', 'b', 'c'}, but {"abc"} is {"abc"}
        self.descendants[child] = self.descendants.get(child, {child}) | self._parents_temp_set
        self._parents_temp_set = set()

    def form_descendants_dict(self):
        """ Runs trough all children in self.children and forms self.descendants dict,
         where child is a key and values are all of its ancestors, including the child."""
        for child in self.children.keys():
            self.add_to_descendants_dict(child)

    def form_ancestors_dict(self):
        """ Runs through every child (name) in self.descendants and checks if it"s a parent of any other class (child).
         If so the (name) is a key and (child) is added to values.
         Every class is at least a parent of itself. """
        for name in self.descendants.keys():
            for child, parents in self.descendants.items():
                if name in parents:
                    self.ancestors[name] = self.ancestors.get(name, set()) | {child}

    def print_number_of_descendants(self):
        """ Prints out name of every class alphabetically ordered
        and number of classes which inherit from it (including itself). """
        ancestors = []
        for parent, children in self.ancestors.items():
            ancestors.append((parent, len(children)))
        ancestors.sort()
        for name, number_of_descendants in ancestors:
            print(f"{name} : {number_of_descendants}")

    def main(self, to_print=False):
        self.keyboard_input_handling()
        self.run_form_children_dict()
        self.form_descendants_dict()
        self.form_ancestors_dict()
        if to_print:
            print(f"children: {self.children}")
            print(f"descendants: {self.descendants}")
            print(f"ancestors: {self.ancestors}")
        self.print_number_of_descendants()


# examples
# [{"name": "A", "parents": []}, {"name": "B", "parents": ["A", "C"]}, {"name": "C", "parents": ["A"]}]
# A : 3
# B : 1
# C : 2

# [{"name": "Gr", "parents": ["Fr"]}, {"name": "Ar", "parents": []}, {"name": "Br", "parents": ["Ar"]}, {"name": "Cr", "parents": ["Ar"]}, {"name": "Dr", "parents": ["Br", "Cr"]}, {"name": "Er", "parents": ["Dr"]}, {"name": "Fr", "parents": ["Dr"]}, {"name": "Xr", "parents": []}, {"name": "Yr", "parents": ["Xr", "Ar"]}, {"name": "Zr", "parents": ["Xr"]}, {"name": "Vr", "parents": ["Zr", "Yr"]}, {"name": "Wr", "parents": ["Vr"]}]
# ans
# A : 5
# B : 1
# C : 4
# D : 2
# E : 1
# F : 3

if __name__ == "__main__":
    exp = Inheritance()
    exp.main(to_print=True)
