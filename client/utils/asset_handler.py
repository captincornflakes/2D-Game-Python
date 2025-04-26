import os
import json
import pygame  # Ensure pygame is imported for asset loading

class AssetHandler:
    def __init__(self, config):
        """Initialize the AssetHandler by loading assets and tile metadata."""
        # Use the provided configuration
        self.config = config
        self.assets_folder = self.config.get("assets_folder", "assets/default")
        self.tiles_file = os.path.join(self.assets_folder, "tiles.json")

        # Asset storage
        self.assets = {}
        self.tiles = {}

        # Load assets and tiles
        self._load_assets()
        self._load_tiles()

    def _load_assets(self):
        """Load all PNG files from the assets folder."""
        if not os.path.exists(self.assets_folder):
            raise FileNotFoundError(f"Assets folder not found: {self.assets_folder}")

        for file_name in os.listdir(self.assets_folder):
            if file_name.endswith(".png"):
                asset_id = os.path.splitext(file_name)[0]  # Use the file name (without extension) as the asset ID
                file_path = os.path.join(self.assets_folder, file_name)
                self.assets[asset_id] = pygame.image.load(file_path)
                print(f"Loaded asset: {asset_id} from {file_path}")

    def _load_tiles(self):
        """Load tile metadata from tiles.json."""
        if not os.path.exists(self.tiles_file):
            raise FileNotFoundError(f"Tiles file not found: {self.tiles_file}")

        with open(self.tiles_file, "r") as file:
            self.tiles = json.load(file)
            print(f"Loaded tiles metadata from {self.tiles_file}")

    def get_asset(self, asset_id):
        """Retrieve a loaded asset by its ID."""
        return self.assets.get(asset_id, None)

    def get_tile_metadata(self, tile_name):
        """Retrieve metadata for a specific tile."""
        return self.tiles.get(tile_name, None)
