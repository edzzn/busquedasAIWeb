#!/usr/bin/env python
# coding: utf-8

# # Busqueda Ciegas
# 
# ## Clase Nodo
# 

# In[114]:


class Node:
    def __init__(self, name, value=0, parent=[], *children):
        self.name = name
        self.value = value
        self.parents = parent[:]
        self.children = list(children)
        self.pesos = {}
        
    def __repr__(self):
        # return f"{self.name}[{self.value}, {self.pesos}, {len(self.children)}]"
        return f"{self.name}"

    def setParents(self, *parents):
        self.parents = parents
        
        for parent in self.parents:
            parent.addChildren(self)

    def _addParents(self, *parents):
        self.parents.extend(parents)
    
#         for parent in parents:
#             if self not in parent.children:
#                 parent.addChildren(self)

    def addChildren(self, children, pesos=[]):
        self.children.extend(children)


        for i, child in enumerate(children):
            if len(pesos) > i:
                self.pesos[child] = pesos[i]

            print(f"Self: {self}, child: {child}, Child.Parents: {child.parents}")
            if self not in child.parents:
                child._addParents(self)
            
            print('AFTER')
            print(f"Self: {self}, child: {child}, Child.Parents: {child.parents}")
            
            print('\n')

    def remove(self, child):
        self.children.remove(child)


# # Métodos de busqueda

# In[141]:


