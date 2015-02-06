

import pygame, sys, helper_classes, helper_functions, levels
from pygame import *
from helper_classes import*
from helper_functions import*
from levels import* # create maps and levels

# need a text sprite class
# when creating these objects get the start x value for the display image
class TextStats(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)       
        self.font = pygame.font.SysFont("None", 24)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.update(0)

        
    def update(self, inputValue):
        self.text = "%d" % (inputValue)                    
        self.image  = self.font.render(self.text, 1, (gold))
        self.rect = [self.pos_x, self.pos_y] 
        
def update_lifeforce(statsBar, lifeforceValue):
    start_x = (statsBar.rect.x + 113)
    if lifeforceValue > start_x:        
        
        pygame.draw.line(screen, green, [start_x, 582], [lifeforceValue, 582], 6)
      

       
#----------------------------------------------------------------------------------------------------------------
def complex_camera(camera, target_rect):
    
    left, top, _, _ = target_rect
    _, _, w, h = camera    
    left, top, _, _ = -left + 300, -top + HALF_HEIGHT, w, h
    left = max(-(camera.width - DISPLAY_WIDTH), left)   # stop scrolling at the right edge
    left = min(0, left)                                 # stop scrolling at the left edge     
    top = max(-(camera.height - DISPLAY_HEIGHT), top)   # stop scrolling at the bottom
    top = min(0, top)                                   # stop scrolling at the top    
    return Rect(left, top, w, h)

#-----------------------------------------------------------------------------------------------------------------
class HitBlock (pygame.sprite.Sprite): ### INVISIBLE DO NOT BLIT

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)    
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill (white)
        self.rect = self.image.get_rect()
        self.rect.y = pos[1]
        self.rect.x = pos[0]
        
class StaticSpriteBlit(pygame.sprite.Sprite): 
    
    def __init__(self, pos, filename, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0] 
        self.rect.y = pos[1]

    def update(self, screen):
        screen.blit (self.image, ([self.rect.x, self.rect.y]))

        
class StaticImageSprite (pygame.sprite.Sprite):
    def __init__(self, x,y, filename, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image_size = self.image.get_size()
        self.image.set_colorkey(alpha)
        self.rect = Rect(x, y, self.image_size[0], self.image_size[1])

    def update(self):
        pass 


##--------------------------------------------- Player Sprite ------------------------------

#girl_list = CreateImageList("player_images/girl1.png", 2)

class AnimatedSpriteSheet(pygame.sprite.Sprite):
    def __init__(self, imageList, pos):        
        pygame.sprite.Sprite.__init__(self)        
        self.spriteSheet = imageList                        # pass a list of image frames
        self.image = self.spriteSheet[0] 
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] 
        self.rect.y = pos[1]
        self.cell_position = 0

    def updateFrame(self, imagePos):                        # Pass in the frame number to go to
        self.image= self.spriteSheet[imagePos]
        
    def animate(self):                                      # Runs the animation sequence
        timer = 0
        if self.cell_position < len(self.spriteSheet)-1:
            self.cell_position +=1            
        else:                                               # Runs when cell_position > frame length
            self.cell_position = len(self.spriteSheet)-1    # Stop the animation at last frame
        timer +=1
        print timer

        self.image = (self.spriteSheet[self.cell_position]) # Blit image at cell_position
##        if timer <=10:
##            self.cell_position = 0


   

