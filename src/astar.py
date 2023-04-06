import heapq
import haversine

class Astar:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.frontier = [(0, 0, start, [start])] # fn, gn, current, path
        self.explored = []
        self.final_path = []
        self.total_cost = 0

    def search(self):
        while self.frontier:
            fn, gn, current, path = heapq.heappop(self.frontier)
            self.explored.append(current)

            if current == self.goal:
                self.final_path = path
                self.total_cost = fn
                return True

            for neighbour in current.neighbour:
                if neighbour not in self.explored:
                    new_gn = gn + haversine.haversine_distance(current, neighbour)
                    new_fn = new_gn + haversine.haversine_distance(neighbour, self.goal)
                    heapq.heappush(self.frontier, (new_fn, new_gn, neighbour, path + [neighbour]))

        return False
    
    def printAnswer(self):
        print("Path: ", end="")
        for i in range(len(self.final_path)):
            if i != len(self.final_path) - 1:
                print(self.final_path[i].name, end=" -> ")
            else:
                print(self.final_path[i].name)
        print("Distance: " + str(self.total_cost) + " m")