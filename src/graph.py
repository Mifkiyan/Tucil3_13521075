class Graph(object):
    def __init__(self, numOfLocation):
        self.numOfLocation = numOfLocation
        self.locationList = []

    def addLocation(self, location):
        self.locationList.append(location)

    def addNeighbours(self, matrix):
        for i in range(self.numOfLocation):
            for j in range(self.numOfLocation):
                if matrix[i][j] != 0 :
                    self.locationList[i].addNeighbour(self.locationList[j])

    def printGraph(self):
        print("Daftar Lokasi: ")
        for location in self.locationList:
            location.print()
            print()
            
class Location(object): # Representasi dari sebuah simpul
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbour = []
    
    def addNeighbour(self, location):
        self.neighbour.append(location)

    def print(self):
        print("Nama Lokasi:", self.name)
        print("Latitude:", self.latitude)
        print("Longitude:", self.longitude)
        print("Tetangga: ", end="")
        for i in range(len(self.neighbour)):
            if i != len(self.neighbour) - 1:
                print(self.neighbour[i].name, end=", ")
            else:
                print(self.neighbour[i].name)
