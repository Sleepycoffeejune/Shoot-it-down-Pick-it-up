import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # base bullet shape (horizontal)
        base_image = pygame.Surface((12, 4), pygame.SRCALPHA)
        base_image.fill((255, 255, 0))  # yellow

        # rotate depending on direction
        if direction == "facing":   # down
            self.image = pygame.transform.rotate(base_image, 90)
        elif direction == "back":   # up
            self.image = pygame.transform.rotate(base_image, -90)
        elif direction == "left":
            self.image = base_image  # already horizontal
        elif direction == "right":
            self.image = base_image

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20
        self.direction = direction

    def update(self):
        if self.direction == "facing":   # down
            self.rect.y += self.speed
        elif self.direction == "back":   # up
            self.rect.y -= self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # remove if off screen
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()
