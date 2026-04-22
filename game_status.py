import csv
import time

class GameStatus:
    gameplay_number = 0 

    def __init__(self):
        from collections import Counter
        self.total_inventory = Counter()
        self.total_pages = 0
        self.score = 0

        # New counters
        self.zombies_killed = 0
        self.bullets_fired = 0

        GameStatus.gameplay_number += 1
        self.current_gameplay = GameStatus.gameplay_number

        self.csv_file = "game_data.csv"

        try:
            with open(self.csv_file, "r") as f:
                pass  # file exists, do nothing
        except FileNotFoundError:
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["elapsed_seconds", "gameplay_number",
                                 "zombies_killed", "trash_collected",
                                 "leftover_trash", "alive_zombies",
                                 "bullets_fired", "score"])

        # Timing
        self.last_log_time = time.time()
        self.elapsed_seconds = 0   #start at 0

    def add_item(self, item, count=1):
        self.total_inventory[item] += count

    def add_page(self):
        self.total_pages += 1

    def reset_day_inventory(self, player):
        player.inventory.clear()

    def calculate_score(self, player):
        trash_points = player.inventory.get("Trash", 0) * 10
        remains_points = player.inventory.get("Zombie Remains", 0) * 50
        self.score = trash_points + remains_points
        return self.score

    def log_data(self, scoreboard, trash_items, zombies_by_bg):
        #Log data every 5 seconds
        now = time.time()
        if now - self.last_log_time >= 5:
            self.last_log_time = now
            self.elapsed_seconds += 5

            # Count leftovers
            leftover_trash = sum(1 for t in trash_items if not t.collected)
            alive_zombies = sum(1 for (bg_surface, label), horde in zombies_by_bg.items()
                                for z in horde if z.state != "dead")
           
            trash_points = scoreboard.trash_collected * 10
            zombie_points = self.zombies_killed * 50
            self.score = trash_points + zombie_points

            with open(self.csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([self.elapsed_seconds, self.current_gameplay,
                                 self.zombies_killed, scoreboard.trash_collected,
                                 leftover_trash, alive_zombies,
                                 self.bullets_fired, self.score])