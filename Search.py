class Search:
    def DFS(self, Inode, nodeVal=[], showStack=False, sort='ASC'):
        stack =  []
        queue = []
        visited = []
        found = []
        curNode = None
        depth = 0

        queue.insert(0, Inode)

        stack.extend([
                f"Searching... {nodeVal} in {Inode.name}",
                f"Queue \t\t Current",
                f"{queue[0].name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

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
                stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")

        return (visited, found, stack)

    def BFS(self, Inode, nodeVal, showStack=False, sort='ASC'):
        stack = []
        queue = []
        visited = []
        found = []
        curNode = None

        queue.append(Inode)
        print(Inode)
        print(Inode.children)

        stack.extend([
            f"Searching... {nodeVal} in {Inode.name}",
            f"Queue \t\t Current",
            f"{queue[0].name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

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
                stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")

        return (visited, found, stack)

    # Iterative Depth Search
    def IDS(self, Inode, nodeVal, maxLevel=3, showStack=False, sort='ASC'):

        stack = []
        visited = []
        found = []
        curNode = None
        curLevel = 0
        isDone = False

        stack.extend([
            f"Searching... {nodeVal} in {Inode.name}",
            f"Level {curLevel}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

        visited.append(Inode)

        if (Inode.name in nodeVal):
            found.append(Inode.name)
            if (showStack):
                print(f"[] \t\t {Inode.name} *")
            stack.append(f"[] \t\t {Inode.name} *")
        else:
            if (showStack):
                print(f"[] \t\t {Inode.name}")
            stack.append(f"[] \t\t {Inode.name} *")
        if len(found) == len(nodeVal):
            return (visited, found)
        curLevel += 1

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
            
            stack.extend([
                f"\nSearching... {nodeVal} in {Inode.name}",
                f"Level {curLevel}",
                f"Queue \t\t Current",
                f"{list(map(lambda node: node.name, queue))}"
            ])
            
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
                    stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {node.name} *")
                else:
                    if (showStack):
                        # queue = list(set(queue) - set(iVisited))
                        print(f"{list(map(lambda node: node.name, queue))} \t\t {node.name}")
                    stack.append(f"{list(map(lambda node: node.name, queue))} \t\t {node.name}")

            curLevel += 1
        return (visited, found, stack)

    # Uniform Cost Search
    def UCS(self, Inode, nodeVal, showStack=False, sort='ASC'):
        stack = []
        queue_dict = {}
        visited = []
        found = []

        queue_dict[Inode] = 0
        stack.extend([
            f"Searching... {nodeVal} in {Inode.name}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

        while (len(queue_dict) and (len(found) != len(nodeVal))):
            curNode = max(queue_dict, key=queue_dict.get)  # 'min' or 'max'

            visited.append(curNode)
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = curNode.pesos[child] + \
                        queue_dict[curNode]
            print(f"{curNode.name}  ? {nodeVal} [{type(nodeVal)}] [{type(nodeVal[0])}]: {curNode.name in nodeVal}")
            if (curNode.name in nodeVal):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found, stack)

    # Gradient Search
    def GS(self, Inode, showStack=False, sort='ASC'):
        stack = []
        queue_dict = {}
        visited = []
        found = []

        queue_dict[Inode] = Inode.value

        stack.extend([
            f"Searching... in {Inode.name}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)    

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max'
            queue_dict = {}
            visited.append(curNode)
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = child.value

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

        return (visited, found, stack)

    # Gradient Search
    def Greedy(self, Inode, showStack=False, sort='ASC'):
        stack = []
        queue_dict = {}
        visited = []
        found = []

        queue_dict[Inode] = Inode.value

        stack.extend([
            f"Searching... in {Inode.name}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)    

        while len(queue_dict):
            curNode = min(queue_dict, key=queue_dict.get)  # 'min' or 'max'
            queue_dict = {}
            visited.append(curNode)
            for child in curNode.children:
                if child not in visited:
                    queue_dict[child] = child.value

            if (curNode.value == 0):
                found.append(curNode.name)
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

        return (visited, found, stack)

    def BestFS(self, Inode, showStack=False, sort='ASC'):
        stack = []
        queue_dict = {}
        visited = []
        found = []

        queue_dict[Inode] = Inode.value

        stack.extend([
            f"Searching... in {Inode.name}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

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
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found, stack)

    def A(self, Inode, showStack=False, sort='ASC'):
        stack = []
        queue_dict = {}
        visited = []
        found = []

        queue_dict[Inode] = Inode.value

        stack.extend([
            f"Searching... in {Inode.name}",
            f"Queue \t\t Current",
            f"{Inode.name}"
        ])

        if (showStack):
            for row in stack:
                print(row)

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
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")
                stack.append(f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found, stack)

    def sortDESC(self, a, b):
        if a.name > b.name:
            return -1

        if a.name < b.name:
            return 1

        return 0

    def sortASC(self, a, b):
        if a.name > b.name:
            return 1

        if a.name < b.name:
            return -1

        return 0

     # Bidireccionar

    def BDS(self, Inode, nodeVal, showStack=False, sort='ASC'):
        stack = []
        queueTB = []
        queueBT = []
        visitedTB = []
        visitedBT = []
        curNodeTB = None
        curNodeBT = None

        queueTB.append(Inode)
        queueBT.append(nodeVal)

        stack.extend([
            f"Searching... {nodeVal} in {Inode.name}",
            f"Queue Top-Bottom \t\t Current",
            f"{queueTB[0].name}",
            f"Searching... {Inode.name} in {nodeVal.name}",
            f"Queue Bottom-TOP \t\t Current",
            f"{queueBT[0].name}",
            '\n'
        ])

        if (showStack):
            for row in stack:
                print(row)

        while len(queueTB) and len(queueBT):

            # Top-Bottom
            curNodeTB = queueTB.pop(-1)

            visitedTB.append(curNodeTB)

            if (sort == 'ASC'):
                curNodeTB.children.sort(key=lambda x: x.name, reverse=False)
            else:
                curNodeTB.children.sort(key=lambda x: x.name, reverse=True)

            for child in curNodeTB.children:
                if child not in visitedTB:
                    queueTB.insert(0, child)

            # Bottom-Top
            curNodeBT = queueBT.pop(-1)

            visitedBT.insert(0, curNodeBT)

            if (sort == 'ASC'):
                curNodeBT.children.sort(key=lambda x: x.name, reverse=False)
            else:
                curNodeBT.children.sort(key=lambda x: x.name, reverse=True)

            for child in curNodeBT.parents:
                if child not in visitedBT:
                    queueBT.insert(0, child)

            # Compare
            stack.append(f"Queue Top-Bottom \t\t Current")
            if not set(queueBT).isdisjoint(queueTB):
                stack.append(f"{list(map(lambda node: node.name, queueTB))}** \t\t {curNodeTB.name}")
            else:
                stack.append(f"{list(map(lambda node: node.name, queueTB))} \t\t {curNodeTB.name}")

            stack.append(f"Queue Bottom-Top \t\t Current")
            if not set(queueBT).isdisjoint(queueTB):
                stack.append(f"{list(map(lambda node: node.name, queueBT))}** \t\t {curNodeBT.name}")
            else:
                stack.append(f"{list(map(lambda node: node.name, queueBT))} \t\t {curNodeBT.name}")


            if (showStack):
                print(f"Queue Top-Bottom \t\t Current")
                if not set(queueBT).isdisjoint(queueTB):
                    print(f"{list(map(lambda node: node.name, queueTB))}** \t\t {curNodeTB.name}")
                else:
                    print(f"{list(map(lambda node: node.name, queueTB))} \t\t {curNodeTB.name}")

                print(f"Queue Bottom-Top \t\t Current")
                if not set(queueBT).isdisjoint(queueTB):
                    print(f"{list(map(lambda node: node.name, queueBT))}** \t\t {curNodeBT.name}")
                else:
                    print(f"{list(map(lambda node: node.name, queueBT))} \t\t {curNodeBT.name}")

            if not set(queueBT).isdisjoint(queueTB):
                return ((visitedTB, visitedBT), [nodeVal.name], stack)

        return ((visitedTB, visitedBT), [None], stack)


if __name__ == '__main__':
    import Node as Node
    t = Node.Node("T", 20)
    n0 = Node.Node("n0", 14)
    n1 = Node.Node("n1", 13)
    n2 = Node.Node("n2", 12)
    n3 = Node.Node("n3", 11)
    n4 = Node.Node("n4", 0)
    n5 = Node.Node("n5", 17)
    n6 = Node.Node("n6", 10)


    t.addChildren([n0, n1, n2], [3, 2, 5])
    n2.addChildren([n3, n6], [7, 5])
    n3.addChildren([n4, n5], [2, 4])

    search = Search()
    path, found, stack = search.DFS(t, ['n6'], False, 'ASC')
    for row in stack:
       print(row)
