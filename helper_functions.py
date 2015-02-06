# helper functions for game

import pygame
from pygame import *


def CreateImageList(filename, number_of_horizontal_cells):
    ''' This function takes a spritesheet and chops it up into 
        idividual images and returns a list of those images'''
    cell_list = []
    animation_sheet = pygame.image.load (filename)
    sheet_size = animation_sheet.get_size()
    cell_width = sheet_size[0] / number_of_horizontal_cells 
    cell_height = sheet_size[1]
    
    # start at 0, stop at sheet size height, increment - cell height
    # this loop chops up all the images and stores them in a list
    for y in range (0, sheet_size[1], cell_height):        
        for x in range (0, sheet_size[0], cell_width):
            surface = pygame.Surface((cell_width, cell_height))
            surface.blit(animation_sheet,(0,0),(x,y, cell_width, cell_height))
            colorkey = surface.get_at((0,0)) # get the bg color of the png
            surface.set_colorkey(colorkey)
            cell_list.append(surface) # list of all cell animations
    return cell_list



        


