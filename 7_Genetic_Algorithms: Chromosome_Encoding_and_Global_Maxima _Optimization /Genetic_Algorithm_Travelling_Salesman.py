import random, math

class TSP_GA:
    def __init__(self, cities, popSize):
        self.cities = cities
        self.n = len(cities)
        self.popSize = popSize
        self.pop = []
        for _ in range(popSize):
            route = list(range(self.n))
            random.shuffle(route)
            self.pop.append(route)

    def distance(self, route):
        total = 0
        for i in range(self.n):
            x1,y1 = self.cities[route[i]]
            x2,y2 = self.cities[route[(i+1)%self.n]]
            total += math.hypot(x2-x1, y2-y1)
        return total

    def fitness(self, route):
        return 1.0 / self.distance(route)

    def select(self):
        scores = [self.fitness(r) for r in self.pop]
        total = sum(scores)
        if total == 0:
            return random.choice(self.pop)
        r = random.uniform(0, total)
        s = 0
        for i, score in enumerate(scores):
            s += score
            if s >= r:
                return self.pop[i][:]
        return self.pop[-1][:]

    def crossover(self, p1, p2):
        start = random.randint(0, self.n-1)
        end = random.randint(start, self.n-1)
        child = [-1]*self.n
        for i in range(start, end+1):
            child[i] = p1[i]
        pos = 0
        for i in range(self.n):
            if child[i] == -1:
                while p2[pos] in child:
                    pos += 1
                child[i] = p2[pos]
        return child

    def mutate(self, route):
        if random.random() < 0.02:
            i,j = random.sample(range(self.n), 2)
            route[i], route[j] = route[j], route[i]
        return route

    def evolve(self, gens=200):
        for _ in range(gens):
            newPop = []
            for _ in range(self.popSize):
                p1,p2 = self.select(), self.select()
                child = self.crossover(p1,p2)
                child = self.mutate(child)
                newPop.append(child)
            self.pop = newPop
        best = min(self.pop, key=self.distance)
        return best, self.distance(best)

cities = [(0,0),(0.2,0.2),(0.4,0.4),(0.6,0.6),(0.8,0.8),(1,1),(1.2,0),(0,0.8),(0.3,0.5),(0.7,0.3)]
ga = TSP_GA(cities, 50)
bestRoute, bestDist = ga.evolve(300)
print(f"Best distance: {bestDist:.3f}")
print(f"Route: {bestRoute}")