class Search:
    def DFS(self, Inode, nodeVal=[], showStack = False, sort = 'ASC'):
        queue = []
        visited = []
        found = []
        curNode = None

        queue.insert(0, Inode)

        if (showStack):
            print(f"Searching... {nodeVal} in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{queue[0].name}")
        
        while (len(queue) and (len(found) != len(nodeVal))):
            curNode = queue.pop(0)

            visited.append(curNode)

            if (sort == 'ASC'):
                curNode.children.sort(key=lambda x: x.name, reverse=True)

            else:
                curNode.children.sort(key=lambda x: x.name, reverse=False)

            for child in curNode.children:
                if child not in visited:
                    queue.insert(0, child)

            if (curNode.name in nodeVal):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")
                
        return (visited, found)

    def BFS(self, Inode, nodeVal, showStack = False, sort = 'ASC'):
        queue = []
        visited = []
        found = []
        curNode = None

        queue.append(Inode)

        if (showStack):
            print(f"Searching... {nodeVal} in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{queue[0].name}")
        
        while (len(queue) and (len(found) != len(nodeVal))):
            
            curNode = queue.pop(-1)
            
            visited.append(curNode)

            if (sort == 'ASC'):
                curNode.children.sort(key=lambda x: x.name, reverse=False)
            else:
                curNode.children.sort(key=lambda x: x.name, reverse=True)

            for child in curNode.children:
                if child not in visited:
                    queue.insert(0, child)

            if (curNode.name in nodeVal):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")
                
        return (visited, found)
    
    # Iterative Depth Search
    def IDS(self, Inode, nodeVal, maxLevel=3, showStack = False, sort = 'ASC'):

        visited = []
        found = []
        curNode = None
        curLevel = 0
        isDone = False
        
        if (showStack):
            print(showStack)
            print(f"Searching... {nodeVal} in {Inode.name}")
            print(f"Level {curLevel}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}") 
    
        
        visited.append(Inode)

        if (Inode.name in nodeVal):
            found.append(Inode.name)
            if (showStack):
                print(f"[] \t\t {Inode.name} *")
        else:
            if (showStack):
                print(f"[] \t\t {Inode.name}")  
        if len(found) == len(nodeVal):
            return (visited, found)
        curLevel += 1

        # print('\n\n')
        while curLevel <= maxLevel:        

            queue = []
            found = []
            
            for node in visited:
                
                if (sort == 'ASC'):
                    node.children.sort(key=lambda x: x.name, reverse=False)
                else:
                    node.children.sort(key=lambda x: x.name, reverse=True)

                for child in node.children:
                    if child not in visited:
                        queue.append(child)
            # print(f"Visited: {visited}")
            # print(f"Queue: {queue}")
            temp_a = queue[:]
            queue = visited[:]
            queue.extend(temp_a)
            # print(f"Queue: {queue}")
            
            if (showStack):
                print(f"\nSearching... {nodeVal} in {Inode.name}")
                print(f"Level {curLevel}")
                print(f"Queue \t\t Current")
                print(f"{list(map(lambda node: node.name, queue))}") 
            
            iVisited = []
            for node in queue:
                if node not in visited:
                    visited.append(node)
                iVisited.append(node)
                queue = [item for item in queue if item not in iVisited]
                if (node.name in nodeVal):
                    found.append(node.name)
                    if (showStack):
                        
                        print(f"{list(map(lambda node: node.name, queue))} \t\t {node.name} *")
                else:
                    if (showStack):
                        # queue = list(set(queue) - set(iVisited))
                        print(f"{list(map(lambda node: node.name, queue))} \t\t {node.name}")

            curLevel += 1
        return (visited, found)
                
    # Uniform Cost Search
    def UCS(self, Inode, nodeVal, showStack = False, sort = 'ASC'):
        queue_dict = {}
        visited = []
        found = []
        
        queue_dict[Inode] = 0
        if (showStack):
            print(f"Searching... {nodeVal} in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}")

        while (len(queue_dict) and (len(found) != len(nodeVal))):
            curNode = max(queue_dict, key=queue_dict.get)  # 'min' or 'max' 
            
            visited.append(curNode)
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = curNode.pesos[child] + queue_dict[curNode]

            if (curNode.name in nodeVal):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
        
            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found)

    # Gradient Search
    def GS(self, Inode, showStack = False, sort = 'ASC'):
        queue_dict = {}
        visited = []
        found = []
        
        queue_dict[Inode] = Inode.value
        if (showStack):
            print(f"Searching... in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}")

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max' 
            queue_dict = {}
            # temp_dict = {}
            # print(queue_dict)
            visited.append(curNode)
            # print(f"curNode.children: {curNode.children}")
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = child.value

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                    
        return (visited, found)

    def BestFS(self, Inode, showStack = False, sort = 'ASC'):
        queue_dict = {}
        visited = []
        found = []
        
        queue_dict[Inode] = Inode.value
        if (showStack):
            print(f"Searching... in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}")

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max' 
            visited.append(curNode)
            # print(f"curNode.children: {curNode.children}")
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = child.value

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                    
                    
            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found)

        queue_dict = {}
        visited = []
        found = []
        
        queue_dict[Inode] = Inode.value
        if (showStack):
            print(f"Searching... in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}")

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max' 
            queue_dict = {}
            # temp_dict = {}
            # print(queue_dict)
            visited.append(curNode)
            # print(f"curNode.children: {curNode.children}")
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = child.value

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                    
        return (visited, found)

    def A(self, Inode, showStack = False, sort = 'ASC'):
        queue_dict = {}
        visited = []
        found = []
        
        queue_dict[Inode] = Inode.value
        if (showStack):
            print(f"Searching... in {Inode.name}")
            print(f"Queue \t\t Current")
            print(f"{Inode.name}")

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max' 
            visited.append(curNode)
            # print(f"curNode.children: {curNode.children}")
            for child in curNode.children:
                if child not in visited:
                    # queue_dict[child] = child.value + curNode.pesos[child] + queue_dict[curNode]
                    queue_dict[child] = child.value + curNode.pesos[child]

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                    
                    
            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found)

        
    def sortDESC(self, a, b):
        if a.name > b.name:
            return -1

        if a.name < b.name:
            return 1

        return 0

    def sortASC (self, a, b):
        if a.name > b.name:
            return 1

        if a.name < b.name:
            return -1

        return 0 
    
    
     #Bidireccionar
    def BDS(self, Inode, nodeVal, showStack = False, sort = 'ASC'):
        queueTB = []
        queueBT = []
        visitedTB = []
        visitedBT = []
        found = []
        curNodeTB = None
        curNodeBT = None

        queueTB.append(Inode)
        queueBT.append(nodeVal)

        if (showStack):
            print(f"Searching... {nodeVal} in {Inode.name}")
            print(f"Queue Top-Botton \t\t Current")
            print(f"{queueTB[0].name}")
            print(f"Searching... {Inode.name} in {nodeVal.name}")
            print(f"Queue Botton-TOP \t\t Current")
            print(f"{queueBT[0].name}")
            
            print('\n')
        
        while len(queueTB) and len(queueBT):
            
            # Top-Botton
            curNodeTB = queueTB.pop(-1)
            
            visitedTB.append(curNodeTB)

            if (sort == 'ASC'):
                curNodeTB.children.sort(key=lambda x: x.name, reverse=False)
            else:
                curNodeTB.children.sort(key=lambda x: x.name, reverse=True)

            for child in curNodeTB.children:
                if child not in visitedTB:
                    queueTB.insert(0, child)
                    
            # Botton-Top
            curNodeBT = queueBT.pop(-1)
            
            visitedBT.insert(0,curNodeBT)

            if (sort == 'ASC'):
                curNodeBT.children.sort(key=lambda x: x.name, reverse=False)
            else:
                curNodeBT.children.sort(key=lambda x: x.name, reverse=True)

            for child in curNodeBT.parents:
                if child not in visitedBT:
                    queueBT.insert(0, child)

            # Compare
            if (showStack):
                print(f"Queue Top-Botton \t\t Current")
                if not set(queueBT).isdisjoint(queueTB):
                    print(f"{list(map(lambda node: node.name, queueTB))}** \t\t {curNodeTB.name}")
                else:
                    print(f"{list(map(lambda node: node.name, queueTB))} \t\t {curNodeTB.name}")
                
                print(f"Queue Botton-Top \t\t Current")
                if not set(queueBT).isdisjoint(queueTB):
                    print(f"{list(map(lambda node: node.name, queueBT))}** \t\t {curNodeBT.name}")
                else:
                    print(f"{list(map(lambda node: node.name, queueBT))} \t\t {curNodeBT.name}")               

            if not set(queueBT).isdisjoint(queueTB):
                return ((visitedTB, visitedBT), [nodeVal.name])
                
        return ((visitedTB, visitedBT), ['s'])
    


