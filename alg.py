import pygame
import random

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)  
red = (255, 0, 0)    
blue = (0, 0, 255)   

# Define the maze as a 2D list (1 = wall, 0 = path, S = start, E = end)
maze_layout = [
    "11111111111111111111",
    "1S000000011000000001",
    "10111011101111111001",
    "10001000000001100001",
    "11101011111001101111",
    "10000010001000000001",
    "10111010101111111001",
    "10000010100000001001",
    "11111011101110111001",
    "100000000010000000E1",
    "11111111111111111111"
]

DIRECTIONS = {
    "U": (0, -1),  
    "D": (0, 1),   
    "L": (-1, 0),  
    "R": (1, 0)   
}

# Opposite directions (to prevent moving backward)
OPPOSITE_DIRECTIONS = {"U": "D", "D": "U", "L": "R", "R": "L"}

cell_size = 40  
circle_radius = 10 
rows = len(maze_layout)
cols = len(maze_layout[0])
width = cols * cell_size
height = rows * cell_size

POPULATION_SIZE = 500
PATH_LENGTH = 250  
SPEED = 0.1  

def draw_maze(surface):
    for y in range(rows):
        for x in range(cols):
            cell = maze_layout[y][x]
            if cell == "1":  
                pygame.draw.rect(surface, black, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == "S":  
                pygame.draw.rect(surface, green, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == "E":  
                pygame.draw.rect(surface, red, (x * cell_size, y * cell_size, cell_size, cell_size))

def can_move(x, y) -> bool:
    if 0 <= x < cols and 0 <= y < rows:  
        return maze_layout[y][x] in ["0", "S", "E"]
    return False

def generate_population():
    start_pos = (1, 1)  
    population = []

    for _ in range(POPULATION_SIZE):
        individual = []  
        x, y = start_pos  
        last_move = None  

        for _ in range(PATH_LENGTH):  
            possible_moves = list(DIRECTIONS.keys())

            if last_move:
                possible_moves.remove(OPPOSITE_DIRECTIONS[last_move])

            direction = random.choice(possible_moves)
            dx, dy = DIRECTIONS[direction]

            if can_move(x + dx, y + dy):
                x += dx
                y += dy
                individual.append(direction) 
                last_move = direction  
            else:
                individual.append("X")  

        population.append(individual)  

    return population

def draw_agent(surface, x, y, color):
    center_x = x * cell_size + cell_size // 2
    center_y = y * cell_size + cell_size // 2
    pygame.draw.circle(surface, color, (center_x, center_y), circle_radius)
    pygame.display.update()

def animate_population(surface, population):
    start_pos = (1, 1) 

    for individual in population:  # Animate only the last 3 individuals
        x, y = start_pos 
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 

        for move in individual:
            #pygame.time.delay(int(SPEED * 1000))  

            if move == "X":
                continue  

            dx, dy = DIRECTIONS[move]

            if can_move(x + dx, y + dy):
                x += dx
                y += dy
                draw_agent(surface, x, y, color)

        #pygame.time.delay(500)  
 

def fitness(individual):
    score = 0
    for move in individual:
        if move == "X":
            continue
        else:
            score = score + 10
    return score

def selection(population):
    scored_population = [(individual, fitness(individual)) for individual in population]
    scored_population.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness descending
    top_50_percent = scored_population[:len(scored_population) // 2]
    return [individual for individual, _ in top_50_percent]

def crossover(selected_population, CHROMO_LEN, population):
    offspring_cross = []
    for i in range(int(len(population))):
        parent1 = random.choice(selected_population)
        parent2 = random.choice(population)

        crossover_point = random.randint(1, CHROMO_LEN - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]

        offspring_cross.append(child)
    return offspring_cross

def mutate(population, mutation_rate):
    for individual in population:
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                possible_moves = list(DIRECTIONS.keys())
                individual[i] = random.choice(possible_moves)

    return population

def main():
    pygame.init()

    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Genetic Maze Algorithm')

    surface.fill(white) 
    draw_maze(surface)  

    population = generate_population()

    generations = 100
    last_generation = []

    
    for generation in range(generations):
        #print(f"Generation {generation + 1}")

        selected_population = selection(population)
       # print("Selected Population:")
       # for i, individual in enumerate(selected_population):
           # print(f"Individual {i + 1}: {individual}")

        new_population = crossover(selected_population, PATH_LENGTH, population)
        new_population = mutate(new_population, 0.1)  # Mutation rate of 10%

        population = new_population
        last_generation = population  # Save the population from the last generation

   # print("Last Generation:")
   # for i, individual in enumerate(last_generation):
   #     print(f"Individual {i + 1}: {individual}")

    # Check if any individual has reached the end (E)
    path_found = False
    for individual in last_generation:
        x, y = 1, 1  # Start position
        for move in individual:
            if move == "X":
                break
            dx, dy = DIRECTIONS[move]
            if can_move(x + dx, y + dy):
                x += dx
                y += dy
            if maze_layout[y][x] == "E":  # End reached
                path_found = True
                break
        if path_found:
            break

    if path_found:
        print("A path was found!")
    else:
        print("No path found.")

    # Only animate the last generation
    animate_population(surface, last_generation)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
