import pygame
import time
import random

from menu import Menu
import data_stats
from game_status import GameStatus
from scoreboard import Scoreboard
from player import Player, HEALTH
from zombie import Zombie
from bullet import Bullet
from background import Background
from object import Page, Trash

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pick it up in process")
clock = pygame.time.Clock()

game_status = GameStatus()
player = Player()
scoreboard = Scoreboard()
BG = Background()

bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle(player)

zombies_by_bg = {}
spawned_zones = set()

spawn_counts = {
    BG.crossroad_bg: 3,
    BG.road_x1_bg: 2,
    BG.road_x2_bg: 2,
    BG.road_y1_bg: 3,
    BG.road_y2_bg: 3,
    BG.sand_bg1: 5,
    BG.sand_bg2: 4,
    BG.sand_bg3: 4,
    BG.sand_bg4: 5,
}


last_spawn_time = {}
SPAWN_COOLDOWN = 180000

debug_mode = False
game_is_on = True
game_over = False
fade_alpha = 0
sleep_popup = False


GRID_WIDTH = 800 // 32
GRID_HEIGHT = 600 // 32
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Menu loop
menu = Menu(screen)

while menu.active:
    for event in pygame.event.get():
        menu.handle_event_main(event)
    menu.draw_main()
    time.sleep(0.1)

# If Stats button clicked
if menu.show_stats:
    data_stats.show_graphs(screen)
    menu.active = True
    menu.show_stats = False

page = None
trash_num = random.randint(30, 80)
trash_items = [Trash(BG) for _ in range(trash_num)] 
if menu.story_mode:
    page = Page(BG)
    page_spawn_day = scoreboard.day  # assume your scoreboard tracks day count



