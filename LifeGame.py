#-*- coding:utf8 -*-
#!/usr/bin/env python
import pygame, sys, time
import numpy as np
from pygame.locals import *

#Read map from data_directory
def world_init(data_dir):
    global world_array
    map_array = np.load(data_dir)
    global COLUMN,ROW
    COLUMN = map_array.shape[1]+2
    ROW = map_array.shape[0]+2

    world_array = np.zeros((ROW,COLUMN))
    world_array[1:ROW-1,1:COLUMN-1] = map_array

    pygame.world = np.zeros((ROW,COLUMN))

#Change RGB Color Here http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/
trail_col = (176,238,238)
dead_col = (255,255,255)
alive_col = (0,191,255)
background_col = (211,211,211)
block_size = 6

pygame.button_down = False

def bw_initialze():
    for sp_col in range(pygame.world.shape[1]):
        for sp_row in range(pygame.world.shape[0]):
            if pygame.world[sp_row][sp_col]:
                pygame.world[sp_row][sp_col] = 1

class Cell(pygame.sprite.Sprite):
    size = block_size+1

    def __init__(self, position,color):
        pygame.sprite.Sprite.__init__(self)
        self.grid = pygame.Surface([self.size-1,self.size-1])
        self.grid.fill((color))
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(background_col)
        self.image.blit(self.grid,(1,1))

        self.rect = self.image.get_rect()
        self.rect.topleft = position

def draw():
    screen.fill(background_col)
    for sp_col in range(pygame.world.shape[1]):
        for sp_row in range(pygame.world.shape[0]):
            if pygame.world[sp_row][sp_col]:
                if not trail_array[sp_row][sp_col]:
                    trail_array[sp_row][sp_col]=1
                new_cell = Cell((sp_col * Cell.size,sp_row * Cell.size),alive_col)
                screen.blit(new_cell.image,new_cell.rect)
            elif (trail_array[sp_row][sp_col]):
                new_cell = Cell((sp_col * Cell.size,sp_row * Cell.size),trail_col)
                screen.blit(new_cell.image,new_cell.rect)
            else:
                new_cell = Cell((sp_col * Cell.size,sp_row * Cell.size),dead_col)
                screen.blit(new_cell.image,new_cell.rect)

def next_generation():
    #trail_array = np.zeros((ROW,COLUMN))
    nbrs_count = sum(np.roll(np.roll(pygame.world, i, 0), j, 1)
                 for i in (-1, 0, 1) for j in (-1, 0, 1)
                 if (i != 0 or j != 0))
    pygame.world = (nbrs_count == 7)|(nbrs_count == 3) | ((pygame.world == 1) & (nbrs_count == 2 )).astype('int')
    #trail_array = (nbrs_count > 4).astype('int')

#initialize the map
def init():
    pygame.world=world_array
    bw_initialze()
    global trail_array
    trail_array = np.zeros((ROW,COLUMN))
    draw()
    return 'Stop'

def blank():
    pygame.world= np.zeros((ROW,COLUMN))
    #bw_initialze()
    global trail_array
    trail_array = np.zeros((ROW,COLUMN))
    draw()
    return 'Stop'

#stop actions
def stop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # keyboard actions
        if event.type == KEYDOWN and event.key == K_RETURN:
            return 'Move'
        
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'

        if event.type == KEYDOWN and event.key == K_RIGHT:
            return 'Next_step'

        if event.type == KEYDOWN and event.key == K_BACKSPACE:
            steps = 20
            step_move(steps)
            return 'Stop'
        if event.type == KEYDOWN and event.key == K_b:
            return 'Blank'

        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button
        
        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1: #left click
                pygame.world[sp_row][sp_col] = 1
                trail_array[sp_row][sp_col] = 1
            elif pygame.button_type == 3: #right click
                pygame.world[sp_row][sp_col] = 0
                trail_array[sp_row][sp_col] = 0

            draw()

    return 'Stop'

# Timer
pygame.clock_start = 0

# actions in move state
def move():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            return 'Stop'
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'
        if event.type == KEYDOWN and event.key == K_RIGHT:
            return 'Next_step'

        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button
        
        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1:
                pygame.world[sp_row][sp_col] = 1
                trail_array[sp_row][sp_col] = 1

            elif pygame.button_type == 3:
                pygame.world[sp_row][sp_col] = 0
                trail_array[sp_row][sp_col] = 0
            draw()

        
    if time.clock() - pygame.clock_start > 0.02:
        next_generation()
        draw()
        pygame.clock_start = time.clock()

    return 'Move'

def step_move(steps):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            return 'Stop'
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'
        if event.type == KEYDOWN and event.key == K_RIGHT:
            return 'Next_step'

        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button

        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1:
                pygame.world[sp_row][sp_col] = 1
                trail_array[sp_row][sp_col] = 1

            elif pygame.button_type == 3:
                pygame.world[sp_row][sp_col] = 0
                trail_array[sp_row][sp_col] = 0
            draw()

    while (steps > 0):
        next_generation()
        draw()
        steps = steps-1
    return 'Move'

def next_step():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'
        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button

        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1:
                pygame.world[sp_row][sp_col] = 1
                trail_array[sp_row][sp_col] = 1

            elif pygame.button_type == 3:
                pygame.world[sp_row][sp_col] = 0
                trail_array[sp_row][sp_col] = 0
            draw()

    if time.clock() - pygame.clock_start > 0.02:
        next_generation()
        draw()
        pygame.clock_start = time.clock()
        return 'Stop'

    return 'Stop'


if __name__ == '__main__':

    #State machine:
    state_actions = {
            'Reset': init,
            'Stop': stop,
            'Move': move,
            'Next_step': next_step,
            'Blank': blank
        }
    state = 'Reset'

    pygame.init()
    pygame.display.set_caption('Conway\'s Game of Life')
    world_init('map/binary_image.npy')

    screen = pygame.display.set_mode((COLUMN *Cell.size, ROW * Cell.size))

    while True: # Run the game

        state = state_actions[state]()
        pygame.display.update()
