import pygame

class tile(pygame.sprite.Sprite):
    
    def __init__(self, X_BACKGROUND, Y_BACKGROUND, X_VALUE = 0, Y_VALUE = 0, TILE = "FLOOR", groups = None):
        super().__init__(groups)

        self.X_VALUE = X_VALUE 
        self.Y_VALUE = Y_VALUE
        self.X_BACKGROUND = X_BACKGROUND
        self.Y_BACKGROUND = Y_BACKGROUND
        #tile type
        self.TILE = TILE
        #tile speed
        self.X_VELOCITY = -5

        #creates the platform tiles
        if self.TILE == "MIDDLE":
            self.image = pygame.image.load(r"background\slice.png").convert_alpha()
        elif self.TILE == "RIGHT":
            self.image = pygame.image.load(r"background\slice_left.png").convert_alpha()
        elif self.TILE == "LEFT":
            self.image = pygame.image.load(r"background\slice_right.png").convert_alpha()
        elif self.TILE == "FLOOR":
            self.image = pygame.image.load(r"background\slice.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.X_VALUE, self.Y_VALUE)

    def move(self):
        #linear movement 
        self.rect.x += self.X_VELOCITY
        #floor tiles
        if self.rect.right < 0 and self.TILE == "FLOOR":
            self.rect.x = self.X_BACKGROUND
        #platform tiles 
        if self.rect.right < 0 and self.TILE != "FLOOR":
            self.kill()
    
    def update(self):
        self.move()

if __name__ == "__main__":
    print("THIS IS THE TILES.PY")
