Grid Pathfinding and Connectivity Project
This project implements a Grid-based pathfinding and connectivity system using C++ and OpenGL, designed for CMPUT 350. It supports A pathfinding* on a tile-based map with octile topology (8 compass directions) and includes efficient connectivity checks using flood fill and caching.

Table of Contents
Features
Installation
Usage
Files Overview
Assignment Context
Features
Grid Class: Represents a rectangular map with octile topology, supporting GROUND, WATER, and BLOCKED tiles.
Pathfinding: Uses the A* algorithm to find the shortest path with both cardinal and diagonal movement.
Connectivity Check: Determines if two locations are connected on the grid, using flood fill and caching for efficiency.
Object Support: Enables pathfinding and connectivity checks for moving objects of various sizes (1x1, 2x2, and 3x3 tiles).
OpenGL Testing Interface: Provides a visual interface to interactively explore the grid, pathfinding, and connectivity using mouse controls.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/ZaidIslam1/PortfolioProjects.git
cd PortfolioProjects/Pathfinding_350
Compile the Program:

bash
Copy code
make
Run the Program:

bash
Copy code
./testGrid
Usage
Mouse Controls:

Left-click: Set start and end points for pathfinding.
Right-click: Highlight connected areas for the selected tile type.
Middle-click: Cycle through object sizes (1x1, 2x2, 3x3).
Keyboard Controls:

Press any key to exit the program.
Files Overview
Grid.cpp / Grid.h: Core grid functionality, including pathfinding and connectivity methods.
GridPriv.h / GridInclude.h: Helper files defining private data and methods for the Grid class.
TestGrid.cpp: A testing setup to validate pathfinding and connectivity operations with OpenGL visualization.
README.txt: Additional project details and instructions.
Makefile: Instructions for compiling the project.
Assignment Context
This project was developed as part of the CMPUT 350 course, focusing on creating a grid-based pathfinding and connectivity system with practical applications in simulations, games, and hierarchical pathfinding. The implementation also explores PRA* abstraction methods to improve pathfinding efficiency on larger maps.
