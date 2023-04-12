import heapq
import distance

class Astar:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.frontier = [(0, 0, start, [start])] # fn, gn, current, path
        self.explored = []
        self.final_path = []
        self.total_cost = 0

    # Mencari path dari start ke goal dan return True jika path ditemukan dan False jika tidak
    def search(self):
        while self.frontier:
            fn, gn, current, path = heapq.heappop(self.frontier)
            self.explored.append(current)

            if current == self.goal:
                self.final_path = path
                self.total_cost = fn  # or gn
                return True
            
            for i in range(len(current.neighbour)):
                neighbour = current.neighbour[i][0]
                if neighbour not in self.explored:
                    new_gn = gn + current.neighbour[i][1]
                    if self.graph.type == "map":
                        new_fn = new_gn + distance.haversine(neighbour, self.goal)
                        heapq.heappush(self.frontier, (new_fn, new_gn, neighbour, path + [neighbour]))
                    elif self.graph.type == "normal":
                        new_fn = new_gn + distance.euclidean(neighbour, self.goal)
                        heapq.heappush(self.frontier, (new_fn, new_gn, neighbour, path + [neighbour]))

        return False
    
    # Mencetak path dan jaraknya
    def printAnswer(self):
        print("Path: ", end="")
        for i in range(len(self.final_path)):
            if i != len(self.final_path) - 1:
                print(self.final_path[i].name, end=" -> ")
            else:
                print(self.final_path[i].name)
        if self.graph.type == "map":
            print("Distance: " + str(self.total_cost) + " m") # Penambahan satuan meter
        elif self.graph.type == "normal":
            print("Distance: " + str(self.total_cost))

    # Mengembalikan path akhir (mungkin kosong)
    def getPath(self):
        return self.final_path