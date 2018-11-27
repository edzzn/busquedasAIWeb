import numpy as np
import DBConnection as DB
import Node as nd

class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes[:]
        self.edges = edges[:]
        self.conn = DB.Connection()
    
    def save(self):
        for node in self.nodes:
            self.conn.insert_node(node)

        for node in self.nodes:
            for child in node.children:
                self.conn.insert_edge(node,child)
    
    def gen_random(self, n, p=0.5):
        self.nodes = [ nd.Node('N'+str(i)) for i in range(n)]
        for node_i in self.nodes:
            for node_j in self.nodes:
                if np.random.random() <= p and node_i is not node_j:
                    edge_val = int((100 - 1) * np.random.random_sample() + 1)
                    node_i.addChildren([node_j], [edge_val])
                    self.edges.append([node_i, node_j, edge_val])


if __name__ == '__main__':
    grafo = Graph()
    grafo.gen_random(10, 0.5)
    print(grafo.nodes)
    print(grafo.edges)
