import pygame
import sys
import girl
import tiles
import random
import birds

#570 is floor height
pygame.init()
SCALE = 5
BACKGROUND_X, BACKGROUND_Y = 256 * SCALE, 128 * SCALE
screen = pygame.display.set_mode((BACKGROUND_X, BACKGROUND_Y))
clock = pygame.time.Clock()
pygame.display.set_caption("Girl Jump Bird")

#models
girl = girl.girl(120, 435, BACKGROUND_X, BACKGROUND_Y)
sprites = pygame.sprite.Group(girl)

#bird sprites
bird_sprites = pygame.sprite.Group()

#floor tiles
tile_sprites = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
checker = -30
right = 1400
while checker < right:
    tiles.tile(BACKGROUND_X, BACKGROUND_Y, right, 570, "FLOOR", floor_sprites)
    right -= 70

test_font = pygame.font.Font("Fonts\slkscr.ttf", 50)
start_time = 0

def display_score():
    global start_time
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (600,50))
    screen.blit(score_surf,score_rect)
    return current_time
    
#platform sprites
def platform_sprites(size):
    right = 2000
    tiles.tile(BACKGROUND_X, BACKGROUND_Y, right, 350, "LEFT", tile_sprites)
    right -= 70
    for _ in range(size):
        tiles.tile(BACKGROUND_X, BACKGROUND_Y, right, 350, "MIDDLE", tile_sprites)
        right -= 70
    tiles.tile(BACKGROUND_X, BACKGROUND_Y, right, 350, "RIGHT", tile_sprites)

bird_shuffle = [450, 255, 200, 420]
#bird sprites
def make_bird(score):
    bird = birds.bird(bird_sprites, score)
    random.shuffle(bird_shuffle)
    bird.rect.y = bird_shuffle[0]

#check for direction the collision occurred
def collision_direction(obstacle):
    # print(obstacle.rect.top - girl.rect.bottom)
    if(10 > girl.rect.bottom - obstacle.rect.top > 0):
        return "DOWN"
    else:
        return None

def check_collision():
    #checks collision on the platform tiles
    for tile in tile_sprites:
        if girl.rect.colliderect(tile):
            direction = collision_direction(tile)
            if direction == "DOWN":
                girl.rect.bottom = tile.rect.top + 3
                if girl.rect.left > 5:
                    girl.rect.x -= 5
                girl.stop_jump()
                girl.stop_fall()
                return
            
    #checks collision on the floor tiles
    for floor in floor_sprites:
        if girl.rect.colliderect(floor):
            direction = collision_direction(floor)
            if direction == "DOWN":
                girl.rect.bottom = floor.rect.top + 3
                if girl.rect.left > 5:
                    girl.rect.x -= 5
                girl.stop_jump()
                girl.stop_fall()
                return
    #if no collision -> girl falls
    girl.fall()

#platform event
PLAT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PLAT_EVENT, 2500)

#bird event
BIRD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_EVENT, 2000)

#start menu screen
def start():
    #girl idle animation frames
    idle_frames = [pygame.image.load(fr"png\Idle ({i}).png").convert_alpha() for i in range(1, 16)]
    # idle_frames = [pygame.transform.scale(image, (self.X_SCALE, self.Y_SCALE)) for image in idle_frames]
    LENGTH_IDLE_FRAMES = len(idle_frames)
    idle_frame = 0
    image = idle_frames[idle_frame]

    #start menu
    start_running = True
    while start_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
                sys.exit()
            #SPACE to begin game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_running = False
                #goes to play display
                play()
        
        #background color and idle animation on screen
        screen.fill((255, 208, 198))
        if idle_frame >= LENGTH_IDLE_FRAMES:
            idle_frame = 0
        image = idle_frames[int(idle_frame)]
        idle_frame += 0.015
        screen.blit(image, (100, 50))

        #start message blit
        start_message = test_font.render(f"PRESS SPACE TO START", False, (236, 115, 89))
        screen.blit(start_message, (540,250))
        pygame.display.flip()

def play():
    #load gif background 
    background = [pygame.image.load(fr"background\Nowy\aaaaaaaaaaa {i}.png").convert_alpha() for i in range(1, 24)]
    background_frame = 0
    background = [pygame.transform.scale(image, (BACKGROUND_X, BACKGROUND_Y)) for image in background]
    LENGTH_BACKGROUND_FRAMES = len(background)

    #empty sprite groups to start new game
    bird_sprites.empty()
    tile_sprites.empty()

    #reset girl position
    girl.rect.topleft = [120, 435]
    score = 0

    #game starting
    play_running = True
    while play_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_running = False
                sys.exit()
            if event.type == PLAT_EVENT:
                #size of platform
                size = random.randint(2,5)
                #creates platform sprites and sent into tile sprite group
                platform_sprites(size)
            if event.type == BIRD_EVENT:
                #score = bird speed relation to score time
                make_bird(score)

        #if bird collides with girl, game ends and changes to END display
        for bird in bird_sprites:
            if girl.rect.colliderect(bird):
                tile_sprites.empty()
                bird_sprites.empty()
                return end(girl.rect.topleft, score)

        check_collision()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            girl.jump()

        if not any(keys):
            girl.stop_run()
            girl.idle()

        if keys[pygame.K_RIGHT]:
            girl.right_direction()
            girl.run()

        if keys[pygame.K_LEFT]: 
            girl.left_direction()
            girl.run()

        #iterates the gif background
        screen.blit(background[int(background_frame)],(0, 0))
        background_frame = (background_frame + 0.2) % LENGTH_BACKGROUND_FRAMES
            
        #draw the sprites and tiles
        sprites.draw(screen)
        tile_sprites.draw(screen)
        floor_sprites.draw(screen)

        #sprite hitbox 
        # hitbox_rect = girl.rect.copy()
        # pygame.draw.rect(screen, (0,0,255), hitbox_rect, 2)

        #updates all the sprites and backgrounds. Displays score on top 
        score = display_score()
        bird_sprites.draw(screen)
        sprites.update(.5)
        tile_sprites.update()
        floor_sprites.update()
        bird_sprites.update()

        pygame.display.flip()
        clock.tick(60)

def end(location, score):
    global start_time
    #kill screen animation for girl sprite
    dead_frame = 0
    dead_frames = [pygame.image.load(fr"png\Dead ({i}).png").convert_alpha() for i in range(1, 30)]
    dead_frames = [pygame.transform.scale(image, (601 * 0.5, 502 * 0.5)) for image in dead_frames]
    LENGTH_DEAD_FRAMES = len(dead_frames)
    DEAD_FRAME_SPEED = 0.008
    image = dead_frames[0]

    #end menu
    end_running = True
    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                end_running = False
                #get new start time so score starts at 0 in the new run
                start_time = int(pygame.time.get_ticks()/1000)
                #back to start menu
                start()
        #dead frame animation, stops at final frame
        if dead_frame < LENGTH_DEAD_FRAMES:
            image = dead_frames[int(dead_frame)]
            #dead frame animation speed 
            dead_frame += DEAD_FRAME_SPEED
        
        #change background / GAME OVER screen
        screen.fill((236, 115, 89))
        screen.blit(image, location)
        score_message = test_font.render(f'Score: {score}',False,(111,196,169))
        game_over_message = test_font.render(f'GAME OVER',False,(111,196,169))
        screen.blit(score_message, (500, 200))
        screen.blit(game_over_message, (470, 150))
        pygame.display.flip()

#game start
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    start()

#close game 
pygame.quit()
sys.exit()
