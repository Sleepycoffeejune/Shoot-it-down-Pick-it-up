import pygame
import sys

# Initialize PyGame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Buttons Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 204)
LIGHT_BLUE = (0, 162, 255)

GREY = (156, 156, 156)
YELLOW = (255, 181, 38)

# Font
FONT = pygame.font.SysFont("Courier", 36, bold=True)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = GREY
        self.hover_color = YELLOW

    def draw(self, surface):
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Draw text centered
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Example button actions
def start_game():
    print("Game Started!")

def show_instructions():
    print("Showing Instructions...")

def quit_game():
    pygame.quit()
    sys.exit()

# Create buttons
buttons = [
    Button(200, 100, 200, 50, "Start Game", start_game),
    Button(200, 170, 200, 50, "Instructions", show_instructions),
    Button(200, 240, 200, 50, "Quit", quit_game)
]

# Main loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for button in buttons:
            button.check_click(event)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
