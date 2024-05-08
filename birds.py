import pygame

class bird(pygame.sprite.Sprite):
    def __init__(self, group, speed):
        self.bird_frame = 0
        self.SCALE = 0.6
        #bird size 259 x 146 give or take
        self.X_SCALE = 259 * self.SCALE
        self.Y_SCALE = 146 * self.SCALE
        #speed increases per time
        self.speed = speed
        super().__init__(group)

        #bird animation frames
        self.bird_frames = [pygame.image.load(fr"bird\skeleton-animation_0{i}.png").convert_alpha() for i in range(0,10)]
        self.bird_frames = [pygame.transform.scale(image,(self.X_SCALE, self.Y_SCALE)) for image in self.bird_frames]
        self.bird_frames = [pygame.transform.flip(image, True, False) for image in self.bird_frames]
        
        #bird position, initial frame, and rect size
        FRAMES_LENGTH = 4
        self.image = self.bird_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (1400,0)
        
    def move(self):
        self.speed /= 10
        self.speed += 5
        #if max level, speed = 25
        if self.speed > 25:
            self.speed = 25
        self.rect.x -= self.speed
        #sprite removed when off-screen
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.move()
        #animation frame change speed
        self.bird_frame += 0.4
        self.image = self.bird_frames[int(self.bird_frame)]
        if self.bird_frame >= 9:
            self.bird_frame = 0

if __name__ == "__main__":
    print("THIS IS THE BIRDS.PY")