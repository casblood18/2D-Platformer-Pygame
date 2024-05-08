import pygame

#girl class
class girl(pygame.sprite.Sprite):  
    def __init__(self, x, y, BACKGROUND_X, BACKGROUND_Y):
        super().__init__()
        self.BACKGROUND_X, self.BACKGROUND_Y = BACKGROUND_X, BACKGROUND_Y
        #x, y size of girl sprite
        self.X_SIZE, self.Y_SIZE = 416, 454
        self.SCALE = 0.3

        #x, y of girl sprite SCALED
        self.X_SCALE = self.X_SIZE * self.SCALE
        self.Y_SCALE = self.Y_SIZE * self.SCALE

        #x, y velocity for movement
        self.X_VELOCITY = 7
        self.Y_VELOCITY = 5

        #idle animation frames
        self.idle_right_frames = [pygame.image.load(fr"png\Idle ({i}).png").convert_alpha() for i in range(1, 16)]
        self.idle_right_frames = [pygame.transform.scale(image, (self.X_SCALE, self.Y_SCALE)) for image in self.idle_right_frames]
        self.idle_left_frames = [pygame.transform.flip(image, True, False) for image in self.idle_right_frames]
        self.LENGTH_IDLE_FRAMES = len(self.idle_right_frames)

        #walk animation frames
        self.walk_right_frames = [pygame.image.load(fr"png\Walk ({i}).png").convert_alpha() for i in range(1, 20)]
        self.walk_right_frames = [pygame.transform.scale(image, (self.X_SCALE, self.Y_SCALE)) for image in self.walk_right_frames]
        self.walk_left_frames = [pygame.transform.flip(image, True, False) for image in self.walk_right_frames]
        self.LENGTH_WALK_FRAMES = len(self.walk_right_frames)

        #jump animation frames
        self.jump_right_frames = [pygame.image.load(fr"png\Jump ({i}).png").convert_alpha() for i in range(1, 30)]
        self.jump_right_frames = [pygame.transform.scale(image, (self.X_SCALE, self.Y_SCALE)) for image in self.jump_right_frames]
        self.jump_left_frames = [pygame.transform.flip(image, True, False) for image in self.jump_right_frames]
        self.LENGTH_JUMP_FRAMES = len(self.jump_right_frames)

        #running animation frames
        self.run_right_frames = [pygame.image.load(fr"png\Run ({i}).png").convert_alpha() for i in range(1, 20)]
        self.run_right_frames = [pygame.transform.scale(image, (self.X_SCALE, self.Y_SCALE)) for image in self.run_right_frames]
        self.run_left_frames = [pygame.transform.flip(image, True, False) for image in self.run_right_frames]
        self.LENGTH_RUN_FRAMES = len(self.run_right_frames)

        #dying animation frames
        # self.dead_right_frames = [pygame.image.load(fr"png\Dead ({i}).png").convert_alpha() for i in range(1, 30)]
        # self.dead_right_frames = [pygame.transform.scale(image, (601 * self.SCALE, 502 * self.SCALE)) for image in self.dead_right_frames]
        # self.dead_left_frames = [pygame.transform.flip(image, True, False) for image in self.dead_right_frames]
        # self.LENGTH_DEAD_FRAMES = len(self.dead_right_frames)

        #sets to true if user input keys
        self.jump_ = False
        self.run_ = False
        self.idle_ = False
        # self.dead_ = False

        #checks for no double jump
        self.one_jump = False
        
        #activates gravity for girl sprite to fall 
        self.fall_ = False
        
        #set the initial frame as the image when game loads
        self.image = self.idle_right_frames[0]
        
        #current frames per the sprite
        self.frame = 0
        self.idle_frame = 0
        self.run_frame = 0
        # self.dead_frame = 0
        self.walk_frame = 0

        #set direction of sprite | 0 = left | 1 = right
        self.direction = 1 

        #set direction of gravity | 0 = falling | 1 = not falling
        self.gravity = 1

        #size of character and placement
        self.rect = self.image.get_rect()
        # self.rect.width = int(self.rect.width * self.SCALE)
        # self.rect.height = int(self.rect.height * self.SCALE)
        self.rect.topleft = [x, y]
    
    def fall(self):
        self.fall_ = True

    def stop_fall(self):
        self.fall_ = False

    def jump(self):
        self.jump_ = True
        if not self.one_jump:
            #activate negative gravity to create a arc in the motion
            self.gravity = -23
            #true = cannot jump again
            self.one_jump = True
        

    def stop_jump(self):
        self.jump_ = False
        self.frame = 0
        self.one_jump = False

    def run(self):
        self.run_ = True
    
    def stop_run(self):
        self.run_ = False
        self.run_frame = 0

    def idle(self):
        self.idle_ = True
    
    # def dead(self):
    #     print(self.rect)
    #     print(self.rect.right)
    #     print(self.rect.left)
    #     self.dead_ = True
    
    def right_direction(self):
        self.direction = 1
    
    def left_direction(self):
        self.direction = 0
    
    def update(self, speed):
        #dying animation
        # if self.dead_:
        #     if self.direction:
        #         self.image = self.dead_right_frames[int(self.dead_frame)]
        #     else:
        #         self.image = self.dead_left_frames[int(self.dead_frame)]
        #     self.dead_frame += speed * 0.7
        #     if self.dead_frame >= self.LENGTH_DEAD_FRAMES:
        #         self.dead_frame = 0
        #         self.dead_ = False

        #jumping facing right
        if self.jump_:
            if self.rect.y + self.gravity <= 435:
                self.gravity += 1
                self.rect.y += self.gravity
            else:  
                self.rect.y = 435
                self.stop_jump()
            if self.direction == 1:
                self.image = self.jump_right_frames[int(self.frame)]
                if self.run_ and ((self.rect.right + self.X_VELOCITY) < self.BACKGROUND_X):
                    self.rect.x += self.X_VELOCITY
            #jumping facing left if direction is 0
            else:
                self.image = self.jump_left_frames[int(self.frame)]
                if self.run_ and ((self.rect.left - self.X_VELOCITY) >= 0):
                    self.rect.x -= self.X_VELOCITY
            #frame iteration for jump animation
            self.frame += speed
            if int(self.frame) >= self.LENGTH_JUMP_FRAMES:
                self.frame = 0

        #running facing right
        elif self.run_:
            if self.direction == 1:
                self.image = self.run_right_frames[int(self.run_frame)]
                if((self.rect.right + self.X_VELOCITY) < self.BACKGROUND_X):
                    self.rect.x += self.X_VELOCITY
            #jumping facing left if direction is 0
            else:
                self.image = self.run_left_frames[int(self.run_frame)]
                if((self.rect.left - self.X_VELOCITY) >= 0):
                    self.rect.x -= self.X_VELOCITY
            #frame iteration for run animation
            self.run_frame += speed
            if int(self.run_frame) >= self.LENGTH_RUN_FRAMES:
                self.run_frame = 0
                self.run_ = False

        #walking when edge of screen
        elif self.rect.left < 10:
            self.image = self.walk_right_frames[int(self.walk_frame)]
            self.walk_frame += (speed * 0.8)
            if int(self.walk_frame) >= self.LENGTH_WALK_FRAMES:
                self.walk_frame = 0

        #idle facing right
        elif self.idle_:
            if self.direction:
                self.image = self.idle_right_frames[int(self.idle_frame)]
            #idle facing left if direction is 0
            else:
                self.image = self.idle_left_frames[int(self.idle_frame)]
            #frame iteration for idle animation
            self.idle_frame += (speed * 0.8)
            if int(self.idle_frame) >= self.LENGTH_IDLE_FRAMES:
                self.idle_frame = 0
            
        if self.fall_ and not self.jump_:
            self.gravity = 0
            self.jump_ = True

if __name__ == "__main__":
    print("THIS IS THE GIRL.PY")