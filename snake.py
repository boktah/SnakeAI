import pygame
import math
import random

screen_width = 960
screen_height = int( screen_width * 3 / 4 )
grid_width = 4 * 8
grid_height = 3 * 8
block_size = screen_width / grid_width

def draw_grid():
    screen.fill(black)
    for x in range(grid_width):
        for y in range(grid_height):
            block = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, grey, block, 1)
    pygame.display.update()

def draw_snake(snake_list):
    for pos in snake_list:
        (x, y) = pos
        pygame.draw.rect(screen, green, )

black = (0, 0, 0)
grey = (40, 40, 40)
green = (50, 140, 30)
red = (140, 50, 30)

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

def translate_coords_to_pixels( x, y ):
    x_pos = x * block_size
    y_pos = y * block_size
    return (x_pos, y_pos)

fruit_x = round( random.randrange(0, grid_width) )
fruit_y = round( random.randrange(0, grid_height) )

while not game_over:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_offset = -1
                y_offset = 0
                x_pos_offset = 1
                x_size_offset = 0
                y_pos_offset = 1
                y_size_offset = -2
            elif event.key == pygame.K_RIGHT:
                x_offset = 1
                y_offset = 0
                x_pos_offset = -1
                x_size_offset = 0
                y_pos_offset = 1
                y_size_offset = -2
            elif event.key == pygame.K_UP:
                x_offset = 0
                y_offset = -1
                x_pos_offset = 1
                x_size_offset = -2
                y_pos_offset = 1
                y_size_offset = 1
            elif event.key == pygame.K_DOWN:
                x_offset = 0
                y_offset = 1
                x_pos_offset = 1
                x_size_offset = -2
                y_pos_offset = -1
                y_size_offset = 0
    
    old_x = x
    old_y = y
    x += x_offset
    y += y_offset

    snake_list.append((x,y))

    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        game_over = True

    # draw_grid()

    # draw fruit
    (fruit_x_pos, fruit_y_pos) = translate_coords_to_pixels( fruit_x, fruit_y )
    pygame.draw.rect(screen, red, (fruit_x_pos, fruit_y_pos, block_size, block_size))

    # draw snake segment
    draw_snake()
    (x_pos, y_pos) = translate_coords_to_pixels( x, y )
    segment = pygame.Rect(x_pos + x_pos_offset, y_pos + y_pos_offset, block_size + x_size_offset, block_size + y_size_offset)
    pygame.draw.rect(screen, green, segment)

    pygame.display.update()
    
    if x == fruit_x and y == fruit_y:
        fruit_x = round( random.randrange(0, grid_width) )
        fruit_y = round( random.randrange(0, grid_height) )
        snake_len += 1
    else:
        # erase last snake block
        block = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
        pygame.draw.rect(screen, black, block, 0)
        pygame.draw.rect(screen, grey, block, 1)

    print(snake_len)

    clock.tick(10)
        

pygame.display.quit()
