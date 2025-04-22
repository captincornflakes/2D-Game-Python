def serialize_data(data):
    import json
    return json.dumps(data)

def deserialize_data(data):
    import json
    return json.loads(data)

def log_message(message):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(message)

def save_player_data(players):
    """Save player data to the players.json file."""
    print("Saving player data...")
    players.save_players()