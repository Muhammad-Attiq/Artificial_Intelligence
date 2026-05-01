import random

class GA:
    def __init__(self, individualSize, populationSize):
        self.population = dict()
        self.individualSize = individualSize
        self.populationSize = populationSize
        self.totalFitness = 0
        i = 0
        while i < populationSize:
            listOfBits = [0] * individualSize
            listOfLocations = list(range(0, individualSize))
            numberOfOnes = random.randint(0, individualSize - 1)
            onesLocations = random.sample(listOfLocations, numberOfOnes)
            for j in onesLocations:
                listOfBits[j] = 1
            self.population[i] = [listOfBits, numberOfOnes]
            self.totalFitness = self.totalFitness + numberOfOnes
            i = i + 1

    def updatePopulationFitness(self):
        self.totalFitness = 0
        for individual in self.population:
            individualFitness = sum(self.population[individual][0])
            self.population[individual][1] = individualFitness
            self.totalFitness = self.totalFitness + individualFitness

    def selectParents(self):
        rouletteWheel = []
        wheelSize = self.populationSize * 5
        h_n = []
        for individual in self.population:
            h_n.append(self.population[individual][1])
        j = 0
        for individual in self.population:
            if sum(h_n) > 0:
                individualLength = round(wheelSize * (h_n[j] / sum(h_n)))
            else:
                individualLength = 0
            j = j + 1
            if individualLength > 0:
                i = 0
                while i < individualLength:
                    rouletteWheel.append(individual)
                    i = i + 1
        if len(rouletteWheel) == 0:
            # If roulette wheel is empty, add all individuals
            for individual in self.population:
                rouletteWheel.append(individual)
        random.shuffle(rouletteWheel)
        parentIndices = []
        i = 0
        while i < self.populationSize:
            parentIndices.append(rouletteWheel[random.randint(0, len(rouletteWheel) - 1)])
            i = i + 1
        newGeneration = dict()
        i = 0
        while i < self.populationSize:
            newGeneration[i] = self.population[parentIndices[i]].copy()
            i = i + 1
        del self.population
        self.population = newGeneration.copy()
        self.updatePopulationFitness()

    def generateChildren(self, crossoverProbability):
        numberOfPairs = round(crossoverProbability * self.populationSize / 2)
        individualIndices = list(range(0, self.populationSize))
        random.shuffle(individualIndices)
        i = 0
        j = 0
        while i < numberOfPairs and j + 1 < self.populationSize:
            crossoverPoint = random.randint(0, self.individualSize - 1)
            child1 = self.population[j][0][0:crossoverPoint] + self.population[j + 1][0][crossoverPoint:]
            child2 = self.population[j + 1][0][0:crossoverPoint] + self.population[j][0][crossoverPoint:]
            self.population[j] = [child1, sum(child1)]
            self.population[j + 1] = [child2, sum(child2)]
            i = i + 1
            j = j + 2
        self.updatePopulationFitness()

    def mutateChildren(self, mutationProbability):
        for individual in self.population:
            for bitIndex in range(self.individualSize):
                if random.random() < mutationProbability:
                    # Flip the bit
                    self.population[individual][0][bitIndex] = 1 - self.population[individual][0][bitIndex]
            # Update fitness after mutation
            self.population[individual][1] = sum(self.population[individual][0])
        self.updatePopulationFitness()


# Main execution
if __name__ == "__main__":
    individualSize, populationSize = 8, 10
    i = 0
    instance = GA(individualSize, populationSize)

    while True:
        instance.selectParents()
        instance.generateChildren(0.8)
        instance.mutateChildren(0.03)

        print(f"\n--- Generation {i} ---")
        print("Population:")
        for idx in instance.population:
            print(f"  Individual {idx}: {instance.population[idx][0]} (Fitness: {instance.population[idx][1]})")
        print(f"Total Fitness: {instance.totalFitness}")
        print(f"Average Fitness: {instance.totalFitness / populationSize:.2f}")
        print(f"Max Fitness: {max(instance.population[idx][1] for idx in instance.population)}")

        i = i + 1

        # Check if solution found
        found = False
        for individual in instance.population:
            if instance.population[individual][1] == individualSize:
                found = True
                break

        if found:
            print(f"\n*** SOLUTION FOUND! ***")
            print(f"Perfect individual found at generation {i}")
            break

        # Optional: stop after too many generations to avoid infinite loop
        if i > 1000:
            print("\nStopping after 1000 generations - solution not found")
            break
