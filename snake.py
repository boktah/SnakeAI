import pygame
import math
from screeninfo import get_monitors

for m in get_monitors():
    print(str(m))

screen_width = 960
screen_height = int( screen_width * 10 / 16 )
grid_width = 32
grid_height = 20
block_size = screen_width / grid_width

def draw_grid():
    screen.fill(black)
    for x in range(grid_width):
        for y in range(grid_height):
            block = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, grey, block, 1)
    pygame.display.update()

black = (0, 0, 0)
grey = (40, 40, 40)
green = (50, 140, 30)

game_over = False

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
draw_grid()
pygame.display.update()

clock = pygame.time.Clock()

x = 16
x_offset = 0
y = 10
y_offset = 0

def translate_coords_to_pixels( x, y ):
    x_pos = x * block_size
    y_pos = y * block_size
    return (x_pos, y_pos)

def translate_pixels_to_coords( x_pos, y_pos ):
    x = math.floor( x_pos / block_size )
    y = math.floor( y_pos / block_size )
    return (x, y)

while not game_over:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_offset = -1
                y_offset = 0
            elif event.key == pygame.K_RIGHT:
                x_offset = 1
                y_offset = 0
            elif event.key == pygame.K_UP:
                x_offset = 0
                y_offset = -1
            elif event.key == pygame.K_DOWN:
                x_offset = 0
                y_offset = 1
    
    x += x_offset
    y += y_offset
    (x_pos, y_pos) = translate_coords_to_pixels( x, y )
    pygame.draw.rect(screen, green, (x_pos, y_pos, block_size, block_size))
    pygame.display.update()

    clock.tick(10)
        

pygame.display.quit()
