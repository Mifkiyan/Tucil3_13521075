from graph import Graph, Location
from ucs import UCS
from astar import Astar
import folium
from flask import Flask, render_template

app = Flask(__name__, template_folder="visual")

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
graph.printAllNode()

start = input("Masukkan nama titik awal: ")
end = input("Masukkan nama titik akhir: ")
while graph.findLocation(start) == None or graph.findLocation(end) == None:
    print("Titik awal dan/atau titik akhir tidak ditemukan, coba lagi\n")
    start = input("Masukkan nama titik awal: ")
    end = input("Masukkan nama titik akhir: ")

Algorithm = input("Masukkan algoritma yang ingin digunakan (UCS/A*): ")
while Algorithm != "UCS" and Algorithm != "A*" and Algorithm != "ucs" and Algorithm != "a*":
    print("Masukan salah, coba lagi\n\n")
    Algorithm = input("Masukkan algoritma yang ingin digunakan (UCS/A*): ")

if Algorithm == "UCS" or Algorithm == "ucs":
    algorithm = UCS(graph, graph.findLocation(start), graph.findLocation(end))
elif Algorithm == "A*" or Algorithm == "a*":
    algorithm = Astar(graph, graph.findLocation(start), graph.findLocation(end))

if not algorithm.search():
    print("\nPath tidak ditemukan")

@app.route('/')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    start_coords = [graph.findLocation(start).latitude, graph.findLocation(start).longitude]
    map = folium.Map(location=start_coords, zoom_start=500)

    # Add all markers to the map
    for location in graph.locationList:
        folium.Marker([location.latitude, location.longitude], popup=location.name).add_to(map)

    # Add a line between the markers
    for location in graph.locationList:
        for neighbour in location.neighbour:
            folium.PolyLine(locations=[[location.latitude, location.longitude], [neighbour.latitude, neighbour.longitude]], color='black').add_to(map)

    path = algorithm.getPath()

    if path != None:
        print()
        algorithm.printAnswer()
        for i in range(len(path)-1):
            folium.PolyLine(locations=[[path[i].latitude, path[i].longitude], [path[i+1].latitude, path[i+1].longitude]], color='red').add_to(map)

    map.save('src/visual/map.html')

    if path == None:
        ans = input("Apakah Anda tetap ingin melihat visualisasi graph-Nya? (Y/n): ")
    elif path != None:
        ans = input("Apakah Anda ingin melihat visualisasi path-Nya? (Y/n): ")
    
    while ans != "Y" and ans != "y" and ans != "N" and ans != "n":
        print("Masukan salah, coba lagi\n\n")
        if path == None:
            ans = input("Apakah Anda tetap ingin melihat visualisasi graph-Nya? (Y/n): ")
        elif path != None:
            ans = input("Apakah Anda ingin melihat visualisasi path-Nya? (Y/n): ")
    
    if ans == "Y" or ans == "y":
        app.run(debug=False)
