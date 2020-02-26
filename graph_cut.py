from graph import Graph
import numpy as np

class GraphCut(object):
    def __init__(self, nodes, connections):
        """
        __init__: Initialize graph
        nodes: A list of vertices
        connections: A list of connections
        """
        self.graph = dict((node, []) for node in nodes)
        for node1, node2, capacity in connections:
            self.graph[node1].append((node2, capacity, 0))
        self.mincut = np.full(len(self.graph), False)

    def residual_graph_build(self):
        connections = []
        for node, neighbors in self.graph.items():
            for neighbor, c, f in neighbors:
                if c > f:
                    connections.append((node, neighbor, c - f))
                if f > 0:
                    connections.append((neighbor, node, f))
        return connections

    def augmenting_arc(self, node1, node2, inc):
        neighbor = self.graph[node1]
        for index in range(len(neighbor)):
            v, capacity, weight = neighbor[index]
            if v == node2 and capacity - weight >= inc:
                neighbor[index] = (node2, capacity, weight + inc)
                return

        neighbor = self.graph[node2]
        for index in range(len(neighbor)):
            if v == node1 and weight >= inc:
                neighbor[index] = (node2, capacity, weight - inc)
                return

    def augmenting_flow(self, connections, inc):
        for node1, node2 in connections:
            self.augmenting_arc(node1, node2, inc)

    def min_cut(self, s, t):
        while(True):
            residual_graph = Graph(self.graph.keys(), self.residual_graph_build())
            connections, visited, inc = residual_graph.augmenting_path(s, t)
            #print(self.calculate_max_flow(s,t), inc)
            if inc <= 0:
                print(visited)
                self.mincut = visited
                break
            self.augmenting_flow(connections, inc)
            print(self.graph)

    def calculate_cut_value(self):
        result = 0
        for node, neighbors in self.graph.items():
            if not self.mincut[node]:
                continue

            for neighbor, c, _ in neighbors:
                if not self.mincut[neighbor]:
                    result = result + c
        return result

    def calculate_max_flow(self, s, t):
        neighbor_s = self.graph[s]
        result = 0
        for (_, _, w) in neighbor_s:
            result = result + w
        return result

def random_graph(n, epsilon = 0.2):
    connections = []
    nodes = []
    for i in range(n):
        nodes.append(i)
        for j in range(n):
            if j == i:
                continue
            t = np.random.rand()
            if (t <= epsilon):
                w = np.random.randint(10)
                connections.append((i,j,w))
    return nodes, connections

#nodes = [0,1,2,3]
#connections = [(0, 1, 2), (0, 2, 9), (1, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 4)]
#nodes = [0, 1, 2]
#connections = [(0, 1, 3), (0, 2, 7), (1, 0, 1), (1, 2, 7), (2, 0, 6), (2, 1, 9)]
nodes, connections = random_graph(10, epsilon = 0.5)
g = GraphCut(nodes, connections)
print(connections)
g.min_cut(0, 3)
print(g.calculate_max_flow(0,4))
print(g.calculate_cut_value())
