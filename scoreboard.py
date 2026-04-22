import pygame

FONT = ("Times New Roman", 36, "bold")

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.day = 1
        self.pages_collected = 0
        self.trash_collected = 0
        self.infection_rate = 0
        self.pending_win = False          # set when 7 pages collected not sleep yet
        self.win_message_screen = False   
        self.game_won = False

        self.font = pygame.font.SysFont(FONT[0], FONT[1])

    def reset(self):
        self.score = 0
        self.day = 1
        self.pages_collected = 0
        self.trash_collected = 0
        self.infection_rate = 0
        self.pending_win = False
        self.win_message_screen = False

    def increase_day(self):
        self.day += 1
        self.score = 0   # reset daily score

    def add_page(self):
        self.pages_collected += 1
        if self.pages_collected >= 7:
            self.pending_win = True   

    def add_trash(self):
        self.trash_collected += 1

    def increase_infection(self, amount=1):
        self.infection_rate += amount
        if self.infection_rate > 100:
            self.infection_rate = 100

    def calculate_score(self, player, game_status=None):
        if game_status:
            trash_points = game_status.total_inventory.get("Trash", 0) * 10
            remains_points = game_status.total_inventory.get("Zombie Remains", 0) * 50
        else:
            trash_points = player.inventory.get("Trash", 0) * 10
            remains_points = player.inventory.get("Zombie Remains", 0) * 50

        self.score = trash_points + remains_points
        return self.score

    def draw(self, screen, story_mode=False):
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        day_text = font.render(f"Day: {self.day}", True, (255, 255, 255))
        infection_text = font.render(f"Infection: {self.infection_rate}%", True, (255, 100, 100))

        screen.blit(score_text, (10, 10))
        screen.blit(day_text, (10, 40))
        screen.blit(infection_text, (10, 70))

        if story_mode:
            page_text = font.render(f"Pages: {self.pages_collected}/7", True, (255, 255, 255))
            screen.blit(page_text, (10, 100))

    def draw_win_message(self, screen):
        # after 7 page 
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        screen.blit(fade_surface, (0, 0))

        font_large = pygame.font.SysFont("Times New Roman", 36, bold=True)
        font_small = pygame.font.SysFont("Times New Roman", 24)
        font_smaller = pygame.font.SysFont("Times New Roman", 10)

        text1 = font_large.render("You collected all 7 pages!", True, (255, 255, 255))
        text2 = font_small.render("This is where I would put the story", True, (255, 255, 200))
        text3 = font_small.render("If I had one...", True, (255, 255, 200))
        text4 = font_smaller.render("Press SPACE", True, (200, 200, 100))

        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        screen.blit(text1, (center_x - text1.get_width() // 2, center_y - 80))
        screen.blit(text2, (center_x - text2.get_width() // 2, center_y - 20))
        screen.blit(text3, (center_x - text3.get_width() // 2, center_y + 10))
        screen.blit(text4, (center_x - text4.get_width() // 2, center_y + 60))

    def game_over(self, screen, fade_alpha, player, game_status):
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Handle different endings
        if self.game_won:
            text1 = self.font.render("YOU WIN!", True, (0, 255, 0))
        elif self.pages_collected >= 7 and not self.pending_win:
            # Player had 7 pages but didn’t sleep
            text1 = self.font.render("GAME OVER", True, (255, 0, 0))
            reason = self.font.render("You collected 7 pages but didn’t make it to bed!", True, (255, 255, 255))
            screen.blit(reason, (screen.get_width()//2 - reason.get_width()//2,
                                 screen.get_height()//2 + 90))
        else:
            text1 = self.font.render("GAME OVER", True, (255, 0, 0))

        text2 = self.font.render("Press SPACE", True, (255, 255, 255))
        screen.blit(text1, (screen.get_width()//2 - text1.get_width()//2,
                            screen.get_height()//2 - 50))
        screen.blit(text2, (screen.get_width()//2 - text2.get_width()//2,
                            screen.get_height()//2 + 10))

        # Final Score
        font_small = pygame.font.SysFont(None, 28)
        final_score = self.calculate_score(player, game_status)
        score_text = font_small.render(f"Final Score: {final_score}", True, (255, 255, 0))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2,
                                 screen.get_height()//2 + 50))

        #Daily inventory
        y = screen.get_height()//2 + 80
        screen.blit(font_small.render("Daily Inventory:", True, (255, 255, 255)), (50, y))
        y += 30
        for item, count in player.inventory.items():
            screen.blit(font_small.render(f"- {item}: {count}", True, (200, 200, 200)), (70, y))
            y += 25

        #Lifetime totals
        y += 20
        screen.blit(font_small.render("Total Collected:", True, (255, 255, 255)), (50, y))
        y += 30
        for item, count in game_status.total_inventory.items():
            screen.blit(font_small.render(f"- {item}: {count}", True, (200, 200, 200)), (70, y))
            y += 25