# # Ejecición Ciegas

# In[115]:


t = Node("T", 20)
n0 = Node("n0", 14)
n1 = Node("n1", 13)
n2 = Node("n2", 12)
n3 = Node("n3", 11)
n4 = Node("n4", 0)
n5 = Node("n5", 17)
n6 = Node("n6", 10)


t.addChildren([n0, n1, n2], [3, 2, 5])
n2.addChildren([n3, n6], [7, 5])
n3.addChildren([n4, n5], [2, 4])


# In[143]:



search = Search()
path, found = search.BDS(t, n4, True, 'ASC')


print(n4.parents)
print('\n')
# path, found = search.BFS(n1, ['N6'], True, 'ASC')
# path, found = search.DFS(n1, ["N6", "N4"], True, 'ASC')
# path, found = search.BFS(t, ["n4"],True, 'ASC')
# path, found = search.IDS(n1, ["N6", "N10"], 2, True, 'ASC')


# In[98]:


get_ipython().run_cell_magic('timeit', '', "path, found = search.GS(t, T, 'ASC')")


# In[144]:


print(f"\nCamino: {path}")
print(f"\nFound: {found}")


# In[64]:


path, found = search.GS(t, ["n4"],True, 'ASC')


# In[67]:



path, found = search.A(t, True, 'ASC')


# In[68]:


print(f"\nCamino: {path}")
print(f"\nFound: {found}")


# # Ejecición Heuristicas

# In[4]:


get_ipython().run_line_magic('time', '')
# Heuristicas

n0 = Node("N0", 0)
n1 = Node("N1", 20)
n2 = Node("N2", 20)
n3 = Node("N3", 10)
n4 = Node("N4", 40)
n5 = Node("N5", 100)
n6 = Node("N6", 110)
n7 = Node("N7", 0)
n8 = Node("N8", 0)

n0.addChildren([n1, n4, n5, n6], [10, 10, 20, 20])
n1.addChildren([n2], [100])
n2.addChildren([n3], [25])
n3.addChildren([n8], [5])
n4.addChildren([n2], [80])
n5.addChildren([n3], [20])
n6.addChildren([n7], [100])



search = Search()

# path, found = search.GS(n0, True, 'ASC')
# path, found = search.BestFS(n0, True, 'ASC')


