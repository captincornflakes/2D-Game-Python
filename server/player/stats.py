class PlayerStats:
    def __init__(self):
        self.health = 100
        self.stamina = 100
        self.hunger = 100
        self.difficulty = 'normal'
        self.game_time = 0  # in seconds
        self.inventory = {}

    def update_health(self, amount):
        self.health = max(0, min(100, self.health + amount))

    def update_stamina(self, amount):
        self.stamina = max(0, min(100, self.stamina + amount))

    def update_hunger(self, amount):
        self.hunger = max(0, min(100, self.hunger + amount))

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def increment_game_time(self, seconds):
        self.game_time += seconds

    def add_item_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item_from_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                del self.inventory[item]