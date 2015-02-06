#*******************************************#
#           HELPER SPRITE MODULE            #
#*******************************************#

import pygame



def load_image(filename): # function for loading images
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print 'Cannot load image:', filename
        raise SystemExit, message
    image = image.convert()
    return image

class StaticSpriteBlit(pygame.sprite.Sprite): #Use for grouping sprites
    
    def __init__(self, pos, filename, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(filename)
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0] 
        self.rect.y = pos[1]

    def update(self, screen):
        screen.blit (self.image, ([self.rect.x, self.rect.y]))



