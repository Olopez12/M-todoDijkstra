import heapq
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_random_grid(rows, cols, obstacle_prob=0.3):
    return [[1 if random.random() > obstacle_prob else 0 for _ in range(cols)] for _ in range(rows)]

def get_random_points(grid, num_points):
    points = []
    rows, cols = len(grid), len(grid[0])
    while len(points) < num_points:
        point = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if grid[point[0]][point[1]] == 1:
            points.append(point)
            grid[point[0]][point[1]] = 1  # Asegurar que los puntos de inicio/fin sean atravesables
    return points

def dijkstra_multiple_paths(grid, start_end_pairs):
    rows, cols = len(grid), len(grid[0])
    all_paths = []
    occupied = [[set() for _ in range(cols)] for _ in range(rows)]
    queues = []
    for start, end in start_end_pairs:
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[start[0]][start[1]] = 0
        queue = [(0, start, 0)]
        predecessors = {start: None}
        queues.append((queue, predecessors, end, distances))
    
    while any(queue for queue, _, _, _ in queues):
        next_queues = []
        for idx, (queue, predecessors, end, distances) in enumerate(queues):
            if not queue:
                next_queues.append((queue, predecessors, end, distances))
                continue

            current_distance, current_position, current_turn = heapq.heappop(queue)
            if current_position == end:
                path = []
                step = end
                while step is not None:
                    path.append(step)
                    step = predecessors.get(step)
                path.reverse()
                all_paths.append(path)
                continue

            current_row, current_col = current_position
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_row, neighbor_col = current_row + direction[0], current_col + direction[1]
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if grid[neighbor_row][neighbor_col] == 1:  # Check if the cell is traversable
                        new_distance = current_distance + 1
                        new_turn = current_turn + 1
                        if new_distance < distances[neighbor_row][neighbor_col]:
                            # Check if no collision in the same turn
                            if new_turn not in occupied[neighbor_row][neighbor_col]:
                                distances[neighbor_row][neighbor_col] = new_distance
                                heapq.heappush(queue, (new_distance, (neighbor_row, neighbor_col), new_turn))
                                predecessors[(neighbor_row, neighbor_col)] = current_position
                                occupied[neighbor_row][neighbor_col].add(new_turn)
            next_queues.append((queue, predecessors, end, distances))
        queues = next_queues
    return all_paths

def plot_grid(grid):
    plt.figure(figsize=(8, 8))
    rows, cols = len(grid), len(grid[0])
    plt.imshow(grid, cmap='Greys', origin='lower')
    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.grid(which='both', color='black', linestyle='-', linewidth=0.5)
    plt.show()

def plot_paths_on_grid(grid, paths):
    plt.figure(figsize=(8, 8))
    rows, cols = len(grid), len(grid[0])
    plt.imshow(grid, cmap='Greys', origin='lower')
    
    # Different colors for each path
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown', 'lime']

    for i, path in enumerate(paths):
        x, y = zip(*path)
        plt.plot(y, x, color=colors[i % len(colors)], marker='o', linestyle='-', linewidth=2, markersize=5, label=f'Agent {i+1}')

    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.grid(which='both', color='black', linestyle='-', linewidth=0.5)
    plt.legend()
    plt.show()

# Generate a 50x50 random grid
grid = generate_random_grid(50, 50, obstacle_prob=0.3)

# Plot the initial grid without paths
plot_grid(grid)

# Randomly generate start and end points
num_agents = 4  # Increased to 4 agents
start_points = get_random_points(grid, num_agents)
end_points = get_random_points(grid, num_agents)
start_end_pairs = list(zip(start_points, end_points))

# Find paths for multiple agents
paths = dijkstra_multiple_paths(grid, start_end_pairs)

# Plot the grid with the paths
plot_paths_on_grid(grid, paths)