import pygame
import math
import random
from time import sleep
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

def a_star(start, goal):
    
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

        for neighbor in neighbors(current):
            tentative_gScore = gScore[current] + 1
            if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)

                # if neighbor not in openSet:
                openSet.put(neighbor, fScore[neighbor])
                # print(neighbor)
    
    return None




screen_width = 960
screen_height = int( screen_width * 3 / 4 )
grid_width = 4 * 8      # 32
grid_height = 3 * 8     # 24
block_size = screen_width / grid_width

def draw_grid():
    screen.fill(black)
    for x in range(grid_width):
        for y in range(grid_height):
            block = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, grey, block, 1)
    # pygame.display.update()

def draw_snake(snake_list):
    draw_grid()
    for i in range(len(snake_list)):
        (x, y) = snake_list[i]
        (x_pos, y_pos) = translate_coords_to_pixels( x, y )
        segment = pygame.Rect(x_pos + 1, y_pos + 1, block_size - 2, block_size - 2)
        pygame.draw.rect(screen, green, segment)

        if (i + 1) < len(snake_list):
            (next_x, next_y) = snake_list[i + 1]
            (next_x_pos, next_y_pos) = translate_coords_to_pixels( next_x, next_y )
            bridge_x = 0
            bridge_x_size = 0
            bridge_y = 0
            bridge_y_size = 0
            if next_x == x and next_y < y: # up
                bridge_x = next_x_pos + 1
                bridge_x_size = block_size - 2
                bridge_y = next_y_pos + block_size - 1
                bridge_y_size = 2
            elif next_x == x and next_y > y: # down
                bridge_x = next_x_pos + 1
                bridge_x_size = block_size - 2
                bridge_y = y_pos + block_size - 1
                bridge_y_size = 2
            elif next_x > x and next_y == y: # right
                bridge_x = x_pos + block_size - 1
                bridge_x_size = 2
                bridge_y = next_y_pos + 1
                bridge_y_size = block_size - 2
            elif next_x < x and next_y == y: # left
                bridge_x = next_x_pos + block_size - 1
                bridge_x_size = 2
                bridge_y = next_y_pos + 1
                bridge_y_size = block_size - 2
            bridge = pygame.Rect(bridge_x, bridge_y, bridge_x_size, bridge_y_size)
            pygame.draw.rect(screen, green, bridge)

def fruit_in_snake(fruit_x, fruit_y):
    for pos in snake_list:
        (x, y) = pos
        if fruit_x == x and fruit_y == y:
            return True
    return False

def calculate_direction(current, moveList: deque):
    nextPos = moveList.popleft()
    direction = -1

    if current == next:
        return None
    
    (x1, y1) = current
    (x2, y2) = nextPos
    if x2 > x1: # right
        direction = 0
    elif y2 > y1: # down
        direction = 1
    elif x2 < x1: # left
        direction = 2
    elif y2 < y1: # up
        direction = 3
    
    print(current, nextPos, direction)
    return direction

def neighbors(n):
    (x, y) = n
    adjNodes = []
    if x + 1 >= 0 and x + 1 < grid_width and not fruit_in_snake(x+1, y):
        adjNodes.append((x+1, y))
    if x - 1 >= 0 and x - 1 < grid_width and not fruit_in_snake(x-1, y):
        adjNodes.append((x-1, y))
    if y + 1 >= 0 and y + 1 < grid_height and not fruit_in_snake(x, y+1):
        adjNodes.append((x, y+1))
    if y - 1 >= 0 and y - 1 < grid_height and not fruit_in_snake(x, y-1):
        adjNodes.append((x, y-1))
    return adjNodes

black = (0, 0, 0)
grey = (40, 40, 40)
green = (50, 140, 30)
red = (220, 20, 20)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
draw_grid()
pygame.display.update()

clock = pygame.time.Clock()

x = math.floor( grid_width / 2 )
x_offset = 1
x_pos_offset = 1
x_size_offset = -2

y = math.floor( grid_height / 2 )
y_offset = 0
y_pos_offset = 1
y_size_offset = -2

game_over = False
snake_list = [(x,y)]
snake_len = 1
direction = 0 # right

def translate_coords_to_pixels( x, y ):
    x_pos = x * block_size
    y_pos = y * block_size
    return (x_pos, y_pos)

fruit_x = round( random.randrange(0, grid_width) )
fruit_y = round( random.randrange(0, grid_height) )

# moveList = a_star( (x,y), (fruit_x, fruit_y) )
# print(moveList)

while not game_over:
    moveList = a_star( (x,y), (fruit_x, fruit_y) )
    direction = calculate_direction( (x,y), moveList )

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            game_over = True
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         direction = 0 if direction != 2 else direction
        #     elif event.key == pygame.K_DOWN:
        #         direction = 1 if direction != 3 else direction
        #     elif event.key == pygame.K_LEFT:
        #         direction = 2 if direction != 0 else direction
        #     elif event.key == pygame.K_UP:
        #         direction = 3 if direction != 1 else direction

    if direction == 0:
        x_offset = 1
        y_offset = 0
    elif direction == 1:
        x_offset = 0
        y_offset = 1
    elif direction == 2:
        x_offset = -1
        y_offset = 0
    elif direction == 3:
        x_offset = 0
        y_offset = -1
            

    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        game_over = True

    x += x_offset
    y += y_offset
    snake_list.append((x,y))

    if (len(snake_list) > snake_len):
        del snake_list[0]
    
    for pos in snake_list[:-1]:
        if (pos == (x,y)):
            game_over = True
    
    draw_snake(snake_list)

    # draw fruit
    (fruit_x_pos, fruit_y_pos) = translate_coords_to_pixels( fruit_x, fruit_y )
    pygame.draw.rect(screen, red, (fruit_x_pos, fruit_y_pos, block_size, block_size))

    pygame.display.update()
    
    if x == fruit_x and y == fruit_y:
        fruit_x = round( random.randrange(0, grid_width) )
        fruit_y = round( random.randrange(0, grid_height) )
        while fruit_in_snake(fruit_x, fruit_y):
            fruit_x = round( random.randrange(0, grid_width) )
            fruit_y = round( random.randrange(0, grid_height) )
        snake_len += 1
        print("length: ", snake_len)
        moveList = a_star( (x,y), (fruit_x, fruit_y) )

    # sleep(1000)
    clock.tick(60)


pygame.display.quit()
