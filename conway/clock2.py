import os
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Configuration
WIDTH, HEIGHT = 1300, 800
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE  # Fixed number of columns
GRID_HEIGHT = HEIGHT // CELL_SIZE  # Fixed number of rows
FPS = 120
simulation_steps_per_frame = 1  # Number of simulation updates per rendered frame
CHARGEFILE = "pattern.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ----- Bigger, More Complex Digit Patterns for the Clock (7 rows x 5 cols for digits, 7x1 for colon) -----
DIGIT_PATTERNS_BIG = {
    '0': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    '1': [
        [0,0,1,0,0],
        [0,1,1,0,0],
        [1,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [1,1,1,1,1]
    ],
    '2': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,0,0,0,1],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,1,1,1,1]
    ],
    '3': [
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,0,1,1,0],
        [0,0,0,0,1],
        [0,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    '4': [
        [0,0,0,1,0],
        [0,0,1,1,0],
        [0,1,0,1,0],
        [1,0,0,1,0],
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,0,1,0]
    ],
    '5': [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    '6': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    '7': [
        [1,1,1,1,1],
        [0,0,0,0,1],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [0,1,0,0,0],
        [0,1,0,0,0]
    ],
    '8': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    '9': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,1],
        [0,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    ':': [
        [0],
        [0],
        [1],
        [0],
        [1],
        [0],
        [0]
    ]
}

# ----- Global Screen Setup -----
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life with Live Cell Clock")

