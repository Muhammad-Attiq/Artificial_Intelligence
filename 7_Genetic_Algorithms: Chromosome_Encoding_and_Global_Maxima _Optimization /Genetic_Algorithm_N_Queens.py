import random
import math

class queensGA:
    def __init__(self, individualSize, populationSize):
        self.population = dict()
        self.individualSize = individualSize
        self.populationSize = populationSize
        self.totalFitness = 0
        i = 0
        while i < populationSize:
            individualArray = [0] * individualSize
            j = 0
            while j < individualSize:
                value = random.randint(0, individualSize-1)
                individualArray[j] = value
                j = j + 1
            self.population[i] = [individualArray.copy(), 0]
            i = i + 1
        self.updatePopulationFitness()

    def updateIndividualFitness(self, individualArray):
        i = 0
        fitnessValue = 0
        while i < self.individualSize:
            j = 0
            while j < self.individualSize:
                if i != j:
                    if individualArray[j] == individualArray[i]:
                        fitnessValue = fitnessValue + 1
                    elif individualArray[j] == individualArray[i] - abs(j-i):
                        fitnessValue = fitnessValue + 1
                    elif individualArray[j] == individualArray[i] + abs(j-i):
                        fitnessValue = fitnessValue + 1
                j = j + 1
            i = i + 1
        return fitnessValue

    def updatePopulationFitness(self):
        self.totalFitness = 0
        for individual in self.population:
            individualFitness = self.updateIndividualFitness(self.population[individual][0])
            self.population[individual][1] = individualFitness
            self.totalFitness = self.totalFitness + individualFitness

    def selectParents(self):
        rouletteWheel = []
        wheelSize = self.populationSize * 5
        h_n = []
        for individual in self.population:
            # Avoid division by zero
            if self.population[individual][1] == 0:
                h_n.append(float('inf'))
            else:
                h_n.append(1.0 / self.population[individual][1])

        # Handle case where all fitness values are 0
        if sum(h_n) == float('inf'):
            h_n = [1.0] * len(self.population)

        j = 0
        for individual in self.population:
            if sum(h_n) > 0:
                individualFitness = round(wheelSize * (h_n[j] / sum(h_n)))
            else:
                individualFitness = 0
            j = j + 1
            if individualFitness > 0:
                i = 0
                while i < individualFitness:
                    rouletteWheel.append(individual)
                    i = i + 1

        # If roulette wheel is empty, add all individuals
        if len(rouletteWheel) == 0:
            for individual in self.population:
                rouletteWheel.append(individual)

        random.shuffle(rouletteWheel)
        parentIndices = []
        i = 0
        while i < self.populationSize:
            parentIndices.append(rouletteWheel[random.randint(0, len(rouletteWheel)-1)])
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
            child1 = self.population[j][0][0:crossoverPoint] + self.population[j+1][0][crossoverPoint:]
            child2 = self.population[j+1][0][0:crossoverPoint] + self.population[j][0][crossoverPoint:]
            self.population[j] = [child1, 0]
            self.population[j+1] = [child2, 0]
            i = i + 1
            j = j + 2
        self.updatePopulationFitness()

    def mutateChildren(self, mutationProbability):
        numberOfBits = round(mutationProbability * self.populationSize * self.individualSize)
        totalIndices = list(range(0, self.populationSize * self.individualSize))
        random.shuffle(totalIndices)
        swapLocations = random.sample(totalIndices, min(numberOfBits, len(totalIndices)))
        for loc in swapLocations:
            individualIndex = math.floor(loc / self.individualSize)
            bitIndex = math.floor(loc % self.individualSize)
            value = random.randint(0, self.individualSize - 1)
            while value == self.population[individualIndex][0][bitIndex]:
                value = random.randint(0, self.individualSize - 1)
            self.population[individualIndex][0][bitIndex] = value
        self.updatePopulationFitness()

# Main execution
individualSize, populationSize = 8, 16
i = 0
instance = queensGA(individualSize, populationSize)

print("Starting Genetic Algorithm for 8-Queens Problem")
print("="*60)

while True:
    instance.selectParents()
    instance.generateChildren(0.5)
    instance.mutateChildren(0.03)

    if i % 20 == 0:
        print(f"\nGeneration {i}:")
        print(f"Best Fitness (lowest is better): {min(instance.population[ind][1] for ind in instance.population)}")
        print(f"Total Fitness: {instance.totalFitness}")

    # Check if solution found (fitness = 0 means no conflicts)
    found = False
    for individual in instance.population:
        if instance.population[individual][1] == 0:
            found = True
            solution = instance.population[individual][0]
            break

    if found:
        print("\n" + "="*60)
        print(f"SOLUTION FOUND at Generation {i}!")
        print(f"Queen positions (by column): {solution}")
        print("\nVisual representation (0 = empty, Q = Queen):")
        print("-"*60)

        # Display the chessboard
        for row in range(individualSize):
            line = ""
            for col in range(individualSize):
                if solution[col] == row:
                    line += " Q "
                else:
                    line += " . "
            print(line)

        print("-"*60)
        print(f"Total Fitness: {instance.totalFitness}")
        break

    i = i + 1

    # Safety break to prevent infinite loop
    if i > 5000:
        print("\nMaximum generations reached without finding perfect solution.")
        print(f"Best solution found (fitness = conflicts):")
        best_fitness = float('inf')
        best_solution = None
        for individual in instance.population:
            if instance.population[individual][1] < best_fitness:
                best_fitness = instance.population[individual][1]
                best_solution = instance.population[individual][0]

        print(f"Queen positions: {best_solution}")
        print(f"Conflicts: {best_fitness}")
        break
