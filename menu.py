import pygame 

import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.smoll_font = pygame.font.SysFont(None, 30)

        # Main menu buttons
        self.start_button = pygame.Rect(300, 250, 200, 80)
        self.quit_button = pygame.Rect(300, 470, 200, 80)

        #Story mode
        self.story_button = pygame.Rect(300, 360, 200, 80)
        self.story_mode = False


        # Pause menu buttons
        self.continue_button = pygame.Rect(300, 250, 200, 80)
        self.pause_quit_button = pygame.Rect(300, 360, 200, 80)

        self.active = True
        self.start_game = False
        self.paused = False

    def draw_main(self):
        self.screen.fill((30, 30, 30))
        title = self.font.render("Shoot it down Pick it up", True, (255, 255, 255))
        sub_title = self.smoll_font.render("Demo 1", True, (225, 225, 225))
        
        center_x = 400
        self.screen.blit(title, (center_x - title.get_width() //2, 150))
        self.screen.blit(sub_title, (center_x - sub_title.get_width() //2, 150 + title.get_height()))

        mouse_pos = pygame.mouse.get_pos()  # current mouse position

        # Start button
        start_color = (0, 200, 0) if self.start_button.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(self.screen, start_color, self.start_button)
        start_text = self.font.render("Start", True, (255, 255, 255))
        self.screen.blit(start_text, start_text.get_rect(center=self.start_button.center))

        # Story Mode button
        story_color = (200, 0, 200) if self.story_button.collidepoint(mouse_pos) else (0, 0, 150)
        pygame.draw.rect(self.screen, story_color, self.story_button)
        story_text = self.font.render("Story Mode", True, (255, 255, 255))
        self.screen.blit(story_text, story_text.get_rect(center=self.story_button.center))

        # Quit button
        quit_color = (200, 0, 0) if self.quit_button.collidepoint(mouse_pos) else (150, 0, 0)
        pygame.draw.rect(self.screen, quit_color, self.quit_button)
        quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))

        pygame.display.flip()

    def draw_pause(self, frozen_frame):
        # Draw the frozen game scene
        self.screen.blit(frozen_frame, (0, 0))

        # Semi-transparent black overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))  # black with alpha
        self.screen.blit(overlay, (0, 0))

        # Pause title and buttons
        title = self.font.render("Paused", True, (255, 255, 255))
        self.screen.blit(title, (320, 150))

        pygame.draw.rect(self.screen, (0, 200, 0), self.continue_button)
        cont_text = self.font.render("Continue", True, (255, 255, 255))
        self.screen.blit(cont_text, cont_text.get_rect(center=self.continue_button.center))

        pygame.draw.rect(self.screen, (200, 0, 0), self.pause_quit_button)
        quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.pause_quit_button.center))

        pygame.display.flip()


    def handle_event_main(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.active = False
                self.start_game = True
                self.story_mode = False   # Normal mode
            elif self.story_button.collidepoint(event.pos):
                self.active = False
                self.start_game = True
                self.story_mode = True    # Story mode
            elif self.quit_button.collidepoint(event.pos):
                pygame.quit()
                exit()


    def handle_event_pause(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                self.paused = False
            elif self.pause_quit_button.collidepoint(event.pos):
                pygame.quit()
                exit()

    def draw_sleep_popup(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        text1 = self.font.render("Go to sleep?", True, (255, 255, 255))
        text2 = self.font.render("Press Y for Yes, N for No", True, (200, 200, 200))

        screen.blit(text1, (screen.get_width()//2 - text1.get_width()//2,
                            screen.get_height()//2 - 40))
        screen.blit(text2, (screen.get_width()//2 - text2.get_width()//2,
                            screen.get_height()//2))

        pygame.display.flip()
