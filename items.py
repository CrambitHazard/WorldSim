# items.py
import random

class Item:
    """
    Represents an item that can be held in an inventory or equipped.
    """
    def __init__(self, name, description, value, item_type, bonuses=None):
        self.name = name
        self.description = description
        self.value = value  # Gold value
        self.type = item_type  # e.g., 'weapon', 'armor', 'accessory'
        self.bonuses = bonuses if bonuses else {}  # Dict with stat bonuses

    def to_dict(self):
        """Convert the item to a dictionary for saving."""
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "type": self.type,
            "bonuses": self.bonuses
        }

    @classmethod
    def from_dict(cls, data):
        """Create an item from saved dictionary data."""
        return cls(
            data["name"],
            data["description"],
            data["value"],
            data["type"],
            data.get("bonuses", {})
        )

def generate_random_item(player_level):
    """
    Generate a random item appropriate for the given player level.
    The item's quality, value, and bonus effects scale with the level.
    """
    # Possible item types and names
    item_types = ["weapon", "armor", "accessory"]
    weapon_names = ["Sword", "Axe", "Dagger", "Mace", "Staff"]
    armor_names = ["Chainmail", "Plate Armor", "Leather Armor", "Robe"]
    accessory_names = ["Ring", "Amulet", "Bracelet", "Talisman"]

    item_type = random.choice(item_types)
    if item_type == "weapon":
        name = random.choice(weapon_names)
    elif item_type == "armor":
        name = random.choice(armor_names)
    else:
        name = random.choice(accessory_names)

    # Quality prefix based on player level
    quality_prefixes = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
    if player_level < 5:
        quality = quality_prefixes[0]
    elif player_level < 10:
        quality = quality_prefixes[1]
    elif player_level < 15:
        quality = quality_prefixes[2]
    elif player_level < 20:
        quality = quality_prefixes[3]
    else:
        quality = quality_prefixes[4]

    full_name = f"{quality} {name}"
    description = f"A {quality.lower()} {name.lower()} suitable for adventurers around level {player_level}."
    value = random.randint(10, 20) * player_level

    # Random bonus: boost one stat slightly
    stat_options = ["strength", "agility", "intelligence", "constitution", "wisdom", "perception", "charisma"]
    bonus_stat = random.choice(stat_options)
    bonus_value = random.randint(1, 3)
    bonuses = {bonus_stat: bonus_value}

    return Item(full_name, description, value, item_type, bonuses)
