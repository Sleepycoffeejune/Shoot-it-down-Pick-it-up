import pygame


STARTING_POSITION = (400, 300)
MOVE_DISTANCE = 15
HEALTH = 300
ATTACK = 10


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # iddle images
        self.img_facing = pygame.image.load("player_img/01_player W.png").convert_alpha()
        self.img_back = pygame.image.load("player_img/01_player S.png").convert_alpha()
        self.img_left = pygame.image.load("player_img/01_player A.png").convert_alpha()
        self.img_right = pygame.image.load("player_img/01_player D.png").convert_alpha()

        # walking image
        self.img_walking_front = [pygame.image.load("player_img/01_walking F1.png").convert_alpha(), self.img_facing ,pygame.image.load("player_img/01_walking F2.png").convert_alpha()]
        self.img_walking_back = [pygame.image.load("player_img/01_walking B1.png").convert_alpha(),self.img_back ,pygame.image.load("player_img/01_walking B2.png").convert_alpha()]
        self.img_walking_left = [pygame.image.load("player_img/01_walking A.png").convert_alpha(), self.img_left]   
        self.img_walking_right = [pygame.image.load("player_img/01_walking D.png").convert_alpha(), self.img_right]

        # gun out
        self.gun_front1 = pygame.image.load("player_img/gun_Front1.png").convert_alpha()
        self.gun_front2 = pygame.image.load("player_img/gun_Front2.png").convert_alpha()
        self.gun_front3 = pygame.image.load("player_img/gun_Front3.png").convert_alpha()
        self.gun_front = [self.gun_front1, self.gun_front2, self.gun_front3]

        self.gun_back1 = pygame.image.load("player_img/gun_Back1.png").convert_alpha()
        self.gun_back2 = pygame.image.load("player_img/gun_Back2.png").convert_alpha()
        self.gun_back3 = pygame.image.load("player_img/gun_Back3.png").convert_alpha()
        self.gun_back = [self.gun_back1, self.gun_back2, self.gun_back3]

        self.gun_R1 = pygame.image.load("player_img/gun_R1.png").convert_alpha()
        self.gun_R2 = pygame.image.load("player_img/gun_R2.png").convert_alpha()
        self.gun_right = [self.gun_R1, self.gun_R2]
        
        self.gun_L1 = pygame.image.load("player_img/gun_L1.png").convert_alpha()        
        self.gun_L2 = pygame.image.load("player_img/gun_L2.png").convert_alpha()
        self.gun_left = [self.gun_L1, self.gun_L2]        
        
        # Scale
        self.img_facing = pygame.transform.scale(self.img_facing, (120, 120))
        self.img_back = pygame.transform.scale(self.img_back, (120, 120))
        self.img_left = pygame.transform.scale(self.img_left, (120, 120))
        self.img_right = pygame.transform.scale(self.img_right, (120, 120))

        self.img_walking_front = [pygame.transform.scale(img, (120, 120)) for img in self.img_walking_front]
        self.img_walking_back = [pygame.transform.scale(img, (120, 120)) for img in self.img_walking_back]
        self.img_walking_left = [pygame.transform.scale(img, (120, 120)) for img in self.img_walking_left]
        self.img_walking_right = [pygame.transform.scale(img, (120, 120)) for img in self.img_walking_right]

        self.gun_front = [pygame.transform.scale(img, (120, 120)) for img in self.gun_front]
        self.gun_back = [pygame.transform.scale(img, (120, 120)) for img in self.gun_back]
        self.gun_left = [pygame.transform.scale(img, (120, 120)) for img in self.gun_left]
        self.gun_right = [pygame.transform.scale(img, (120, 120)) for img in self.gun_right]
       
        # Masks
        self.mask_facing = pygame.mask.from_surface(self.img_facing)
        self.mask_back = pygame.mask.from_surface(self.img_back)
        self.mask_left = pygame.mask.from_surface(self.img_left)
        self.mask_right = pygame.mask.from_surface(self.img_right)

        self.mask_walking_front = [pygame.mask.from_surface(img) for img in self.img_walking_front]
        self.mask_walking_back = [pygame.mask.from_surface(img) for img in self.img_walking_back]
        self.mask_walking_left = [pygame.mask.from_surface(img) for img in self.img_walking_left]
        self.mask_walking_right = [pygame.mask.from_surface(img) for img in self.img_walking_right]

        self.mask_gun_front = [pygame.mask.from_surface(img) for img in self.gun_front]
        self.mask_gun_back = [pygame.mask.from_surface(img) for img in self.gun_back]
        self.mask_gun_left = [pygame.mask.from_surface(img) for img in self.gun_left]
        self.mask_gun_right = [pygame.mask.from_surface(img) for img in self.gun_right]
        
        # Initial state
        self.state = "idle"
        self.facing = "facing"   
        self.gun_out = False
        self.image = self.img_facing
        self.mask = self.mask_facing
        self.rect = self.image.get_rect(center=STARTING_POSITION)

        self.walk_index = 0
        self.sprint = False
        self.move_distance = MOVE_DISTANCE

        self.velocity_x = 0
        self.velocity_y = 0

        self.HP = HEALTH
        self.damage = ATTACK
        self.last_hit_time = 0
        self.flash_timer = None  
        from collections import Counter
        self.inventory = Counter() 


    def update_sprite(self):
        if self.gun_out:
            if self.state == "idle":
                if self.facing == "facing":
                    self.image = self.gun_front[0]
                    self.mask = self.mask_gun_front[0]
                elif self.facing == "back":
                    self.image = self.gun_back[0]
                    self.mask = self.mask_gun_back[0]
                elif self.facing == "left":
                    self.image = self.gun_left[0]
                    self.mask = self.mask_gun_left[0]
                elif self.facing == "right":
                    self.image = self.gun_right[0]
                    self.mask = self.mask_gun_right[0]
            elif self.state == "walking":
                if self.facing == "facing":
                    idx = self.walk_index % len(self.gun_front)
                    self.image = self.gun_front[idx]
                    self.mask = self.mask_gun_front[idx]
                elif self.facing == "back":
                    idx = self.walk_index % len(self.gun_back)
                    self.image = self.gun_back[idx]
                    self.mask = self.mask_gun_back[idx]
                elif self.facing == "left":
                    idx = self.walk_index % len(self.gun_left)
                    self.image = self.gun_left[idx]
                    self.mask = self.mask_gun_left[idx]
                elif self.facing == "right":
                    idx = self.walk_index % len(self.gun_right)
                    self.image = self.gun_right[idx]
                    self.mask = self.mask_gun_right[idx]

        else:
            if self.state == "idle":
                if self.facing == "facing":
                    self.image = self.img_facing
                    self.mask = self.mask_facing
                elif self.facing == "back":
                    self.image = self.img_back
                    self.mask = self.mask_back
                elif self.facing == "left":
                    self.image = self.img_left
                    self.mask = self.mask_left
                elif self.facing == "right":
                    self.image = self.img_right
                    self.mask = self.mask_right
            elif self.state == "walking":
                if self.facing == "facing":
                    self.image = self.img_walking_front[self.walk_index % len(self.img_walking_front)]
                    self.mask = self.mask_walking_front[self.walk_index % len(self.img_walking_front)]
                elif self.facing == "back":
                    self.image = self.img_walking_back[self.walk_index % len(self.img_walking_back)]
                    self.mask = self.mask_walking_back[self.walk_index % len(self.img_walking_back)]
                elif self.facing == "left":
                    self.image = self.img_walking_left[self.walk_index % len(self.img_walking_left)]
                    self.mask = self.mask_walking_left[self.walk_index % len(self.img_walking_left)]
                elif self.facing == "right":
                    self.image = self.img_walking_right[self.walk_index % len(self.img_walking_right)]
                    self.mask = self.mask_walking_right[self.walk_index % len(self.img_walking_right)]
   
    def update(self):
        # handle flash reset
        if self.flash_timer and pygame.time.get_ticks() > self.flash_timer:
            self.flash_timer = None
            self.update_sprite()

    def flash_red(self):
        tinted = self.image.copy()
        red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 120))
        tinted.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = tinted
        self.flash_timer = pygame.time.get_ticks() + 200  # 200 ms
    
    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > 500:  # cooldown
            self.HP -= amount
            if self.HP < 0:
                self.HP = 0
                self.alive = False
            self.flash_red()
            self.last_hit_time = now
    
    def draw_health_bar(self, screen):
        bar_x = self.rect.centerx - 40
        bar_y = self.rect.top - 15
        bar_width = 80
        bar_height = 8
        health_ratio = max(self.HP / HEALTH, 0)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255 * (1 - health_ratio), 255 * health_ratio, 0),
                         (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)


    def attempt_move(self, dx, dy, current_bg, zombies_by_bg, transition_func, edge_check):
        # update facing/state
        if dx < 0: self.facing = "left"
        elif dx > 0: self.facing = "right"
        elif dy < 0: self.facing = "back"
        elif dy > 0: self.facing = "facing"

        self.state = "walking"
        self.walk_index += 1
        self.update_sprite()
        self.state = "idle"

        new_rect = self.rect.move(dx, dy)

        # border check
        if any(new_rect.colliderect(border) for border in current_bg.get_borders()):
            self.velocity_x = 0
            self.velocity_y = 0
            return

        # zombie collision check
        collision = False
        for (bg_surface, label), horde in zombies_by_bg.items():
            if bg_surface == current_bg.check_bg():
                for zombie in horde:
                    offset = (zombie.rect.x - new_rect.x, zombie.rect.y - new_rect.y)
                    if self.mask.overlap(zombie.mask, offset):
                        collision = True
                        break
            if collision:
                break

        if collision:
            self.velocity_x = 0
            self.velocity_y = 0
            return

        # apply movement
        self.rect = new_rect
        self.velocity_x = dx
        self.velocity_y = dy

        # edge transition or stop
        if edge_check(self.rect, self.image):
            if transition_func():
                # reposition to opposite edge
                if dx < 0: self.rect.x = 800 + self.image.get_width()/2
                elif dx > 0: self.rect.x = -self.image.get_width()/2
                elif dy < 0: self.rect.y = 600 + self.image.get_height()/2
                elif dy > 0: self.rect.y = -self.image.get_height()/2
            else:
                # clamp at half width/height
                if dx < 0: self.rect.left = -self.image.get_width()/2
                elif dx > 0: self.rect.right = 800 + self.image.get_width()/2
                elif dy < 0: self.rect.top = -self.image.get_height()/2
                elif dy > 0: self.rect.bottom = 600 + self.image.get_height()/2
                self.velocity_x = 0
                self.velocity_y = 0


    def move_up(self, current_bg, zombies_by_bg):
        self.attempt_move(0, -self.move_distance, current_bg, zombies_by_bg,
                        current_bg.trans_U,
                        lambda rect, img: rect.top < -img.get_height()/2)

    def move_down(self, current_bg, zombies_by_bg):
        self.attempt_move(0, self.move_distance, current_bg, zombies_by_bg,
                        current_bg.trans_D,
                        lambda rect, img: rect.bottom > 600 + img.get_height()/2)

    def move_left(self, current_bg, zombies_by_bg):
        self.attempt_move(-self.move_distance, 0, current_bg, zombies_by_bg,
                        current_bg.trans_L,
                        lambda rect, img: rect.left < -img.get_width()/2)

    def move_right(self, current_bg, zombies_by_bg):
        self.attempt_move(self.move_distance, 0, current_bg, zombies_by_bg,
                        current_bg.trans_R,
                        lambda rect, img: rect.right > 800 + img.get_width()/2)


    def go_to_start(self):
        self.rect.center = STARTING_POSITION
        self.facing = "facing"
        self.update_sprite()

    def sprinting(self):
        if self.sprint == True:
            self.move_distance = MOVE_DISTANCE * 3
        else: 
            self.move_distance = MOVE_DISTANCE


    def gun(self):
        if self.gun_out:
            self.gun_out = False
            self.update_sprite()
        else:
            self.gun_out = True 
            self.update_sprite()


    def shoot(self, bullet_group):
        if self.gun_out:
            # muzzle position depends on facing
            if self.facing == "facing":   # front
                x = self.rect.centerx
                y = self.rect.bottom - 20
            elif self.facing == "back":
                x = self.rect.centerx
                y = self.rect.top + 20
            elif self.facing == "left":
                x = self.rect.left + 20
                y = self.rect.centery
            elif self.facing == "right":
                x = self.rect.right - 20
                y = self.rect.centery

            from bullet import Bullet
            bullet = Bullet(x, y, self.facing)
            bullet_group.add(bullet)

    def pickup(self, zombies_by_bg, BG, game_status=None):
        if not self.gun_out:  # only allowed when gun is put away
            for (bg_surface, label), horde in zombies_by_bg.items():
                if bg_surface == BG.check_bg():
                    for zombie in horde[:]:  # iterate over copy
                        if zombie.state == "dead" and self.rect.colliderect(zombie.rect):
                            # add to daily inventory
                            self.inventory["Zombie Remains"] += 1
                            # add to lifetime totals
                            if game_status:
                                game_status.add_item("Zombie Remains")
                            # remove remains from game
                            horde.remove(zombie)
                            zombie.kill()
                            print("Picked up remains! Inventory:", self.inventory)


    def draw_inventory(self, screen):
        font = pygame.font.SysFont(None, 24)
        x = 10
        y = screen.get_height() - 150  # bottom-left corner

        title = font.render("Inventory:", True, (255, 255, 255))
        screen.blit(title, (x, y))
        y += 25

        # Only show items from the player's daily inventory
        for item, count in self.inventory.items():
            text = font.render(f"- {item}: {count}", True, (200, 200, 200))
            screen.blit(text, (x, y))
            y += 20