cell_list_r = CreateImageList("player_images/boy_walking_Right.png", 6)
cell_list_l = CreateImageList("player_images/boy_walking_Left.png", 6)
cell_list_u = CreateImageList("player_images/boy_walking_Up.png", 6)
cell_list_d = CreateImageList("player_images/boy_walking_Down.png", 6)
start_x = 100
start_y = 100

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):        
        pygame.sprite.Sprite.__init__(self)       
        self.cell_position = 0

        # initial start position of player
        self.image = cell_list_r[0] # face the player to the right
        self.rect = self.image.get_rect()
        self.rect.x = start_x # start position x
        self.rect.y = start_y # start position y
        
        self.wealth = 0
        self.level = 0
        self.lifeForce = 0
        
                
    def update(self, up, down, left, right, wall_list):
    
        if left :
            self.images = cell_list_l[2:]
            self.rect.x -=3
            for wall in wall_list:   # if players hits a wall
                if pygame.sprite.collide_rect(self, wall):
                    self.images = cell_list_l[0:1]
                    self.rect.left = wall.rect.right
            self.blit(self.images, self.rect)
            
        if right :
            self.images = cell_list_r[2:]
            self.rect.x +=3
            for wall in wall_list:   # if players hits a wall
                if pygame.sprite.collide_rect(self, wall):
                    self.images = cell_list_r[0:1]
                    self.rect.right = wall.rect.left
            self.blit(self.images, self.rect)
            
        if up :
            self.images = cell_list_u[2:]
            self.rect.y -=3
            for wall in wall_list:   # if players hits a wall
                if pygame.sprite.collide_rect(self, wall):
                    self.images = cell_list_u[0:1]
                    self.rect.top = wall.rect.bottom
            self.blit(self.images, self.rect)
            
        if down :
            self.images = cell_list_d[2:]
            self.rect.y +=3
            for wall in wall_list:   # if players hits a wall
                if pygame.sprite.collide_rect(self, wall):
                    self.images = cell_list_d[0:1]
                    self.rect.bottom = wall.rect.top
            self.blit(self.images, self.rect)        

        
    def blit(self,imageList, rect):            
        
        if self.cell_position < len(imageList)-1:
            self.cell_position +=1 
        else:
            self.cell_position = 0

        self.image = (imageList[self.cell_position])
        self.rect = self.image.get_rect()
        self.rect.x = rect[0] 
        self.rect.y = rect[1]         



# Create Sprite Objects which cause damage
# The number of sprites created equals the number of list value coordinate pairs)
def createDangerObjects(filename, frames, coord_list):
    for i in range (len(coord_list)):
        for coord in coord_list:
            danger = AnimatedSpriteSheet(CreateImageList(filename, frames), coord)
            animatedObjectGroup.add(danger)
            itemSpriteGroup.add(danger)
            
            danger_rect = HitBlock(coord)
            dangerGroup.add (danger_rect)
            
def createRewardObjects(filename, frames, coord_list):
    for i in range (len(coord_list)):
        for coord in coord_list:
            reward = AnimatedSpriteSheet(CreateImageList(filename, frames), coord)
            animatedObjectGroup.add(reward)
            itemSpriteGroup.add(reward)
           
# -----------------------------Lists-----------------------------------------------------

wall_list = [] # Add items that player can not pass through

#---------------------------------- SPRITE GROUPS -----------------------------------------

player_Sprite = pygame.sprite.Group()           # Add to blit_list last (bring to front screen)
itemSpriteGroup = pygame.sprite.Group()         # Add all interactive items
characterGroup = pygame.sprite.Group()          ######  NOT USED YET #########################
entityGroup = pygame.sprite.Group()             # Add to blit_list all static items

animatedObjectGroup = pygame.sprite.Group()     # Objects with animation effects

statsGroup = pygame.sprite.Group()              # Display dynamic stats
displayGroup = pygame.sprite.Group()            # Display images for Inventory & Statistics Bar

treasureGroup = pygame.sprite.Group()           # Player hits treasure
dangerGroup = pygame.sprite.Group()             # Player hits danger_RECT 

#------------------------------Game Variables---------------------------------------------

# clock variables
FPS = 18
CLOCK = pygame.time.Clock()

# colur variables
white = (255, 255, 255)
black = (0, 0, 0)
gold = (255, 204, 0)
green = (51, 153, 0)

# screen/display 

CELL_SIZE = 32
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

HALF_WIDTH = int(DISPLAY_WIDTH/ 2)
HALF_HEIGHT = int(DISPLAY_HEIGHT / 2)

TOTAL_LEVEL_WIDTH  = len(LEVEL_01[0])* CELL_SIZE # Top LEVEL_01 = actual map size
TOTAL_LEVEL_HEIGHT = len(LEVEL_01)* CELL_SIZE

DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
screen = pygame.display.set_mode(DISPLAY_SIZE) # actual screen

pygame.display.set_caption("Give it a NAME???????????")


