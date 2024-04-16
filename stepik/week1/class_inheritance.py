
class MROImplementation:
    def __init__(self):
        self.children = {}  # parents are values
        self.ancestors = {}  # values are lists of all ancestors
        self.parents_temp_list = []

    def child_parents_input(self):
        """ first input to form a dictionary of children (keys) and parents (values) """
        input_data = int(input())
        for _ in range(input_data):
            a, *b = input().replace(":", " ").split()
            self.children[a] = \
                self.children.get(a, []) + b  # if key doesn't exist then parent is an empty list, else append parents
            for i in b:
                self.children[i] = self.children.get(i, [])
        # self.children = {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B', 'C']}

    def find_all_ancestors(self, child):
        """ recursively gathers parents of all parents in self.parents_temp_list """
        self.parents_temp_list += self.children[child]
        for parent in self.children[child]:
            self.find_all_ancestors(parent)

    def add_to_ancestors_dict(self, child):
        """ gets all ancestors of child as key to self.ancestors dict and clears self.parents_temp_list"""
        self.find_all_ancestors(child)
        self.ancestors[child] = self.ancestors.get(child, []) + self.parents_temp_list
        self.parents_temp_list = []

    def inheritance_check(self):
        """ checks if first class is the ancestor of the second class """
        input_data_qntty = int(input())
        for _ in range(input_data_qntty):
            # print(f"Children: {self.children}")
            self.parent, self.child = input().split()
            self.ancestor_check(self.parent, self.child)

    def ancestor_check(self, parent, child):
        self.add_to_ancestors_dict(child)
        # print(f"Parents are: {self.ancestors}")
        # print(f"parents of {self.child} are {self.ancestors[child]}")
        print("Yes" if parent in self.ancestors[child] or parent == child else "No")

    def launch(self):
        self.child_parents_input()
        # print(self.children)
        # for child in self.children.keys():
        #     self.add_to_ancestors_dict(child)
        # print(self.ancestors)
        self.inheritance_check()


if __name__ == "__main__":
    MROImplementation().launch()
