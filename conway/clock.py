import os
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Configuration
WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 1
CHARGEFILE = "pattern.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Utility: get the absolute path for the pattern file in the same directory as the script.
def get_pattern_file_path(filename="pattern.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

# Initialize grid
def create_grid():
    return np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

def draw_grid(grid, offset_x, offset_y, cell_size):
    screen.fill(BLACK)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 1:
                pygame.draw.rect(
                    screen, WHITE,
                    ((x * cell_size) + offset_x, (y * cell_size) + offset_y, cell_size, cell_size)
                )

def update_grid(grid):
    new_grid = np.copy(grid)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            # Count live neighbors
            neighbors = (
                grid[(y - 1) % grid.shape[0], (x - 1) % grid.shape[1]]
                + grid[(y - 1) % grid.shape[0], x % grid.shape[1]]
                + grid[(y - 1) % grid.shape[0], (x + 1) % grid.shape[1]]
                + grid[y % grid.shape[0], (x - 1) % grid.shape[1]]
                + grid[y % grid.shape[0], (x + 1) % grid.shape[1]]
                + grid[(y + 1) % grid.shape[0], (x - 1) % grid.shape[1]]
                + grid[(y + 1) % grid.shape[0], x % grid.shape[1]]
                + grid[(y + 1) % grid.shape[0], (x + 1) % grid.shape[1]]
            )

            # Apply b4/s1 rules:
            # Live cell survives only with exactly 1 neighbor.
            if grid[y, x] == 1:
                if neighbors != 1:
                    new_grid[y, x] = 0
            # Dead cell is born only if it has exactly 4 neighbors.
            else:
                if neighbors == 4:
                    new_grid[y, x] = 1

    return new_grid


def save_pattern(grid, filename="pattern.txt"):
    """Export live cell coordinates to a text file in the same directory as the script."""
    path = get_pattern_file_path(filename)
    with open(path, "w") as f:
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if grid[y, x] == 1:
                    f.write(f"{x} {y}\n")
    print(f"Pattern saved to {path}")

def load_pattern(grid, filename=CHARGEFILE, offset=(0,0)):
    """Import a pattern from a text file in the same directory and overlay it onto the grid."""
    path = get_pattern_file_path(filename)
    offset_x, offset_y = offset
    try:
        with open(path, "r") as f:
            for line in f:
                x, y = map(int, line.strip().split())
                new_x = x + offset_x
                new_y = y + offset_y
                if 0 <= new_x < grid.shape[1] and 0 <= new_y < grid.shape[0]:
                    grid[new_y, new_x] = 1
        print(f"Pattern loaded from {path}")
    except Exception as e:
        print(f"Error loading pattern from {path}: {e}")
    return grid

def load_pattern_rle(grid, filename="pattern.rle", offset=(0, 0)):
    """Import a pattern from an RLE file and overlay it onto the grid.
    
    The RLE file should follow the common Game of Life format:
      - Lines starting with '#' are comments.
      - The first non-comment line is the header (e.g., x = 3, y = 3, rule = B3/S23).
      - The subsequent lines encode the pattern using RLE:
          - A number preceding a symbol indicates a repetition.
          - 'b' indicates dead cells (skipped).
          - 'o' indicates live cells.
          - '$' indicates the end of a row (move to the next row).
          - '!' marks the end of the pattern.
    
    The pattern is overlaid on the grid using the given offset.
    """
    path = get_pattern_file_path(filename)
    offset_x, offset_y = offset
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        # Remove comments and blank lines
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        if not lines:
            print("No pattern data found in the RLE file.")
            return grid

        # The first non-comment line is the header; we skip it.
        header = lines[0]
        # Combine the remaining lines (they might be split over multiple lines)
        pattern_data = "".join(lines[1:])

        x = 0
        y = 0
        number = ""
        i = 0
        while i < len(pattern_data):
            char = pattern_data[i]
            if char.isdigit():
                number += char
            elif char == 'b':  # dead cells: simply advance x without setting any cell.
                count = int(number) if number else 1
                x += count
                number = ""
            elif char == 'o':  # live cells: set the appropriate cells to alive.
                count = int(number) if number else 1
                for _ in range(count):
                    new_x = x + offset_x
                    new_y = y + offset_y
                    if 0 <= new_y < grid.shape[0] and 0 <= new_x < grid.shape[1]:
                        grid[new_y, new_x] = 1
                    x += 1
                number = ""
            elif char == '$':  # end-of-line: move to the next row
                count = int(number) if number else 1
                y += count
                x = 0
                number = ""
            elif char == '!':  # end-of-pattern marker
                break
            i += 1

        print(f"RLE pattern loaded from {path}")
    except Exception as e:
        print(f"Error loading RLE pattern from {path}: {e}")
    return grid

def load_pattern_rle(grid, filename="pattern.rle", offset=(0, 0)):
    """Import a pattern from an RLE file and overlay it onto the grid.
    
    The RLE file should follow the common Game of Life format:
      - Lines starting with '#' are comments.
      - The first non-comment line is the header (e.g., x = 3, y = 3, rule = B3/S23).
      - The subsequent lines encode the pattern using RLE:
          - A number preceding a symbol indicates a repetition.
          - 'b' indicates dead cells (skipped).
          - 'o' indicates live cells.
          - '$' indicates the end of a row (move to the next row).
          - '!' marks the end of the pattern.
    
    The pattern is overlaid on the grid using the given offset.
    """
    path = get_pattern_file_path(filename)
    offset_x, offset_y = offset
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        # Remove comments and blank lines
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        if not lines:
            print("No pattern data found in the RLE file.")
            return grid

        # The first non-comment line is the header; we skip it.
        header = lines[0]
        # Combine the remaining lines (they might be split over multiple lines)
        pattern_data = "".join(lines[1:])

        x = 0
        y = 0
        number = ""
        i = 0
        while i < len(pattern_data):
            char = pattern_data[i]
            if char.isdigit():
                number += char
            elif char == 'b':  # dead cells: simply advance x without setting any cell.
                count = int(number) if number else 1
                x += count
                number = ""
            elif char == 'o':  # live cells: set the appropriate cells to alive.
                count = int(number) if number else 1
                for _ in range(count):
                    new_x = x + offset_x
                    new_y = y + offset_y
                    if 0 <= new_y < grid.shape[0] and 0 <= new_x < grid.shape[1]:
                        grid[new_y, new_x] = 1
                    x += 1
                number = ""
            elif char == '$':  # end-of-line: move to the next row
                count = int(number) if number else 1
                y += count
                x = 0
                number = ""
            elif char == '!':  # end-of-pattern marker
                break
            i += 1

        print(f"RLE pattern loaded from {path}")
    except Exception as e:
        print(f"Error loading RLE pattern from {path}: {e}")
    return grid

def main():
    clock = pygame.time.Clock()
    grid = create_grid()
    initial_grid = np.copy(grid)  # Store the initial state
    running = True
    paused = True

    offset_x, offset_y = 0, 0
    cell_size = CELL_SIZE

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if not paused:
                        initial_grid = np.copy(grid)  # Save current state as initial when starting
                if event.key == pygame.K_c:
                    grid = create_grid()
                if event.key == pygame.K_r:  # Reset to initial state
                    grid = np.copy(initial_grid)
                if event.key == pygame.K_e:  # Export pattern
                    save_pattern(grid)
                if event.key == pygame.K_i:  # Import pattern
                    grid = load_pattern(grid, offset=(0, 0))
                if event.key == pygame.K_i:  # Import pattern
                    # You can change the filename below to the file you wish to load.
                    if CHARGEFILE == "osilator.rle":  # or "pattern.txt"
                        grid = load_pattern_rle(grid, CHARGEFILE, offset=(0, 0))
                    else:
                        grid = load_pattern(grid, CHARGEFILE, offset=(0, 0))

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x = (pos[0] - offset_x) // cell_size
                y = (pos[1] - offset_y) // cell_size
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = 1

            if pygame.mouse.get_pressed()[2]:  # Right-click to kill live cells
                pos = pygame.mouse.get_pos()
                x = (pos[0] - offset_x) // cell_size
                y = (pos[1] - offset_y) // cell_size
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up to zoom in
                    cell_size = min(40, cell_size + 1)
                if event.button == 5:  # Scroll down to zoom out
                    cell_size = max(5, cell_size - 1)

        if not paused:
            grid = update_grid(grid)

        draw_grid(grid, offset_x, offset_y, cell_size)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
