#pragma once
#include "GridInclude.h"

// Functor for A* priority queue comparison
struct CompareNode {
	using Node = std::tuple<int, int, int>; // (f-cost, x, y)
	bool operator()(const Node &a, const Node &b) const {
		return std::get<0>(a) > std::get<0>(b); // Min-heap based on f-cost
	}
};

// Private helper functions for A* pathfinding
int heuristic(int x1, int y1, int x2, int y2) const;
bool isWithinBounds(int x, int y, int size) const;
bool canMoveTo(int x, int y, int size, Grid::Tile tileType) const;

// Declare private members for Grid class
int width, height;
mutable std::vector<std::vector<Grid::Tile>> map;
mutable std::map<std::tuple<int, int, int, int, int>, bool>
    cache; // mutable because isConnected is const
