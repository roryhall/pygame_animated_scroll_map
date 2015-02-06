# helper classes for GAME

import pygame
from pygame import *


class Camera(object):
    def __init__(self, camera_func, width, height):
        
        self.camera_func = camera_func
        
        self.state = Rect(0, 0, width, height)# width and height of the current level map

    def apply(self, target): # This is where we re-calculate the position of an entity on the screen to apply the scrolling.
        return target.rect.move(self.state.topleft)

    def update(self, target): # Update each iteration passs in target
        self.state = self.camera_func(self.state, target.rect)

        