#-------------------------------------Main Game Function-----------------
def main():
    pygame.init()
    up = down = left = right  = False    

    
    player = PlayerSprite()
    player.lifeForce = 312 # need to access the image rect here
    
    inventoryDisplay_Coords = (637,385)
    inventoryDisplay = StaticSpriteBlit (inventoryDisplay_Coords,"optImages/stats_32_opt.png", black)

    
    player_levelStats = TextStats([700, 575])   #Player level statistic
    player_wealthStats = TextStats([500, 575])  #Player wealth statistic
 

    statsBar_Coords = (2, 568)
    statsBar = StaticSpriteBlit (statsBar_Coords, "optImages/statsBar_32_opt.png", black)
    
    # MOVE OBJECTS TO LEVELS
    sheep1 = StaticImageSprite(576, 64, "images3/sheep32.png", black)    
    house1 = StaticImageSprite(1000, 16, "images3/house01_196.png", white)
                

    explodingBarrel_Coords = [(128,228), (256, 352), (364,364)]
    createDangerObjects("optImages/barrelsExploding2_32_opt.png", 13, explodingBarrel_Coords)

    pos1 = (160, 96)
    pos2 = (160, 160)
    treasure_01 = AnimatedSpriteSheet(CreateImageList("optImages/treasureChest_32opt.png", 3), pos1)
    treasure_02 = AnimatedSpriteSheet(CreateImageList("optImages/treasureChest_32opt.png", 3), pos2)

    p_pos1 = (200,200)
    potion_01 = AnimatedSpriteSheet(CreateImageList("optImages/potion_18_opt.png", 4), p_pos1)
    
    add_to_itemSpriteGroup = [sheep1, house1, treasure_01, treasure_02, potion_01]
    for item in add_to_itemSpriteGroup:
        itemSpriteGroup.add(item)

    add_to_treasureGroup = [treasure_01, treasure_02] # When hit specify objects frame to go to
    for item in add_to_treasureGroup:
        treasureGroup.add (item)

    add_to_animatedObjectGroup = [potion_01] # When player hits these the ojects animation plays
    for item in add_to_animatedObjectGroup:
        animatedObjectGroup.add(item)
##
##    add_to_dangerGroup = [] # Invisible hit blocks, remove once hit to avoid point lose loops
##    for item in add_to_dangerGroup:
##        dangerGroup.add (item)

        
    entityGroup.add(player)
    player_Sprite.add(player)
    
    displayGroup.add(statsBar)
    
    statsGroup.add(player_wealthStats)
    statsGroup.add(player_levelStats)    
    
    createLevel(TILE_SIZE, wall_list, entityGroup)
    camera = Camera(complex_camera, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT)    

    
    #--------------------------------Game Loop-------------------------------
    while True:

        CLOCK.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True                   
                if event.key == pygame.K_UP:
                    up = True                    
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_s:
                    displayGroup.add(inventoryDisplay)
                    
                if event.key == pygame.K_c:
                    displayGroup.remove(inventoryDisplay)                   

            if event.type == pygame.KEYUP:  

                if event.key == pygame.K_LEFT:
                    left = False                  
                if event.key == pygame.K_RIGHT:
                    right = False                    
                if event.key == pygame.K_UP:
                    up = False                   
                if event.key == pygame.K_DOWN:
                    down = False   

        hit_list = pygame.sprite.groupcollide(treasureGroup, player_Sprite, 0,0).keys()
        if hit_list:            
            for item in hit_list:                
                item.updateFrame(1)
                print "Found Coins. Do you want the booty? Press key a"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:                            
                        item.updateFrame(2)
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.wealth +=5 # Add wealth on keyup, then remove from hit list
                        item.updateFrame(2)
                        treasureGroup.remove(item)

        # dangerGroup contains invisible rect overlays for animated Objects, these are removed when
        # hit. This overlay allows the animation sequence of the object to run through to the end
        hit_dangerlist = pygame.sprite.groupcollide(dangerGroup, player_Sprite, 1,0).keys()
        if hit_dangerlist:            
            for item in hit_dangerlist:                
                player.lifeForce -= 10
            
        animated_ObjectList = pygame.sprite.groupcollide(animatedObjectGroup, player_Sprite, 0,0).keys()
        if animated_ObjectList:            
            for item in animated_ObjectList:
                item_reset = item
                item.animate()

                


                
        if player.lifeForce <=1:
            print "GAME OVER"


        camera.update(player)
        
        player.update(up, down, left, right, wall_list)        

        #Blit images per group, player the last in group so as to blit and bring forward
        blit_list = [entityGroup, characterGroup, itemSpriteGroup, player_Sprite]
        for groups in blit_list:
            for x in groups:
                screen.blit(x.image, camera.apply(x))
                
        displayGroup.draw(screen)# Draw Inventory and Statistics bar to screen

               
        update_lifeforce(statsBar, player.lifeForce)
        player_levelStats.update(player.level)
        player_wealthStats.update(player.wealth)
        statsGroup.draw(screen)

        
        pygame.display.update()

if __name__ == "__main__":
    main()       