# ----- Utility Functions -----
def get_pattern_file_path(filename="pattern.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

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
            if grid[y, x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[y, x] = 0
            elif grid[y, x] == 0 and neighbors == 3:
                new_grid[y, x] = 1
    return new_grid

def save_pattern(grid, filename="pattern.txt"):
    path = get_pattern_file_path(filename)
    with open(path, "w") as f:
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if grid[y, x] == 1:
                    f.write(f"{x} {y}\n")
    print(f"Pattern saved to {path}")

def load_pattern(grid, filename=CHARGEFILE, offset=(0,0)):
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
        print(f"Pattern loaded from {path} with offset {offset}")
    except Exception as e:
        print(f"Error loading pattern from {path}: {e}")
    return grid

# ----- Modified Clock Drawing Function with Wave Effect -----
def draw_clock_live(clock_time, top_left, cell_size, wave_timer, wave_duration):
    """
    Draws a larger clock (using DIGIT_PATTERNS_BIG) and, if a wave is active,
    inverts cell states from left to right as the wave front passes.
    """
    # Convert clock_time (seconds) to HH:MM:SS string.
    hours = clock_time // 3600
    minutes = (clock_time % 3600) // 60
    seconds = clock_time % 60
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    # Compute total columns used by the clock.
    total_cols = 0
    for char in time_str:
        pattern = DIGIT_PATTERNS_BIG.get(char)
        if pattern:
            total_cols += len(pattern[0]) + 1  # pattern width + gap
    total_cols -= 1  # remove gap after last character
    
    # Calculate clock dimensions.
    clock_display_width = total_cols * cell_size
    clock_display_height = 7 * cell_size  # 7 rows in our pattern

    # Determine wave progress.
    wave_progress = 0
    if wave_timer > 0:
        wave_progress = 1 - (wave_timer / wave_duration)
    wave_front = total_cols * wave_progress

    # Draw each character.
    x_offset_cells = 0  # in cell units relative to clock area top-left
    for char in time_str:
        pattern = DIGIT_PATTERNS_BIG.get(char)
        if not pattern:
            continue
        rows = len(pattern)
        cols = len(pattern[0])
        for r in range(rows):
            for c in range(cols):
                global_x = x_offset_cells + c
                cell_on = (pattern[r][c] == 1)
                if wave_timer > 0 and global_x < wave_front:
                    cell_on = not cell_on
                if cell_on:
                    cell_rect = pygame.Rect(
                        top_left[0] + (x_offset_cells + c) * cell_size,
                        top_left[1] + r * cell_size,
                        cell_size,
                        cell_size
                    )
                    pygame.draw.rect(screen, WHITE, cell_rect)
        x_offset_cells += cols + 1

# ----- Main Game Loop -----
def main():
    sim_clock = pygame.time.Clock()
    grid = create_grid()
    initial_grid = np.copy(grid)  # Store the initial state
    running = True
    paused = True

    offset_x, offset_y = 0, 0
    cell_size = CELL_SIZE

    clock_time = 0  # in seconds
    collision_flag = False  # tracks if a simulation cell was colliding with clock area

    # Wave effect variables.
    wave_timer = 0         # Current wave timer (in frames)
    wave_duration = 30     # Total duration of the wave effect (in frames)
    wave_pending = False   # Flag to indicate a pending clock update after the wave

    # Variables for dragging (panning) the view.
    dragging = False
    drag_start_pos = None
    initial_offset = (offset_x, offset_y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard controls.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if not paused:
                        initial_grid = np.copy(grid)
                if event.key == pygame.K_c:
                    grid = create_grid()
                if event.key == pygame.K_r:
                    grid = np.copy(initial_grid)
                if event.key == pygame.K_e:
                    save_pattern(grid)
                if event.key == pygame.K_i:
                    grid = load_pattern(grid, offset=(10, 0))

            # Mouse button down.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # middle button for panning.
                    dragging = True
                    drag_start_pos = event.pos
                    initial_offset = (offset_x, offset_y)
                if event.button == 4:  # scroll up to zoom in.
                    cell_size = min(40, cell_size + 1)
                if event.button == 5:  # scroll down to zoom out.
                    cell_size = max(5, cell_size - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    dragging = False

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    current_mouse_pos = event.pos
                    dx = current_mouse_pos[0] - drag_start_pos[0]
                    dy = current_mouse_pos[1] - drag_start_pos[1]
                    offset_x = initial_offset[0] + dx
                    offset_y = initial_offset[1] + dy

            # Left-click to set a cell alive.
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x = (pos[0] - offset_x) // cell_size
                y = (pos[1] - offset_y) // cell_size
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = 1

            # Right-click to kill a cell.
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x = (pos[0] - offset_x) // cell_size
                y = (pos[1] - offset_y) // cell_size
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = 0

        # Update the simulation.
        if not paused:
            for _ in range(simulation_steps_per_frame):
                grid = update_grid(grid)

        # Calculate clock area dimensions based on the BIG pattern.
        sample_time_str = f"{(clock_time // 3600):02}:{(clock_time % 3600)//60:02}:{(clock_time % 60):02}"
        total_cols = 0
        for char in sample_time_str:
            pattern = DIGIT_PATTERNS_BIG.get(char)
            if pattern:
                total_cols += len(pattern[0]) + 1
        total_cols -= 1  # remove last gap
        clock_display_width = total_cols * cell_size
        clock_display_height = 7 * cell_size  # pattern height

        # Place the clock at bottom-right with a margin.
        clock_top_left = (WIDTH - clock_display_width - 10, HEIGHT - clock_display_height - 10)
        clock_area_rect = pygame.Rect(clock_top_left[0], clock_top_left[1], clock_display_width, clock_display_height)

        # Delete any simulation cells that intrude into the clock area.
        collision = False
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if grid[y, x] == 1:
                    cell_rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y, cell_size, cell_size)
                    if cell_rect.colliderect(clock_area_rect):
                        grid[y, x] = 0
                        collision = True

        # When a new collision is detected, start the wave effect but do not update the clock yet.
        if collision and not collision_flag and not wave_pending:
            wave_timer = wave_duration  # start wave effect
            wave_pending = True
            collision_flag = True
        elif not collision:
            collision_flag = False

        # Update the wave timer.
        if wave_timer > 0:
            wave_timer -= 1
        # Once the wave effect completes, update the clock.
        elif wave_pending:
            clock_time += 1
            if clock_time >= 86400:
                clock_time = 0
            wave_pending = False

        # Draw grid and overlay the live-cell clock.
        draw_grid(grid, offset_x, offset_y, cell_size)
        draw_clock_live(clock_time, clock_top_left, cell_size, wave_timer, wave_duration)

        pygame.display.flip()
        sim_clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
