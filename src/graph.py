class Graph(object):
    def __init__(self, type, numOfNode):
        self.type = type # Tipe tergantung antara untuk map atau graph biasa
        self.numOfNode = numOfNode
        self.nodeList = []

    def addNode(self, Node):
        self.nodeList.append(Node)
    
    def addNodeNeighbours(self, matrix):
        for i in range(self.numOfNode):
            for j in range(self.numOfNode):
                if matrix[i][j] != 0:
                    self.nodeList[i].addNeighbour(self.nodeList[j], matrix[i][j])

    def printAllNode(self):
        print("Daftar Node: ")
        for node in self.nodeList:
            node.print()
            print()

    def findNode(self, nodeName):
        for node in self.nodeList:
            if node.name == nodeName:
                return node
        return None
        
class Node(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x # Latitude untuk map
        self.y = y # Longitude untuk map
        self.neighbour = [] # neighbour berisi objek Node dan jaraknya
    
    # Untuk sorting apabila terdapat cost yang memiliki nilai yang sama
    def __ls__(self, other):
        return self.name < other.name
    
    def addNeighbour(self, node, distance):
        self.neighbour.append([node, distance])

    def print(self):
        print("Nama Node:", self.name)
        print("Koordinat:", self.x, self.y)
        print("Tetangga: ", end="")
        for i in range(len(self.neighbour)):
            if i != len(self.neighbour) - 1:
                print(self.neighbour[i][0].name + " (" + str(self.neighbour[i][1]) + ")", end=", ")
            else:
                print(self.neighbour[i][0].name + " (" + str(self.neighbour[i][1]) + ")")

    def getDistanceNeighbour(self, neighbour):
        for i in range(len(self.neighbour)):
            if self.neighbour[i][0] == neighbour:
                return self.neighbour[i][1]