# If Start was clicked, run the game loop
if menu.start_game:
    while game_is_on:
        time.sleep(0.1)
        screen.blit(BG.image, (0, 0))

        #Game control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.paused = True

            if event.type == pygame.KEYDOWN:
                if scoreboard.win_message_screen:
                    if event.key == pygame.K_SPACE:
                        scoreboard.win_message_screen = False
                        scoreboard.pending_win = True 
                        game_over = True
                        scoreboard.game_won = True
                        

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        if scoreboard.pending_win:
                            # First SPACE press after win → just acknowledge win screen
                            scoreboard.pending_win = False
                            # Keep YOU WIN screen 
                        elif scoreboard.game_won:
                            # After winning go back to menu 
                            game_is_on = False
                            menu.active = True
                            menu.start_game = False
                            # game is off, no menu aaaaaaaaaaaaaa 
                        else:
                            # Normal Game Over restart
                            player.go_to_start()
                            player.HP = HEALTH
                            player.alive = True
                            BG.background = BG.home_bg
                            BG.update_img()
                            zombies_by_bg.clear()
                            spawned_zones.clear()
                            scoreboard.reset()
                            trash_items.clear()
                            trash_num = random.randint(30, 80)
                            trash_items = [Trash(BG) for _ in range(trash_num)]
                            fade_alpha = 0
                            game_over = False
                            player.inventory.clear()
                            last_spawn_time.clear()
                            game_status.total_inventory.clear() 
                            game_status.score = 0
                            if menu.story_mode:
                                page = Page(BG)
                                page_spawn_day = scoreboard.day
                            else:
                                page = None

                elif sleep_popup:
                    if event.key == pygame.K_y:
                        player.go_to_start()
                        player.HP = HEALTH
                        BG.background = BG.home_bg
                        BG.update_img()
                        zombies_by_bg.clear()
                        spawned_zones.clear()
                        scoreboard.increase_day()
                        
                        
                        if scoreboard.pending_win and scoreboard.pages_collected >= 7:
                            scoreboard.win_message_screen = True
                        last_spawn_time.clear()

                        # Calculate infection only once per new day
                        unclean_trash = sum(1 for t in trash_items if not t.collected)
                        unclean_remains = sum(1 for (bg_surface, label), horde in zombies_by_bg.items()
                                            for z in horde if z.state == "dead")
                        alive_zombies = sum(1 for (bg_surface, label), horde in zombies_by_bg.items()
                                            for z in horde if z.state != "dead")

                        scoreboard.increase_infection(unclean_trash * 0.5 + unclean_remains * 1.0 + alive_zombies * 0.2)
                        
                        trash_items.clear() 
                        trash_num = random.randint(30, 80)
                        trash_items = [Trash(BG) for _ in range(trash_num)]
                        # Check game over condition
                        if not scoreboard.game_won and scoreboard.infection_rate >= 100:
                            game_over = True

                        sleep_popup = False  
                        
                        #new day inventory
                        game_status.reset_day_inventory(player)


                        # Spawn a new page only once per new day
                        if menu.story_mode and page_spawn_day != scoreboard.day:
                            page = Page(BG)
                            page_spawn_day = scoreboard.day
                    if event.key == pygame.K_n:
                        sleep_popup = False
                        player.go_to_start()
                    

                else:
                    if event.key == pygame.K_g:
                        player.gun()
                    if event.key == pygame.K_SPACE:
                        player.shoot(bullet_group)
                        game_status.bullets_fired += 1
                    if event.key == pygame.K_TAB:
                        debug_mode = not debug_mode
        

        if not game_over and not sleep_popup:
            bullet_group.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move_up(BG, zombies_by_bg)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move_down(BG, zombies_by_bg)
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.move_left(BG, zombies_by_bg)
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.move_right(BG, zombies_by_bg)
            if keys[pygame.K_e]:
                # pickup zombie remains
                player.pickup(zombies_by_bg, BG, game_status)

                # pickup trash only if no gun out
                if not player.gun_out:
                    for trash in trash_items:
                        if not trash.collected and BG.check_bg() == trash.spawn_bg and player.rect.colliderect(trash.rect):
                            trash.collect()
                            scoreboard.add_trash()
                            player.inventory["Trash"] += 1
                            game_status.add_item("Trash")
                            print("Trash collected!")
                
                scoreboard.calculate_score(player)


            #sprint go brrrrrrr     
            player.sprint = keys[pygame.K_LSHIFT]
            player.sprinting()

            #Collision
            for transition in BG.get_special_transitions():
                if player.rect.colliderect(transition["rect"]):
                    if transition["label"] == "house_door":
                        if BG.check_bg() == BG.home_bg and player.velocity_y > 0:
                            BG.background = transition["target_bg"]
                            BG.update_img()
                            player.rect.center = transition["target_pos"]
                        elif BG.check_bg() == BG.road_house_bg and player.velocity_y < 0:
                            BG.background = transition["target_bg"]
                            BG.update_img()
                            player.rect.center = transition["target_pos"]

            #check bed zone 
            if BG.check_bg() == BG.home_bg:
                for label, zone in BG.get_zones():
                    if label == "bed_zone" and player.rect.colliderect(zone):
                        sleep_popup = True

            current_bg_surface = BG.check_bg()
            now = pygame.time.get_ticks()

            #check spawn
            for label, zone in BG.get_zones():
                if label == "bed_zone":
                    continue
                zone_key = (current_bg_surface, label)
                if player.rect.colliderect(zone):
                    if current_bg_surface not in last_spawn_time or now - last_spawn_time[current_bg_surface] > SPAWN_COOLDOWN:
                        base_count = spawn_counts.get(current_bg_surface, 3)

                        # Scale with infection rate: +1 zombie every 20% infection
                        extra = int(scoreboard.infection_rate // 20)

                        count = base_count + extra

                        zombies_by_bg[zone_key] = [Zombie(current_bg_surface) for _ in range(count)]

                        spawned_zones.add(zone_key)
                        last_spawn_time[current_bg_surface] = now

            #Zombie AI
            for (bg_surface, label), horde in zombies_by_bg.items():
                if bg_surface == BG.check_bg():
                    for zombie in horde:
                        zombie.update_ai(player, BG, grid)  # grid = walkable map


            for (bg_surface, label), horde in zombies_by_bg.items():
                if bg_surface == BG.check_bg():
                    for zombie in horde:
                        for bullet in bullet_group:
                            if zombie.rect.colliderect(bullet.rect) and zombie.state != "dead":
                                zombie.take_damage(player.damage)
                                bullet.kill()
                                if zombie.state == "dead":
                                    game_status.zombies_killed += 1
                        if zombie.state != "dead" and player.rect.colliderect(zombie.rect):
                            offset_player = (zombie.rect.x - player.rect.x, zombie.rect.y - player.rect.y)
                            if player.mask.overlap(zombie.mask, offset_player):
                                player.velocity_x = 0
                                player.velocity_y = 0
                                zombie.velocity_x = 0
                                zombie.velocity_y = 0
                                player.take_damage(zombie.damage)

                                if debug_mode:
                                    overlay_p = pygame.Surface((player.rect.width, player.rect.height), pygame.SRCALPHA)
                                    overlay_p.fill((255, 0, 0, 100))
                                    screen.blit(overlay_p, player.rect)

                                    overlay_z = pygame.Surface((zombie.rect.width, zombie.rect.height), pygame.SRCALPHA)
                                    overlay_z.fill((255, 0, 0, 100))
                                    screen.blit(overlay_z, zombie.rect)
           
            if player.HP <= 0 and not game_over:
                player.alive = False
                game_over = True
                scoreboard.pending_win = False


            # Check game over condition
            if scoreboard.infection_rate >= 100:
                game_over = True


            #draw
            all_sprites = [player]
            for (bg_surface, label), horde in zombies_by_bg.items():
                if bg_surface == BG.check_bg():
                    all_sprites += horde
            all_sprites.sort(key=lambda s: s.rect.bottom)

            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)
                if isinstance(sprite, Player):
                    sprite.draw_health_bar(screen)
                elif isinstance(sprite, Zombie):
                    sprite.draw_health_bar(screen)

            for bullet in bullet_group:
                screen.blit(bullet.image, bullet.rect)
            
            if page and not page.collected and BG.check_bg() == page.spawn_bg:
                screen.blit(page.image, page.rect)
                if page.collect(player):
                    scoreboard.add_page()
                    print("Page collected!")
                    if scoreboard.pages_collected >= 7:
                        scoreboard.pending_win = True
                        scoreboard.game_won = True
            
            for trash in trash_items:
                if not trash.collected and BG.check_bg() == trash.spawn_bg:
                    screen.blit(trash.image, trash.rect)
                    
            if scoreboard.win_message_screen:
                scoreboard.draw_win_message(screen)
            elif game_over:
                scoreboard.game_over(screen, fade_alpha, player, game_status)


            #DEBUG CHEAT
            if debug_mode:
                for label, zone in BG.get_zones():
                    overlay = pygame.Surface((zone.width, zone.height), pygame.SRCALPHA)
                    overlay.fill((255, 0, 0, 100))
                    screen.blit(overlay, (zone.x, zone.y))
                    font = pygame.font.SysFont(None, 20)
                    text = font.render(label, True, (255, 255, 255))
                    screen.blit(text, (zone.x, zone.y - 15))

                for transition in BG.get_special_transitions():
                    rect = transition["rect"]
                    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 255, 100))
                    screen.blit(overlay, (rect.x, rect.y))
                    font = pygame.font.SysFont(None, 20)
                    text = font.render(transition["label"], True, (255, 255, 255))
                    screen.blit(text, (rect.x, rect.y - 15))

                for border in BG.get_borders():
                    overlay = pygame.Surface((border.width, border.height), pygame.SRCALPHA)
                    overlay.fill((0, 255, 0, 100))
                    screen.blit(overlay, (border.x, border.y))

            player_group.update()
            scoreboard.draw(screen, story_mode=menu.story_mode)
            player.draw_inventory(screen)

        game_status.log_data(scoreboard, trash_items, zombies_by_bg)


        if game_over:
            scoreboard.game_over(screen, fade_alpha, player, game_status)

        elif sleep_popup:
            menu.draw_sleep_popup(screen)
       
        frozen_frame = screen.copy()       
        while menu.paused:
            for event in pygame.event.get():
                menu.handle_event_pause(event)
            menu.draw_pause(frozen_frame)
            time.sleep(0.1)


        pygame.display.flip()

pygame.quit()
