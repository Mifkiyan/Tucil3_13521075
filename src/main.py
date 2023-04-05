from graph import Graph, Location

def makeGraphFromFile(file):
    fileLines = file.read().splitlines()
    numOfPlace = int(fileLines[0])
    locationList = fileLines[1:numOfPlace+1]
    readMatrix = fileLines[numOfPlace+1:]
    adjacencyMatrix = [[0 for i in range(numOfPlace)] for j in range(numOfPlace)]

    graph = Graph(numOfPlace)

    for i in range(numOfPlace):
        splitString = locationList[i].split(", ")
        nameOfLocation = splitString[0]
        latitudeOfLocation = float(splitString[1])
        longitudeOfLocation = float(splitString[2])
        newLocation = Location(nameOfLocation, latitudeOfLocation, longitudeOfLocation)
        graph.addLocation(newLocation)
        adjacencyMatrix[i] = [int(x) for x in readMatrix[i].split(" ")]

    graph.addNeighbours(adjacencyMatrix)
    
    return graph


while True:
    filename = input("Masukkan nama file: ")
    try:
        file = open("test/" + filename + ".txt")
    except FileNotFoundError:
        print("File tidak ditemukan, coba lagi\n")
    else:
        break

graph = makeGraphFromFile(file)
graph.printGraph()