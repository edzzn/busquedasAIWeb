import numpy as np
import DBConnection as DB
import Node as nd
import Search as Search

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
    
    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def gen_random(self, n, p=0.5):
        self.nodes = [ nd.Node("N"+str(i)) for i in range(n)]
        for node_i in self.nodes:
            for node_j in self.nodes:
                if np.random.random() <= p and node_i is not node_j:
                    edge_val = int((100 - 1) * np.random.random_sample() + 1)
                    node_i.addChildren([node_j], [edge_val])
                    self.edges.append([node_i, node_j, edge_val])

    def read_file(self, file_name):
        edges = {}
        file = open(file_name, "r")
        graph_data = file.read()
        for row in graph_data.split("\n"):
            # print(row)
            # Beware of empty lines
            if not row:
                pass
            #   Heuristica
            elif ";" not in row:
                pass
                # print("Heuristica: {}:{}".format(row.split(":")[0], row.split(":")[1]))    
            else:   
                currNode = None
                for i, node in enumerate(row.split(";")):
                    if i == 0:
                        currNonde = nd.Node(node.split(":")[0], int(node.split(":")[1]))
                        self.nodes.append(currNonde)
                        
                    else:
                        edgeName = str(node.split(":")[0])
                        edgeWeight = int(node.split(":")[1])
                        edgeHeuristic = int(node.split(":")[2])
                        # print(edgeName)
                        edges[edgeName] = (currNonde.name, edgeWeight, edgeHeuristic)

        # print("\n")
        for edge in edges:
            edgeName = edge
            currNodeName = edges[edge][0]
            edgeWeight = edges[edge][1]
            
            edgeHeuristic = edges[edge][2]
            
            # Weight should be != 0
            if edgeWeight > 0:
            
                currNode = self.get_node(currNodeName)
                currEdge = self.get_node(edgeName)

            #     print("Edge: {}, Weight: {}".format(currEdge, edgeWeight))
                # print("Node: {}, Edge: {}, Weight: {}".format(currNodeName, edgeName, edgeWeight))
                
                self.edges.append([currNode, currEdge, edgeWeight])
                currNode.addChildren([currEdge], [edgeWeight])
                # print(currNode.children)

if __name__ == "__main__":
    grafo = Graph()
    grafo.read_file("..\\uploads\\d0de61ca5ba04c06b08bc01182b3e9af-ex.txt")
    print(grafo.nodes)
    print(grafo.edges)
    search = Search.Search()

    
    init_node = grafo.get_node('a')
    # print(init_node)
    nodeVal= 'h'

    path, found, stack = search.DFS(init_node, [nodeVal], False, 'ASC')
    for row in stack:
       print(row)
