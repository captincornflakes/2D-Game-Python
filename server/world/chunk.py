class Chunk:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiles = [[None for _ in range(32)] for _ in range(32)]
        self.loaded = False

    def load(self):
        # Load chunk data from a file or initialize if not exists
        self.loaded = True

    def save(self):
        # Save chunk data to a file
        pass

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile

    def is_loaded(self):
        return self.loaded