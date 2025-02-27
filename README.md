## Index

- [Three-Body Problem Simulation](#three-body-problem-simulation)
- [Turing Machine Calculator](#turing-machine-calculator)
- [Conway Game Mod](#conway-game-mod)

## Three-Body Problem Simulation

This project is a Jupyter Notebook that simulates the three-body problem, a classical problem in physics that involves predicting the motion of three celestial bodies interacting with each other through gravitational forces. The notebook provides a visual representation of the trajectories of the bodies over time.

### Features:
- **Interactive Visualization**: The notebook includes interactive plots to visualize the motion of the three bodies.
- **Customizable Parameters**: Users can modify the initial conditions and parameters of the simulation to explore different scenarios.
- **Numerical Integration**: The simulation uses numerical methods to solve the differential equations governing the motion of the bodies.

### How to Use:
- **Running the Notebook**: Open the Jupyter Notebook and execute the cells to run the simulation.
- **Adjusting Parameters**: Modify the initial positions, velocities, and masses of the bodies in the notebook to see how they affect the motion.
- **Visualizing Results**: Use the interactive plots to observe the trajectories and analyze the behavior of the system.
## Turing Machine Calculator

This project implements a Turing Machine capable of performing basic arithmetic operations such as addition, subtraction, multiplication, division, square root, and exponentiation. The Turing Machine is a theoretical model of computation that manipulates symbols on a strip of tape according to a set of rules.

### Features:
- **Addition**: Computes the sum of two numbers.
- **Subtraction**: Computes the difference between two numbers.
- **Multiplication**: Computes the product of two numbers.
- **Division**: Computes the quotient and remainder of two numbers.
- **Square Root**: Computes the square root of a number.
- **Exponentiation**: Computes the result of raising a number to the power of another number.

### How to Use:
- **Input Format**: The input should be provided in a specific format on the tape, with each number and operation separated by a special symbol.
- **Running the Machine**: Start the Turing Machine by initializing the tape with the input and executing the transition rules.
- **Reading the Output**: The result of the computation will be written on the tape after the machine halts.



## Conway game mod 

Conway's Game of Life is a cellular automaton devised by mathematician John Conway. The game consists of a grid of cells that can live, die, or multiply based on a set of rules. The standard ruleset, known as B3/S23, dictates that:
- A live cell with 2 or 3 live neighbors survives (S23).
- A dead cell with exactly 3 live neighbors becomes a live cell (B3).
- All other live cells die in the next generation, and all other dead cells stay dead.

In this modified version, to create gliders with smaller structures, the ruleset changes to B2/S23:
- A live cell with 2 or 3 live neighbors survives (S23).
- A dead cell with exactly 2 live neighbors becomes a live cell (B2).
- All other live cells die in the next generation, and all other dead cells stay dead.


### How to Use:
- Export Pattern (E key): Press the E key to write the current live cell coordinates to "pattern.txt".
- Import Pattern (I key): Press the I key to read "pattern.txt" and overlay its pattern onto the grid.
- Basic Controls:
    - Mouse Left-Click: Add live cells.
    - Mouse Right-Click: Add dead cells.
    - Mouse Scroll: Zoom in/out.
    - SPACE: Pause or resume the simulation.
    - C: Clear the grid.
    - R: Reset the grid.
