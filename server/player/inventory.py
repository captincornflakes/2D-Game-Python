class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity=1):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items:
            if self.items[item_name] > quantity:
                self.items[item_name] -= quantity
            elif self.items[item_name] == quantity:
                del self.items[item_name]

    def get_items(self):
        return self.items

    def has_item(self, item_name):
        return item_name in self.items and self.items[item_name] > 0

    def clear_inventory(self):
        self.items.clear()