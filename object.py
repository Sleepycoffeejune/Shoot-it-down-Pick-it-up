import pygame, random

class Page(pygame.sprite.Sprite):
    def __init__(self, BG):
        super().__init__()
        # Load page image
        self.image = pygame.image.load("collectables/page.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()

        # Choose random background (excluding home_bg)
        possible_bgs = [
            BG.crossroad_bg, BG.road_x1_bg, BG.road_x2_bg,
            BG.road_y1_bg, BG.road_y2_bg,
            BG.sand_bg1, BG.sand_bg2, BG.sand_bg3, BG.sand_bg4
        ]
        self.spawn_bg = random.choice(possible_bgs)

        # Random position inside the map
        self.rect.center = (random.randint(100, 700), random.randint(100, 500))

        self.collected = False

    def collect(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            return True  # signal collected
        return False



import pygame
import random

class Trash(pygame.sprite.Sprite):
    def __init__(self, BG):
        super().__init__()
        self.image = pygame.image.load("collectables/trash.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()

        # Define valid backgrounds (exclude home_bg)
        valid_bgs = [
            BG.crossroad_bg, BG.road_x1_bg, BG.road_x2_bg,
            BG.road_y1_bg, BG.road_y2_bg,
            BG.sand_bg1, BG.sand_bg2, BG.sand_bg3, BG.sand_bg4
        ]
        self.spawn_bg = random.choice(valid_bgs)

        # Random position inside the map, avoiding borders
        attempts = 0
        while True:
            self.rect.x = random.randint(50, BG.image.get_width() - 50)
            self.rect.y = random.randint(50, BG.image.get_height() - 50)
            if self.valid_spawn(BG):
                break
            attempts += 1
            if attempts > 100:  # safeguard
                break

        self.collected = False

    def collect(self):
        self.collected = True
        return True

    
    def valid_spawn(self, BG):
        for border in BG.get_borders():
            if self.rect.colliderect(border):
                return False
        return True
