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
    
    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def load_graph(self):
        self.nodes = self.conn.get_nodes()
        # nodes =  list(map(lambda node: node.name, self.nodes))
        # print(f"nodes: {self.nodes}")
        self.edges = self.conn.get_edges(self.nodes)
        # print(f"Edges:: {self.edges}")

        # for edge1 in self.edges:
        # print(f"nodes:: {self.edges[0]}")
        # print(f"edges:: {self.edges[1]}")
        # for edge in self.edges:
        #     print(f"Edge: {edge[0]} -> {edge[1]} ")
            # self.edges.append([currNode, currEdge, edgeWeight])
            # currNode.addChildren([currEdge], [edgeWeight])

    def gen_random(self, n, p=0.5):
        self.nodes = [ nd.Node(
                        "N"+str(i),
                         int((100 - 1) * np.random.random_sample() + 1)
                        ) for i in range(n-1)]
        self.nodes.append(nd.Node("N" + str(n-1), 0))
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
                        # print(edgeName)
                        edges[edgeName] = (currNonde.name, edgeWeight)

        # print("\n")
        for edge in edges:
            edgeName = edge
            currNodeName = edges[edge][0]
            edgeWeight = edges[edge][1]
            
            # Weight should be != 0
            if edgeWeight > 0:
            
                currNode = self.get_node(currNodeName)
                currEdge = self.get_node(edgeName)

            #     print("Edge: {}, Weight: {}".format(currEdge, edgeWeight))
                # print("Node: {}, Edge: {}, Weight: {}".format(currNodeName, edgeName, edgeWeight))
                
                self.edges.append([currNode, currEdge, edgeWeight])
                currNode.addChildren([currEdge], [edgeWeight])
                # print(currNode.children)

    def average_children(self):
        children = []
        for node in self.nodes:
            children.extend(node.children)
        return int(len(children) / len(self.nodes))

if __name__ == "__main__":
    grafo = Graph()
    grafo.read_file("..\\uploads\\199bf4f6a5444539a0fd2d852f8b042f-ex.txt")
    print(grafo.nodes)
    print(grafo.edges)
