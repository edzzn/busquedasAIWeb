class Search:
    def DFS(self, Inode, nodeVal=[], showStack=False, sort='ASC'):
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
                    print(
                        f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")

        return (visited, found)

    def BFS(self, Inode, nodeVal, showStack=False, sort='ASC'):
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
                    print(
                        f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name, queue))} \t\t {curNode.name}")

        return (visited, found)

    # Iterative Depth Search
    def IDS(self, Inode, nodeVal, maxLevel=3, showStack=False, sort='ASC'):

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

                        print(
                            f"{list(map(lambda node: node.name, queue))} \t\t {node.name} *")
                else:
                    if (showStack):
                        # queue = list(set(queue) - set(iVisited))
                        print(
                            f"{list(map(lambda node: node.name, queue))} \t\t {node.name}")

            curLevel += 1
        return (visited, found)

    # Uniform Cost Search
    def UCS(self, Inode, nodeVal, showStack=False, sort='ASC'):
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
                    queue_dict[child] = curNode.pesos[child] + \
                        queue_dict[curNode]

            if (curNode.name in nodeVal):
                found.append(curNode.name)
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found)

    # Gradient Search
    def GS(self, Inode, showStack=False, sort='ASC'):
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
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

        return (visited, found)

    def BestFS(self, Inode, showStack=False, sort='ASC'):
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
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

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
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

        return (visited, found)

    def A(self, Inode, showStack=False, sort='ASC'):
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
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name} *")
            else:
                if (showStack):
                    print(
                        f"{list(map(lambda node: node.name + '(' +str(queue_dict[node]) + ')', queue_dict))} \t\t {curNode.name}")

            # Eliminamos al nodo del diccionario
            del queue_dict[curNode]

        return (visited, found)

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

            visitedBT.insert(0, curNodeBT)

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
                    print(
                        f"{list(map(lambda node: node.name, queueTB))}** \t\t {curNodeTB.name}")
                else:
                    print(
                        f"{list(map(lambda node: node.name, queueTB))} \t\t {curNodeTB.name}")

                print(f"Queue Botton-Top \t\t Current")
                if not set(queueBT).isdisjoint(queueTB):
                    print(
                        f"{list(map(lambda node: node.name, queueBT))}** \t\t {curNodeBT.name}")
                else:
                    print(
                        f"{list(map(lambda node: node.name, queueBT))} \t\t {curNodeBT.name}")

            if not set(queueBT).isdisjoint(queueTB):
                return ((visitedTB, visitedBT), [nodeVal.name])

        return ((visitedTB, visitedBT), ['s'])
