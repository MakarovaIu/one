"""
Code from MIT 6.00.2x
Created on Tue Jul 12 15:04:56 2016

@author: guttag
"""
from unit1_graphs import Node, Edge, Graph, Digraph
from unit1_student_graph import WeightedEdge


def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):  # Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


def DFS(graph, start, end, path, shortest, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes.
       Returns a shortest path from start to end in graph."""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path:  # avoid cycles
            if shortest is None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest, toPrint)
                if newPath is not None:
                    shortest = newPath
        elif toPrint:
            print('Already visited', node)
    return shortest


def shortestPathDFS(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns the shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)


def testSPDFS(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPathDFS(g, g.getNode(source), g.getNode(destination), toPrint=True)
    if sp is not None:
        print('Shortest path from', source, 'to', destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)


def BFS(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        # Get and remove oldest element in pathQueue
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None


def shortestPathBFS(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)


def cost(path):
    result = ''
    for i in range(len(path)):
        result += str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


def DFS_with_cost(graph, start, end, path, shortest, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes;
         path and shortest are tuples containing a list of
         nodes and a cost
      Returns a shortest path from start to end in graph"""
    path = (path + [start], 0)
    if toPrint:
        print('Current DFS path:', printPath(path[0]))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path:  # avoid cycles
            if not shortest or cost(path) < cost(shortest):
                newPath = DFS(graph, node, end, path, shortest, toPrint)
                if newPath:
                    shortest = newPath


def testSP():
    nodes = []
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):  # Create 6 nodes
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(WeightedEdge(nodes[0], nodes[1]))
    g.addEdge(WeightedEdge(nodes[1], nodes[2]))
    g.addEdge(WeightedEdge(nodes[2], nodes[3]))
    g.addEdge(WeightedEdge(nodes[2], nodes[4]))
    g.addEdge(WeightedEdge(nodes[3], nodes[4]))
    g.addEdge(WeightedEdge(nodes[3], nodes[5]))
    g.addEdge(WeightedEdge(nodes[0], nodes[2], 10))
    g.addEdge(WeightedEdge(nodes[1], nodes[0]))
    g.addEdge(WeightedEdge(nodes[3], nodes[1]))
    g.addEdge(WeightedEdge(nodes[4], nodes[0]))
    sp = shortestPathDFS(g, nodes[0], nodes[5], toPrint=True)
    print('Shortest path is', printPath(sp))
    sp = BFS(g, nodes[0], nodes[5])
    print('Shortest path found by BFS:', printPath(sp))


if __name__ == '__main__':
    # print(buildCityGraph(Graph))

    # testSPDFS('Chicago', 'Boston')
    testSPDFS('Boston', 'Phoenix')

    testSP()
