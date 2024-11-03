# Grid Pathfinding and Connectivity Project

This project implements a **Grid-based pathfinding and connectivity system** using C++ and OpenGL, designed for **CMPUT 350**. It supports **A* pathfinding** on a tile-based map with **octile topology** (8 compass directions) and includes efficient connectivity checks using flood fill and caching. This system could be used for simulations, games, or any application needing efficient movement and connectivity operations on a grid.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files Overview](#files-overview)


## Features

- **Grid Class**: Represents a rectangular map with octile topology, with support for `GROUND`, `WATER`, and `BLOCKED` tiles.
- **Pathfinding**: Uses the A* algorithm to find the shortest path, with cardinal and diagonal movement costs.
- **Connectivity Check**: Determines if two locations are connected on the grid, using flood fill and caching for efficiency.
- **Object Support**: Allows pathfinding and connectivity checks for moving objects of different sizes (1x1, 2x2, and 3x3 tiles).
- **OpenGL Testing Interface**: Visualizes pathfinding and connectivity operations, with interactive mouse controls for exploring the grid.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ZaidIslam1/PortfolioProjects.git
    cd PortfolioProjects/Pathfinding_350
    ```

2. **Compile**:
    ```bash
    make
    ```

3. **Run**:
    ```bash
    ./testGrid
    ```
4. **Remove**
    ```bash
    make clean
    ```
## Usage

- **Left-click**: Set start and end points for pathfinding.
- **Right-click**: Show connected component.
- **Middle-click**: Cycle through object sizes (1x1, 2x2, 3x3).
- **Keypress**: Exit program.

## Files Overview

- **Grid.h** / **Grid.cpp**: Core grid functionality, including pathfinding and connectivity.
- **GridPriv.h** / **GridInclude.h**: Helper files defining private data and methods for the Grid class.
- **TestGrid.cpp**: Testing setup for pathfinding and connectivity.
- **Makefile**: Compilation instructions.

## Assignment Context

This project is part of an assignment for CMPUT 350, focusing on implementing and testing a grid-based pathfinding and connectivity system, alongside exploring **PRA\*** map abstraction for hierarchical pathfinding.
