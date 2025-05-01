import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 935

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# images 
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1, 4):
            img = pygame.image.load(f'img/frame{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
    
    def update(self, *args, **kwargs):

        #gravity
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 812:
            self.rect.y += int(self.vel)
        
        #up/down motion
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #flap motion
        self.counter += 1
        flap_cool = 10
        if self.counter > flap_cool:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        self.image = pygame.transform.rotate(self.images[self.index], self.vel*-3)
  

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

#variables
ground_scroll = 0
scroll_speed = 4
ground_y = screen_height - ground_img.get_height()


run = True
while run:
    clock.tick(fps)

    # background photo adding
    screen.blit(bg, (0,0))

    #bird 
    bird_group.draw(screen)
    bird_group.update(screen)

    #ground photo adding
    for x in range(0, screen_width + ground_img.get_width(), ground_img.get_width()):
        screen.blit(ground_img, (x + ground_scroll, ground_y))

    #ground photo scrolling
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > ground_img.get_width():
        ground_scroll = 0

    # ending the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.QUIT