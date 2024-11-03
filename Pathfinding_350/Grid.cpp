#include "Grid.h"
#include <cassert>
#include <cmath>
#include <queue>
#include <set>

Grid::Grid(int width, int height)
    : width(width), height(height), map(height, std::vector<Tile>(width)) {
	assert(width > 0 && height > 0);
}

Grid::~Grid() {}

int Grid::getWidth() const { return width; }
int Grid::getHeight() const { return height; }

Grid::Tile Grid::getTile(int x, int y) const {
	assert(x >= 0 && x < width);
	assert(y >= 0 && y < height);
	return map[y][x];
}

void Grid::setTile(int x, int y, Tile tile) {
	assert(x >= 0 && x < width);
	assert(y >= 0 && y < height);
	map[y][x] = tile;
}

bool Grid::isWithinBounds(int x, int y, int size) const {
	return (x >= 0 && y >= 0 && x + size < getWidth() &&
	        y + size < getHeight());
}

bool Grid::canMoveTo(int x, int y, int size, Tile tileType) const {
	if (!isWithinBounds(x, y, size))
		return false;
	for (int direct_x = 0; direct_x <= size; ++direct_x) {
		for (int direct_y = 0; direct_y <= size; ++direct_y) {
			// Check if each tile within object's area matches target tile type
			if (getTile(x + direct_x, y + direct_y) != tileType)
				return false;
		}
	}
	return true;
}

int Grid::heuristic(int x1, int y1, int x2, int y2) const {
	int direct_x = x1 - x2;
	int direct_y = y1 - y2;
	// Euclidean distance multiplied by cardinal cost for A* heuristic
	return static_cast<int>(
	    std::sqrt(direct_x * direct_x + direct_y * direct_y) * CARDINAL_COST);
}

bool Grid::isConnected(int size, int x1, int y1, int x2, int y2) const {
	std::tuple<int, int, int, int, int> key = {size, x1, y1, x2, y2};

	// Check if the result is already cached
	if (cache.find(key) != cache.end()) {
		return cache[key];
	}

	// Validate if start and end points are within bounds and match tile type
	if (!isWithinBounds(x1, y1, size) || !isWithinBounds(x2, y2, size)) {
		if (getTile(x1, y1) != getTile(x2, y2)) {
			cache[key] = false;
			return false;
		}
	}

	std::queue<std::pair<int, int>> frontier; // Queue for flood fill
	std::set<std::pair<int, int>> visited;    // Track visited nodes
	frontier.push({x1, y1});
	visited.insert({x1, y1});

	int direct_x[4] = {0, 1, 0, -1}; // N, E, S, W
	int direct_y[4] = {-1, 0, 1, 0};

	while (!frontier.empty()) {
		std::pair<int, int> current = frontier.front();
		int current_x = current.first;
		int current_y = current.second;
		frontier.pop();

		// If we reached the target, cache and return true
		if (current_x == x2 && current_y == y2) {
			cache[key] = true;
			return true;
		}

		// Explore neighboring nodes in four cardinal directions
		for (int i = 0; i < 4; ++i) {
			int nextNode_x = current_x + direct_x[i];
			int nextNode_y = current_y + direct_y[i];
			std::pair<int, int> neighbor = {nextNode_x, nextNode_y};

			// If move is valid and neighbor not yet visited, add to queue
			if (canMoveTo(nextNode_x, nextNode_y, size, getTile(x1, y1)) &&
			    visited.insert(neighbor).second) {
				frontier.push(neighbor);
			}
		}
	}

	// Cache result if no connection is found
	cache[key] = false;
	return false;
}

int Grid::findShortestPath(int size, int x1, int y1, int x2, int y2,
                           std::vector<Direction> &path) const {
	// Return -1 if start or end point is invalid
	if (!isWithinBounds(x1, y1, size) || !isWithinBounds(x2, y2, size) ||
	    getTile(x1, y1) != getTile(x2, y2)) {
		return -1;
	}

	using Node = std::tuple<int, int, int>; // (f-cost, x, y)
	std::priority_queue<Node, std::vector<Node>, CompareNode> pq;
	std::map<std::tuple<int, int>, int> g_costs;      // Cost map
	std::map<std::tuple<int, int>, Direction> parent; // Store path

	int direct_x[8] = {0, 1, 1, 1, 0, -1, -1, -1}; // Directions for movement
	int direct_y[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
	const Direction directions[8] = {N, NE, E, SE, S, SW, W, NW};

	g_costs[{x1, y1}] = 0; // Initialize g-cost for start node
	pq.push({heuristic(x1, y1, x2, y2), x1, y1});

	while (!pq.empty()) {
		Node current = pq.top();
		int current_x = std::get<1>(current);
		int current_y = std::get<2>(current);
		pq.pop();

		// Path found, reconstruct the path
		if (current_x == x2 && current_y == y2) {
			int px = x2, py = y2;
			while (px != x1 || py != y1) {
				Direction dir = parent[{px, py}];
				path.push_back(dir);
				px -= direct_x[dir];
				py -= direct_y[dir];
			}
			std::reverse(path.begin(), path.end());
			return g_costs[{x2, y2}];
		}

		for (int i = 0; i < 8; ++i) { // Check in all 8 compass directions
			int nextNode_x = current_x + direct_x[i];
			int nextNode_y = current_y + direct_y[i];
			int cost = (i % 2 == 0) ? CARDINAL_COST : DIAGONAL_COST;

			if (i % 2 != 0) { // Diagonal move
				int adj_x1 = current_x + direct_x[i];
				int adj_y1 = current_y;

				int adj_x2 = current_x;
				int adj_y2 = current_y + direct_y[i];

				// Ensure both adjacent tiles along the diagonal are free
				if (!canMoveTo(adj_x1, adj_y1, size, getTile(x1, y1)) ||
				    !canMoveTo(adj_x2, adj_y2, size, getTile(x1, y1))) {
					continue; // Skip this diagonal move if either adjacent tile
					          // is blocked
				}
			}

			// If movement to next node is valid
			if (canMoveTo(nextNode_x, nextNode_y, size, getTile(x1, y1))) {
				std::tuple<int, int> current_pos(current_x, current_y);
				std::tuple<int, int> next_pos(nextNode_x, nextNode_y);
				int new_g_cost = g_costs[current_pos] + cost;

				// Update g-cost if a better path is found
				if (g_costs.find(next_pos) == g_costs.end() ||
				    new_g_cost < g_costs[next_pos]) {
					g_costs[next_pos] = new_g_cost;
					int f_cost =
					    heuristic(nextNode_x, nextNode_y, x2, y2) + new_g_cost;
					pq.push({f_cost, nextNode_x, nextNode_y});
					parent[next_pos] = directions[i]; // Track direction for
				}
			}
		}
	}
	return -1; // Return -1 if no path is found
}
