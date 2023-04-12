import heapq
import distance

class UCS:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.frontier = [(0, start, [start])] # cost, current, path
        self.explored = []
        self.final_path = []
        self.total_cost = 0
    
    # Mencari path dari start ke goal dan return True jika path ditemukan dan False jika tidak
    def search(self):
        while self.frontier:
            current_cost, current, path = heapq.heappop(self.frontier)
            self.explored.append(current)

            if current == self.goal:
                self.final_path = path
                self.total_cost = current_cost
                return True

            for i in range(len(current.neighbour)):
                neighbour = current.neighbour[i][0]
                if neighbour not in self.explored:
                    new_cost = current_cost + current.neighbour[i][1]
                    heapq.heappush(self.frontier, (new_cost, neighbour, path + [neighbour]))

        return False
    
    def printAnswer(self):
        print("Path: ", end="")
        for i in range(len(self.final_path)):
            if i != len(self.final_path) - 1:
                print(self.final_path[i].name, end=" -> ")
            else:
                print(self.final_path[i].name)
        if self.graph.type == "map":
            print("Distance: " + str(self.total_cost) + " m")
        elif self.graph.type == "matriks":
            print("Distance: " + str(self.total_cost))

    def getPath(self):
        return self.final_path