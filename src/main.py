from graph import Graph, Node
from ucs import UCS
from astar import Astar
import matplotlib.pyplot as plt
import networkx as nx
import folium
from flask import Flask, render_template

# Membuat graph dari matriks berbobot
def makeGraphFromFile(file, type):
    # Membaca file dan inisiasi graph kosong
    fileLines = file.read().splitlines()
    numOfPlace = int(fileLines[0])
    locationList = fileLines[1:numOfPlace+1]
    readMatrix = fileLines[numOfPlace+1:]
    adjacencyMatrix = [[0 for i in range(numOfPlace)] for j in range(numOfPlace)]

    graph = Graph(type, numOfPlace)

    # Membuat objek Node dan menambahkan ke graph
    for i in range(numOfPlace):
        splitString = locationList[i].split(", ")
        nameOfNode = splitString[0]
        xOfNode = float(splitString[1])
        yOfNode = float(splitString[2])
        newNode = Node(nameOfNode, xOfNode, yOfNode)
        graph.addNode(newNode)
        adjacencyMatrix[i] = [int(x) for x in readMatrix[i].split(" ")]

    graph.addNodeNeighbours(adjacencyMatrix)

    return graph

def visualizeGraph(graph, path): # Hanya untuk graf biasa
    G = nx.Graph()
    for node in graph.nodeList:
        G.add_node(node.name, pos=(node.x, node.y))
        for neighbour in node.neighbour:
            G.add_edge(node.name, neighbour[0].name, weight=neighbour[1], color='black')
        
    
    # Warna hitam untuk jalur yang tidak dipilih dan merah untuk jalur yang dipilih
    for i in range(len(path) - 1):
        G.remove_edge(path[i].name, path[i+1].name)
        G.add_edge(path[i].name, path[i+1].name, weight=path[i].getDistanceNeighbour(path[i+1]), color='red')
    # Warna biru untuk node yang tidak ada di jalur dan merah untuk node yang ada di jalur
    # node_colors = ['red' if node in path else 'blue' for node in G.nodes()]

    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = nx.get_edge_attributes(G, 'color').values()
    nx.draw(G, pos,with_labels=True,edge_color=edge_colors,
            node_size=1000,font_color="white",font_size=20,
            font_family="Times New Roman", font_weight="bold",width=5)
    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=10)
    plt.show()


inputType = input("Masukan berupa graph biasa atau map (Biasa/Map)? ")
while inputType != "Biasa" and inputType != "Map" and inputType != "biasa" and inputType != "map":
    print("Masukan salah, coba lagi\n")
    inputType = input("Masukan berupa graph biasa atau map (Biasa/Map)? ")

while True:
    filename = input("Masukkan nama file: ")
    try:
        if inputType == "Matriks" or inputType == "matriks":
            file = open("test/matriks/" + filename + ".txt")
        elif inputType == "Map" or inputType == "map":
            file = open("test/map/" + filename + ".txt")
    except FileNotFoundError:
        print("File tidak ditemukan, coba lagi\n")
    else:
        break

if inputType == "Matriks" or inputType == "matriks":
    graph = makeGraphFromFile(file, "matriks")
elif inputType == "Map" or inputType == "map":
    graph = makeGraphFromFile(file, "map")

graph.printAllNode()

start = input("Masukkan nama titik awal: ")
end = input("Masukkan nama titik akhir: ")
while graph.findNode(start) == None or graph.findNode(end) == None:
    print("Titik awal dan/atau titik akhir tidak ditemukan, coba lagi\n")
    start = input("Masukkan nama titik awal: ")
    end = input("Masukkan nama titik akhir: ")

Algorithm = input("Masukkan algoritma yang ingin digunakan (UCS/A*): ")
while Algorithm != "UCS" and Algorithm != "A*" and Algorithm != "ucs" and Algorithm != "a*":
    print("Masukan salah, coba lagi\n")
    Algorithm = input("Masukkan algoritma yang ingin digunakan (UCS/A*): ")

if Algorithm == "UCS" or Algorithm == "ucs":
    algorithm = UCS(graph, graph.findNode(start), graph.findNode(end))
elif Algorithm == "A*" or Algorithm == "a*":
    algorithm = Astar(graph, graph.findNode(start), graph.findNode(end))

if inputType == "Matriks" or inputType == "matriks":
    if algorithm.search():
        algorithm.printAnswer()
        visualizeGraph(graph, algorithm.getPath())
    else:
        print("Path tidak ditemukan")

elif inputType == "Map" or inputType == "map":
    # Initialize Flask and render map
    app = Flask(__name__, template_folder="visual")

    @app.route('/')
    def map():
        return render_template('map.html')

    if not algorithm.search():
        print("\nPath tidak ditemukan")

    # Menampilkan kooridnat awal
    start_coords = [graph.findNode(start).x, graph.findNode(start).y]
    map = folium.Map(location=start_coords, zoom_start=500)

    # Menambahkan marker dan garis hitam antar semua Location
    for location in graph.nodeList:
        folium.Marker([location.x, location.y], popup=location.name).add_to(map)

    for location in graph.nodeList:
        for neighbour in location.neighbour:
            folium.PolyLine(locations=[[location.x, location.y], [neighbour[0].x, neighbour[0].y]], color='black').add_to(map)

    path = algorithm.getPath()

    # Menambahkan garis merah antar Location yang ada di path
    if path != None:
        print()
        algorithm.printAnswer()
        for i in range(len(path)-1):
            folium.PolyLine(locations=[[path[i].x, path[i].y], [path[i+1].x, path[i+1].y]], color='red').add_to(map)

    map.save('src/visual/map.html')

    if path == None:
        ans = input("Apakah Anda tetap ingin melihat visualisasi graph-Nya? (Y/n): ")
    elif path != None:
        ans = input("Apakah Anda ingin melihat visualisasi path-Nya? (Y/n): ")
    
    while ans != "Y" and ans != "y" and ans != "N" and ans != "n":
        print("Masukan salah, coba lagi\n")
        if path == None:
            ans = input("Apakah Anda tetap ingin melihat visualisasi graph-Nya? (Y/n): ")
        elif path != None:
            ans = input("Apakah Anda ingin melihat visualisasi path-Nya? (Y/n): ")
    
    if ans == "Y" or ans == "y":
        app.run(debug=False)