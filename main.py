import pygame
import sys
import keyboard

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Import images
        bepbl_idle = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_idle.png"))
        bepbl_idle2 = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_idle2.png"))
        
        bepbl_run = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_run.png"))
        bepbl_run2 = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_run2.png"))
        bepbl_run3 = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_run3.png"))
        bepbl_run21 = pygame.transform.scale2x(pygame.image.load("sprites/bepbl_run2.1.png"))
        
        bepbl_fall = pygame.transform.scale2x(pygame.image.load("sprites/hero_duck.png"))
        bepbl_skrt = pygame.transform.scale2x(pygame.image.load("sprites/hero_walk1.png"))
        
        # Images for animation
        self.idle_images = [bepbl_idle, bepbl_idle2]
        self.run_images = [bepbl_run, bepbl_run21] #bepbl_run3, bepbl_run2, bepbl_run3]
        self.fall_image = bepbl_fall
        self.skrt_image = bepbl_skrt
        
        # Animation variables
        self.current_animation = self.idle_images
        self.animation_index = 0
        self.flip = False
        
        # Create image and rect
        self.rect_x = 800
        self.rect_y = 400
        self.image = self.current_animation[self.animation_index]
        self.rect = self.image.get_rect(center = (self.rect_x, self.rect_y ))
        
        # Movement variables
        self.max_velocity = 10
        self.velocity = 0
        self.acceleration = 0.5
        self.friction = 0.5
    
    # Animation functions
    def animate_idle(self):
        self.current_animation = self.idle_images
        self.animation_index += 0.02
        if self.animation_index > len(self.idle_images):
            self.animation_index = 0
        self.image = self.idle_images[int(self.animation_index)]
    
    def animate_move(self):
        self.current_animation = self.run_images
        self.animation_index += 0.05
        if self.animation_index > len(self.run_images):
            self.animation_index = 0
        if self.flip:
            self.image = pygame.transform.flip(self.run_images[int(self.animation_index)], True, False)
        else:
            self.image = self.run_images[int(self.animation_index)]
    
    def animate_skrt(self):
        self.image = self.skrt_image


    def animate_fall(self):

        self.image = self.fall_image

    
    # Movement functions
    def movement_right(self):
        self.rect.x += self.velocity
    
    def movement_left(self):
        self.rect.x -= self.velocity

    def move_right(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.movement_right()
    
    def move_left(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.movement_left()
    
    def stop_right(self):
        self.velocity = max(self.velocity - self.friction / 2, 0)
        self.movement_right()
    
    def stop_left(self):
        self.velocity = max(self.velocity - self.friction / 2, 0)
        self.movement_left()
    
pygame.init()
screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player())

direction = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
    
    if player.sprite.rect.x < 0:
        player.sprite.rect.x = 1700
    if player.sprite.rect.x > 1800:
        player.sprite.rect.x = 10
    
    player.sprite.rect.bottom = 481
    moved = False
    
    if player.sprite.velocity == 0:
        idle = True
    
    
    print(player.sprite.rect.bottom)
    
    key = pygame.key.get_pressed()
    right = key[pygame.K_RIGHT]
    left = key[pygame.K_LEFT]
    
    if right:
        player.sprite.move_right()
        player.sprite.animate_move()
        player.sprite.flip = False
        moved = True
        idle = False
        direction = 1

    if left:
        player.sprite.move_left()
        player.sprite.animate_move()
        player.sprite.flip = True
        moved = True
        idle = False
        direction = 2
    
    if right and left:
        # rect.bottom == 481
        player.sprite.rect.bottom = 600
        player.sprite.animate_fall()
    
    if not moved and direction == 1:
        player.sprite.animate_skrt()
        player.sprite.stop_right()
    
    if not moved and direction == 2:
        player.sprite.animate_skrt()
        player.sprite.stop_left()
    
    if idle:
        player.sprite.animate_idle()
    
   
    screen.fill("Gray") 
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)