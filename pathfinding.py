# A* search/pathfinding algorithm using pseudocode from Wikipedia
from collections import deque
from queue import PriorityQueue

def reconstruct_path(cameFrom, current):
    total_path = deque([current])
    while current in cameFrom:
        current = cameFrom[current]
        total_path.appendleft(current)
    total_path.popleft()
    return total_path

def heuristic(n, goal):
    x1, y1 = n
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(start, goal, neighbors_func):
    
    # openSet is the set of discovered nodes that may be expanded upon as a min-heap
    openSet = PriorityQueue()
    openSet.put(start, 0)

    # cameFrom[n] maps to the node preceding n on the cheapest path from start
    cameFrom = {}
    # g = cost of path from start to n
    gScore = { start: 0 }
    # f = g + h(n) given heuristic function n estimating cost of path from n to goal
    fScore = { start: heuristic(start, goal) }

    while openSet:
        # current = node in openSet with lowest f score
        current = openSet.get()
        # (priority, current) = lowest
        if current == goal:
            return reconstruct_path(cameFrom, current)

        for neighbor in neighbors_func(current):
            tentative_gScore = gScore[current] + 1
            if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)

                # if neighbor not in openSet:
                openSet.put(neighbor, fScore[neighbor])
                # print(neighbor)
    
    return None
