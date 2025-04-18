import os
import time
import random
import json
import sys

def clear_screen():
    """Clear the terminal screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')

def typewriter_effect(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def save_game(player, world=None, filename=None):
    """Save game state to a file."""
    if filename is None:
        filename = f"{player.name}_save.json"
    
    save_data = {
        "player": player.to_dict(),
        "world": world.to_dict() if world else None,
        "timestamp": time.time()
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        return f"Game saved successfully as {filename}"
    except Exception as e:
        return f"Error saving game: {str(e)}"

def load_game(filename):
    """Load game state from a file."""
    from character import PlayerCharacter
    from simulation import WorldSimulation
    
    try:
        with open(filename, 'r') as f:
            save_data = json.load(f)
        
        player = PlayerCharacter.from_dict(save_data["player"])
        
        world = None
        if save_data.get("world"):
            world = WorldSimulation.from_dict(save_data["world"])
        
        return player, world, "Game loaded successfully"
    except FileNotFoundError:
        return None, None, "Save file not found"
    except Exception as e:
        return None, None, f"Error loading game: {str(e)}"

def get_save_files():
    """Get a list of available save files."""
    return [f for f in os.listdir('.') if f.endswith('_save.json')]

def dice_roll(sides=6, num_dice=1):
    """Simulate rolling dice."""
    return sum(random.randint(1, sides) for _ in range(num_dice))

def probability_check(probability):
    """Check if a random probability succeeds."""
    return random.random() < probability

def format_bar(current, maximum, bar_length=20, fill_char='█', empty_char='░'):
    """Create a visual bar (for health, etc.)"""
    if maximum <= 0:
        return empty_char * bar_length
    
    fill = int(bar_length * (current / maximum))
    return fill_char * fill + empty_char * (bar_length - fill)

def wrap_text(text, width=80):
    """Wrap text to fit within a specific width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)
