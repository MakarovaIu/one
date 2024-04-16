"""
Students line up and must be ordered alphabetically.
The teacher only swaps the positions of two students that are next to each other in line.
Let's consider a line of three students, Alice, Bob, and Carol (denoted A, B, and C).
Using the Graph class created in the lecture, we can create a graph with the following design:
vertices represent permutations of the students in line; edges connect two permutations if
one can be made into the other by swapping two adjacent students.
"""
from unit1_graphs import Node, Edge, Graph


class WeightedEdge(Edge):
    def __init__(self, src, dest, weight=0):
        super().__init__(src, dest)
        self.weight = weight

    def getWeight(self):
        return self.weight

    def __str__(self):
        return super().__str__() + " ({})".format(self.getWeight())


def organizing_students():
    # We construct our graph by first adding the following nodes:
    nodes = [Node("ABC"), Node("ACB"), Node("BAC"), Node("BCA"), Node("CAB"), Node("CBA")]

    g = Graph()
    for n in nodes:
        g.addNode(n)

    # My code below.

    # Add the appropriate edges to the graph.
    # Edges connect two nodes if a permutation is possible. Only adjacent students can be swapped.
    N = len(nodes)
    for i in range(N):
        for j in range(i+1, N):
            if nodes[i].getName()[:2] == nodes[j].getName()[1::-1] \
                    or nodes[i].getName()[1:] == nodes[j].getName()[:0:-1]:
                g.addEdge(Edge(nodes[i], nodes[j]))

    return g


if __name__ == '__main__':
    students_graph = organizing_students()
    print(students_graph)
