# game_state.py
import json
import time
from character import PlayerCharacter
from simulation import WorldSimulation

class GameState:
    """
    Encapsulates the overall game state including the player and the simulation world.
    Provides methods to update, save, and load the state.
    """
    def __init__(self, player=None, world=None):
        self.player = player  # Instance of PlayerCharacter (for Character Mode)
        self.world = world    # Instance of WorldSimulation (for Simulation Mode)
        self.last_update = time.time()

    def update(self):
        """
        Update game state if needed.
        For simulation mode, trigger a world update (one tick).
        """
        if self.world:
            self.world.run_simulation(ticks=1, display_results=False)
        self.last_update = time.time()

    def to_dict(self):
        """Convert game state to a dictionary for saving."""
        return {
            "player": self.player.to_dict() if self.player else None,
            "world": self.world.to_dict() if self.world else None,
            "last_update": self.last_update
        }

    @classmethod
    def from_dict(cls, data):
        """Recreate game state from dictionary data."""
        from character import PlayerCharacter  # Ensure proper imports
        from simulation import WorldSimulation
        
        player = PlayerCharacter.from_dict(data["player"]) if data.get("player") else None
        world = WorldSimulation.from_dict(data["world"]) if data.get("world") else None
        state = cls(player, world)
        state.last_update = data.get("last_update", time.time())
        return state

    def save(self, filename):
        """Save the game state to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return f"Game state saved to {filename}"
        except Exception as e:
            return f"Error saving game state: {str(e)}"

    @classmethod
    def load(cls, filename):
        """Load the game state from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return cls.from_dict(data), "Game state loaded successfully"
        except Exception as e:
            return None, f"Error loading game state: {str(e)}"
