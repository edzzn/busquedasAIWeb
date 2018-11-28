class Node:
    def __init__(self, name, value=0, parent=[], *children):
        self.name = name
        self.value = value
        # self.peso = peso
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

    def addChildren(self, children, pesos=[]):
        # self.children.extend(children)

        for i, child in enumerate(children):
            if child not in self.children:
                self.children.append(child)
                
            if len(pesos) > i:
                self.pesos[child] = pesos[i]

            # print(
            #     f"Self: {self}, child: {child}, Child.Parents: {child.parents}")
            if self not in child.parents:
                child._addParents(self)

            # print('AFTER')
            # print(
            #     f"Self: {self}, child: {child}, Child.Parents: {child.parents}")

            # print('\n')

    def remove(self, child):
        self.children.remove(child)

    def maxDepth(self):
        currNode = Node(self.name, self.value, self.parents[:])
        for child in self.children:
            currNode.addChildren([child])
        currNodes = [currNode]
        max_depth = 0
        currChildren = []
        visited = []
        while currNodes:
            
            print('currNodes')
            print(currNodes)
            for node in currNodes:
                print('node')
                print(node)
                print('visited')
                print(visited)
                for child in node.children:
                    if child not in visited:
                        visited.append(child)
                        print('child')
                        print(visited)
                        currChildren.append(child)
                # node.children = []
            max_depth += 1
            currNodes = currChildren[:]
            currChildren = []

        return max_depth
