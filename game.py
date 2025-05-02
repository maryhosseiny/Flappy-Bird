import pygame
from pygame.locals import *
import random

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
button_img = pygame.image.load('img/restart.png')

font = pygame.font.SysFont('Bauhuas 93', 60)
white = (255, 255, 255) 

#variables
ground_scroll = 0
scroll_speed = 4
ground_y = screen_height - ground_img.get_height()
flying = False
game_over = False
pipe_gap = 200 #pixels
pipe_frq = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frq
score = 0
pass_pipe = False

def draw_text(text, font, text_col, x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    flying = False
    score = 0
    return score

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
        self.clicked = False
    
    def update(self, *args, **kwargs):
        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 820:
                self.rect.y += int(self.vel)
        if game_over == False:
            #up/down motion
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #flap motion
            self.counter += 1
            flap_cool = 7
            if self.counter > flap_cool:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-3)
        else: 
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/obs.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]
    
    def update(self, *args, **kwargs):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(-100, screen_height)
        self.speed = random.uniform(0.3, 1.2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-150, -40)
            self.rect.x = random.randint(0, screen_width)


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

background_group = pygame.sprite.Group()

floating_paths = [
    'img/shard1.png', 'img/shard2.png', 'img/shard3.png',
    'img/shard4.png', 'img/shard5.png', 'img/shard6.png',
    'img/shard7.png', 'img/shard8.png'
]

# Add multiple of each for variety
for path in floating_paths:
    for _ in range(2):  # two of each for more visual interest
        background_group.add(BackgroundObject(path))


flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)  

button = Button(screen_width//2 - 196 // 2, screen_height//2 - 79 // 2, button_img)


run = True
while run:
    clock.tick(fps)

    # background photo adding
    screen.blit(bg, (0,0))

    background_group.update()
    background_group.draw(screen)

    #bird on screen
    bird_group.draw(screen)
    bird_group.update(screen)
    pipe_group.draw(screen)


    #ground photo adding
    for x in range(0, screen_width + ground_img.get_width(), ground_img.get_width()):
        screen.blit(ground_img, (x + ground_scroll, ground_y))
    
    #checking score 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
           if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
               score += 1
               pass_pipe = False 

    draw_text(str(score), font, white, int(screen_width/2), 20)

    #collision 
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #checking for bird hitting the ground
    if flappy.rect.bottom > 815:
        game_over = True
        flying = False



    #ground photo scrolling
    if game_over == False and flying == True: 
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frq:
            pipe_height = random.randint(-100,100)

            btm_pipe = Pipe(screen_width,int(screen_height/2) + pipe_height,-1)
            top_pipe = Pipe(screen_width,int(screen_height/2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)   
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > ground_img.get_width():
            ground_scroll = 0
        pipe_group.update()

    #resetting
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()


    # ending the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.QUIT