# In[5]:


get_ipython().run_cell_magic('time', '', "path, found = search.A(n0, False, 'ASC')")


# In[6]:


get_ipython().run_cell_magic('time', '', 'path, found = search.A(n0, True, \'ASC\')\n\nprint(f"\\nCamino: {path}")\nprint(f"\\nFound: {found}")')


# In[7]:


get_ipython().run_cell_magic('time', '', 'path, found = search.BestFS(n0, True, \'ASC\')\n\nprint(f"\\nCamino: {path}")\nprint(f"\\nFound: {found}")')


# # networkx

# In[8]:


import matplotlib.pyplot as plt


# In[9]:


import networkx as nx


# In[10]:


G=nx.Graph()
G.add_nodes_from([2,3])


# In[11]:


G


# In[12]:


H=nx.path_graph(10)
G.add_nodes_from(H)


# In[17]:


nx.draw(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)
plt.show()


# In[20]:


nx.draw(G)
plt.savefig("path.png")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # DB Connection

# In[53]:


# Install
get_ipython().system('conda install psycopg2 -y')


# In[54]:


DB_URI = "postgres://nmipfnmxbjfosa:40a0f08bfad570064c89ba5e3862fe0e2322dabaaaf09aec9460cf9a1afdbc0c@ec2-54-204-14-96.compute-1.amazonaws.com:5432/d68lno2cct2tpd"

import psycopg2 

DB_HOST = "ec2-54-204-14-96.compute-1.amazonaws.com"
DB_DB = "d68lno2cct2tpd"
DB_USER = "nmipfnmxbjfosa"
DB_PASSWORD = "40a0f08bfad570064c89ba5e3862fe0e2322dabaaaf09aec9460cf9a1afdbc0c"


# In[55]:





# In[56]:


commands = [
    """
    CREATE TABLE nodes
    (
        node_id SERIAL PRIMARY KEY,
        node_name VARCHAR(255) NOT NULL,
        CONSTRAINT "Name_unique" UNIQUE (node_name)
    )
    WITH (
        OIDS = FALSE
    )
    """,
    """
    CREATE TABLE edges
    (
        edge_id SERIAL PRIMARY KEY,
        parent_id INTEGER NOT NULL,
        child_id INTEGER NOT NULL,        
        CONSTRAINT parent_child_unique UNIQUE (parent_id, child_id),
        CONSTRAINT "child_FK" FOREIGN KEY (child_id)
            REFERENCES nodes (node_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT "parent_FK" FOREIGN KEY (parent_id)
            REFERENCES nodes (node_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
    WITH (
        OIDS = FALSE
    )
    """
           ]


# In[57]:


create_tables()


# In[58]:
# In[59]:


insert_node(n5)


# In[60]:


insert_edge(n1,n4)


# # Generate Random Graphs
# ## Erdos Renyi 
# http://www.cs.unibo.it/babaoglu/courses/csns/slides/10-models-erdos-renyi.pdf
# https://gnunet.org/sites/default/files/Erd%C5%91s%20%26%20R%C3%A9nyi%20-%20On%20Random%20Graphs.pdf
# 
# Most Basic implementation: https://simondobson.org/2017/06/09/erdos-renyi-networks/
# 
# Total edges = (n(n-1))/n  * p

# In[ ]:


get_ipython().system('conda install numpy -y')


# In[63]:


import numpy as np
import scipy

class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges
    
    def save(self):
        for node in self.nodes:
            insert_node(node)

        for node in self.nodes:
            for child in node.children:
                insert_edge(node,child)
    
    def gen_random(self, n, p=0.5):
        self.nodes = [ Node('N'+str(i)) for i in range(n)]
        for node_i in self.nodes:
            for node_j in self.nodes:
                if np.random.random() <= p:
                    node_i.addChildren(node_j)
                
                
    


# In[64]:


grafo = Graph()


# In[65]:


grafo.gen_random(10, 0.5)


# In[14]:


grafo.nodes


# In[ ]:


grafo.save()


# In[23]:


nodes = get_nodes()


# In[24]:


nodes


# In[25]:


nodes = get_edges(nodes)


# In[26]:


print(nodes)


# In[ ]:




