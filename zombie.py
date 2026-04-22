import pygame, random, time, math
from collections import deque

HEALTH = 30
ATTACK = 10
TILE_SIZE = 32
GRID_WIDTH = 800 // TILE_SIZE
GRID_HEIGHT = 600 // TILE_SIZE
CHASE_RADIUS = 200  # pixels

def to_grid(pos):
    return pos[0] // TILE_SIZE, pos[1] // TILE_SIZE

def to_pixels(grid_pos):
    return grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE

def bfs_path(start, goal, grid):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if grid[ny][nx] == 0 and (nx, ny) not in came_from:
                    queue.append((nx, ny))
                    came_from[(nx, ny)] = current
    # reconstruct path
    path = []
    current = goal
    while current and current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

class Zombie(pygame.sprite.Sprite):
    def __init__(self, spawn_bg):
        super().__init__()
        # idle images
        self.img_front = pygame.image.load("zombie_img/zombie 1.1 A.png").convert_alpha()
        self.img_back = pygame.image.load("zombie_img/zombie_Back1.png").convert_alpha()
        self.img_left = pygame.image.load("zombie_img/zombie_L1.png").convert_alpha()
        self.img_right = pygame.image.load("zombie_img/zombie_R1.png").convert_alpha()

        # walking animations
        self.img_walking_front = [
            pygame.image.load("zombie_img/zombie 1.2 A.png").convert_alpha(),
            self.img_front
        ]
        self.img_walking_back = [
            pygame.image.load("zombie_img/zombie_Back2.png").convert_alpha(),
            self.img_back
        ]
        self.img_walking_left = [pygame.image.load("zombie_img/zombie_L2.png").convert_alpha(), self.img_left]
        self.img_walking_right = [pygame.image.load("zombie_img/zombie_R2.png").convert_alpha(), self.img_right]

        # scale everything
        self.img_front = pygame.transform.scale(self.img_front, (150, 120))
        self.img_back = pygame.transform.scale(self.img_back, (150, 120))
        self.img_left = pygame.transform.scale(self.img_left, (150, 120))
        self.img_right = pygame.transform.scale(self.img_right, (150, 120))

        self.img_walking_front = [pygame.transform.scale(img, (150, 120)) for img in self.img_walking_front]
        self.img_walking_back = [pygame.transform.scale(img, (150, 120)) for img in self.img_walking_back]
        self.img_walking_left = [pygame.transform.scale(img, (150, 120)) for img in self.img_walking_left]
        self.img_walking_right = [pygame.transform.scale(img, (150, 120)) for img in self.img_walking_right]
        
        #mask
        self.mask_front = pygame.mask.from_surface(self.img_front)
        self.mask_back = pygame.mask.from_surface(self.img_back)
        self.mask_left = pygame.mask.from_surface(self.img_left)
        self.mask_right = pygame.mask.from_surface(self.img_right)

        self.mask_walking_front = [pygame.mask.from_surface(img) for img in self.img_walking_front]
        self.mask_walking_back = [pygame.mask.from_surface(img) for img in self.img_walking_back]
        self.mask_walking_left = [pygame.mask.from_surface(img) for img in self.img_walking_left]
        self.mask_walking_right = [pygame.mask.from_surface(img) for img in self.img_walking_right]
        
        #zombie remain
        self.remains_img = pygame.image.load("zombie_img/zombies remain.png").convert_alpha()
        self.remains_img = pygame.transform.scale(self.remains_img, (150, 120))


        rand_x = random.randint(50, 750)
        rand_y = random.randint(50, 550)
        self.rect = self.img_front.get_rect(center=(rand_x, rand_y))
        self.velocity_x = 0
        self.velocity_y = 0

        # background tracking
        self.spawn_bg = spawn_bg
        self.active = True

        # wandering logic
        self.current_direction = None
        self.next_change_time = time.time() + random.uniform(1, 2)

        # shuffle speed variation
        self.move_distance = random.randint(5, 10)

        # random delay before first movement
        self.start_delay = time.time() + random.uniform(0.5, 3.0)

        # random initial facing direction
        self.facing = random.choice(["front", "back", "left", "right"])
        self.state = "idle"
        self.walk_index = 0

        # set initial sprite image based on facing
        if self.facing == "front":
            self.image = self.img_front
        elif self.facing == "back":
            self.image = self.img_back
        elif self.facing == "left":
            self.image = self.img_left
        elif self.facing == "right":
            self.image = self.img_right

        # set initial mask to match facing
        if self.facing == "front":
            self.mask = self.mask_front
        elif self.facing == "back":
            self.mask = self.mask_back
        elif self.facing == "left":
            self.mask = self.mask_left
        elif self.facing == "right":
            self.mask = self.mask_right
        
        self.HP = HEALTH
        self.damage = ATTACK


    def update_sprite(self):
        if self.state == "idle":
            if self.facing == "front":
                self.image = self.img_front
                self.mask = self.mask_front
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
            if self.facing == "front":
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
        # red damage
        tinted = self.image.copy()
        red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 120))
        tinted.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = tinted
        self.flash_timer = pygame.time.get_ticks() + 200  # 200 ms

    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if not hasattr(self, "last_hit_time") or now - self.last_hit_time > 500:
            self.HP -= amount
            if self.HP < 0:
                self.HP = 0
            self.flash_red()
            self.last_hit_time = now

            if self.HP == 0:
                self.die()

    def die(self):
        # swap to remains image
        self.image = self.remains_img
        self.mask = pygame.mask.from_surface(self.remains_img)
        self.state = "dead"
        self.velocity_x = 0
        self.velocity_y = 0
        # keep rect in place



    def random_walk(self, current_bg):
        # only active in spawn background
        if current_bg.check_bg() != self.spawn_bg:
            self.active = False
            self.state = "idle"
            self.update_sprite()
            return
        else:
            self.active = True

        # wait until start_delay expires
        if time.time() < self.start_delay:
            self.state = "idle"
            self.update_sprite()
            return

        # time to pick a new direction
        if time.time() >= self.next_change_time:
            # sometimes pick idle, sometimes a direction
            self.current_direction = random.choice(["up", "down", "left", "right", None])
            
            # random pause length
            if self.current_direction is None:
                self.next_change_time = time.time() + random.uniform(2, 4)  # idle pause 2–4s
            else:
                self.next_change_time = time.time() + random.uniform(1, 2)  # walking 1–2s

        # move if direction is set
        if self.current_direction:
            self.walk_index += 1
            self.state = "walking"

            if self.current_direction == "up":
                self.facing = "back"
                if self.rect.top - self.move_distance > 0:
                    self.rect.y -= self.move_distance
                    self.velocity_y = -self.move_distance
                    self.velocity_x = 0
                else:
                    self.current_direction = "down"

            elif self.current_direction == "down":
                self.facing = "front"
                if self.rect.bottom + self.move_distance < 600:
                    self.rect.y += self.move_distance
                    self.velocity_y = self.move_distance
                    self.velocity_x = 0
                else:
                    self.current_direction = "up"

            elif self.current_direction == "left":
                self.facing = "left"
                if self.rect.left - self.move_distance > 0:
                    self.rect.x -= self.move_distance
                    self.velocity_x = -self.move_distance
                    self.velocity_y = 0
                else:
                    self.current_direction = "right"

            elif self.current_direction == "right":
                self.facing = "right"
                if self.rect.right + self.move_distance < 800:
                    self.rect.x += self.move_distance
                    self.velocity_x = self.move_distance
                    self.velocity_y = 0
                else:
                    self.current_direction = "left"


        else:
            self.state = "idle"
            self.velocity_x = 0
            self.velocity_y = 0


        self.update_sprite()

    def draw_health_bar(self, screen):
        # only draw if zombie is alive
        if self.state != "dead" and self.HP > 0:
            bar_x = self.rect.centerx - 20
            bar_y = self.rect.top - 10
            bar_width = 40
            bar_height = 5
            health_ratio = max(self.HP / HEALTH, 0)

            # background
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # health fill
            pygame.draw.rect(screen, (255 * (1 - health_ratio), 255 * health_ratio, 0),
                            (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
            # border
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

    def move_towards(self, target_px):
        tx, ty = target_px
        dx = tx - self.rect.centerx
        dy = ty - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.rect.x += int(self.move_distance * dx / dist)
            self.rect.y += int(self.move_distance * dy / dist)
            # update facing for animation
            if abs(dx) > abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "front" if dy > 0 else "back"
            self.state = "walking"
            self.walk_index += 1
            self.update_sprite()

    def chase(self, player, grid):
        zombie_grid = to_grid(self.rect.center)
        player_grid = to_grid(player.rect.center)
        path = bfs_path(zombie_grid, player_grid, grid)
        if len(path) > 1:
            next_step = path[1]
            target_px = to_pixels(next_step)
            self.move_towards(target_px)

    def update_ai(self, player, current_bg, grid):
        if self.state == "dead":
            return
        # only active in spawn background
        if current_bg.check_bg() != self.spawn_bg:
            self.active = False
            self.state = "idle"
            self.update_sprite()
            return
        else:
            self.active = True

        # distance check
        zx, zy = self.rect.center
        px, py = player.rect.center
        dist = math.hypot(zx - px, zy - py)

        if dist <= CHASE_RADIUS:
            self.chase(player, grid)
        else:
            self.random_walk(current_bg)