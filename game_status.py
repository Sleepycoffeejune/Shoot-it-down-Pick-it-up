from collections import Counter

class GameStatus:
    def __init__(self):
        # Tracks total collected items across all days
        self.total_inventory = Counter()
        self.total_pages = 0

    def add_item(self, item, count=1):
        self.total_inventory[item] += count

    def add_page(self):
        self.total_pages += 1

    def reset_day_inventory(self, player):
        """Clear player's daily inventory but keep totals here."""
        player.inventory.clear()

    def calculate_score(self, player):
        """Calculate score based on daily inventory."""
        trash_points = player.inventory.get("Trash", 0) * 10
        remains_points = player.inventory.get("Zombie Remains", 0) * 50
        self.score = trash_points + remains_points
        return self.score
