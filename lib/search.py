class Node:
    def __init__(self, name, value=0, parent=[], *children):
        self.name = name
        self.value = value
        self.parents = parent
        self.children = list(children)
        self.pesos = {}
        
    def __repr__(self):
        return f"{self.name}[{self.value}, {self.pesos}, {len(self.children)}]"
        # return f"{self.name}"

    def setParents(self, *parents):
        self.parents = parents
        
        for parent in self.parents:
            parent.addChildren(self)

    def addParents(self, *parents):
        self.parents.extend(parents)
    
        for parent in parents:
            if self not in parent.children:
                parent.addChildren(self)

    def addChildren(self, children, pesos=[]):
        self.children.extend(children)


        for i, child in enumerate(children):
            if len(pesos) > i:
                self.pesos[child] = pesos[i]

            if self not in child.parents:
                child.addParents(self)

    def remove(self, child):
        self.children.remove(child)

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


if __name__ == '__main__':
    n1 = Node("N1")
    n2 = Node("N2")
    n3 = Node("N3")
    n4 = Node("N4")
    n5 = Node("N5")
    n6 = Node("N6")
    n7 = Node("N7")
    n8 = Node("N8")
    n9 = Node("N9")
    n10 = Node("N10")

    n1.addChildren([n2, n3], [3, 4])
    n2.addChildren([n4, n5], [5, 6])
    n3.addChildren([n6, n7], [7, 8])
    n5.addChildren([n8], [9])



    search = Search()

    # path, found = search.DFS(n1, ["N6", "N4"], True, 'ASC')
    # path, found = search.IDS(n1, ["N6", "N10"], 2, True, 'ASC')
    # path, found = search.UCS(n1, ["N6", "N2"], True, 'ASC')

    # print(f"\nCamino: {path}")
    # print(f"\nFound: {found}")

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
    path, found = search.A(n0, True, 'ASC')

    print(f"\nCamino: {path}")
    print(f"\nFound: {found}")
