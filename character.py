import random
import json
import os
from utils import clear_screen, typewriter_effect

class Character:
    """Base character class for both player characters and NPCs."""
    races = [
        "Human", "Dwarf", "Elf", "Demon", "Angel", 
        "Demigod", "Messiah", "Dragon", "Beastman", "Kaosborne"
    ]
    
    classes = [
        "Warrior", "Mage", "Ranger", "Cleric", "Rogue",
        "Paladin", "Warlock", "Bard", "Monk", "Berserker"
    ]
    
    @classmethod
    def get_race(cls):
        """Randomly select a race."""
        roll = random.randint(1, len(cls.races))
        return cls.races[roll - 1]
    
    @classmethod
    def get_class(cls):
        """Randomly select a character class."""
        roll = random.randint(1, len(cls.classes))
        return cls.classes[roll - 1]
    
    def __init__(self, name, race=None, character_class=None):
        """Initialize a new character with specified or random attributes."""
        self.name = name
        self.race = race or Character.get_race()
        self.character_class = character_class or Character.get_class()
        self.inventory = []
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.stats = Stats(self.race, self.character_class)
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.gold = 50
        self.quests = []
        
    def level_up(self):
        """Increase character level and update stats."""
        self.level += 1
        self.exp = self.exp - self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        
        # Increase stats based on character class
        if self.character_class in ["Warrior", "Berserker", "Paladin"]:
            self.stats.strength += 2
            self.stats.constitution += 2
            self.stats.intelligence += 1
        elif self.character_class in ["Mage", "Warlock"]:
            self.stats.intelligence += 3
            self.stats.wisdom += 2
            self.stats.strength += 0.5
        elif self.character_class in ["Ranger", "Rogue"]:
            self.stats.agility += 3
            self.stats.perception += 2
            self.stats.strength += 1
        elif self.character_class in ["Cleric", "Bard"]:
            self.stats.wisdom += 2
            self.stats.charisma += 2
            self.stats.intelligence += 1.5
        elif self.character_class == "Monk":
            self.stats.agility += 2
            self.stats.wisdom += 2
            self.stats.strength += 1.5
            
        # Update derived stats
        self.stats.update_derived_stats()
        
        return f"Congratulations! {self.name} is now level {self.level}!"
    
    def gain_exp(self, amount):
        """Add experience points and check for level up."""
        self.exp += amount
        message = f"{self.name} gained {amount} experience points."
        
        if self.exp >= self.exp_to_next_level:
            level_up_message = self.level_up()
            message += f"\n{level_up_message}"
            
        return message
    
    def add_to_inventory(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)
        return f"{item.name} added to inventory."
    
    def equip_item(self, item_name):
        """Equip an item from the inventory."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if hasattr(item, 'type'):
                    # Unequip current item in that slot if any
                    if self.equipment[item.type]:
                        old_item = self.equipment[item.type]
                        self.inventory.append(old_item)  # Return old item to inventory
                        
                    # Remove from inventory and add to equipment
                    self.inventory.remove(item)
                    self.equipment[item.type] = item
                    
                    # Apply item stats
                    self.stats.apply_equipment_bonuses()
                    
                    return f"{item.name} equipped."
                return f"{item.name} cannot be equipped."
        return f"{item_name} not found in inventory."
    
    def display_character_sheet(self):
        """Display detailed character information."""
        clear_screen()
        sheet = f"""
{'=' * 50}
{self.name} - Level {self.level} {self.race} {self.character_class}
{'-' * 50}
EXP: {self.exp}/{self.exp_to_next_level}
Gold: {self.gold}

ATTRIBUTES:
  Health: {self.stats.health}/{self.stats.max_health}
  Mana: {self.stats.mana}/{self.stats.max_mana}
  Strength: {self.stats.strength}
  Intelligence: {self.stats.intelligence}
  Wisdom: {self.stats.wisdom}
  Constitution: {self.stats.constitution}
  Agility: {self.stats.agility}
  Perception: {self.stats.perception}
  Charisma: {self.stats.charisma}

DERIVED STATS:
  Physical Attack: {self.stats.physical_attack}
  Magical Attack: {self.stats.magical_attack}
  Physical Defense: {self.stats.physical_defense}
  Magical Defense: {self.stats.magical_defense}
  Speed: {self.stats.speed}

EQUIPMENT:
  Weapon: {self.equipment['weapon'].name if self.equipment['weapon'] else 'None'}
  Armor: {self.equipment['armor'].name if self.equipment['armor'] else 'None'}
  Accessory: {self.equipment['accessory'].name if self.equipment['accessory'] else 'None'}

INVENTORY:
  {', '.join([item.name for item in self.inventory]) if self.inventory else 'Empty'}

ACTIVE QUESTS:
  {', '.join([quest.title for quest in self.quests]) if self.quests else 'None'}
{'=' * 50}
"""
        print(sheet)
        input("Press Enter to continue...")

    def to_dict(self):
        """Convert character to dictionary for saving."""
        return {
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "level": self.level,
            "exp": self.exp,
            "exp_to_next_level": self.exp_to_next_level,
            "gold": self.gold,
            "stats": self.stats.to_dict(),
            "inventory": [item.to_dict() for item in self.inventory],
            "equipment": {
                "weapon": self.equipment["weapon"].to_dict() if self.equipment["weapon"] else None,
                "armor": self.equipment["armor"].to_dict() if self.equipment["armor"] else None,
                "accessory": self.equipment["accessory"].to_dict() if self.equipment["accessory"] else None
            },
            "quests": [quest.to_dict() for quest in self.quests]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a character from dictionary data."""
        from items import Item  # Import here to avoid circular imports
        from quests import Quest # type: ignore
        
        character = cls(data["name"], data["race"], data["character_class"])
        character.level = data["level"]
        character.exp = data["exp"]
        character.exp_to_next_level = data["exp_to_next_level"]
        character.gold = data["gold"]
        character.stats = Stats.from_dict(data["stats"])
        
        # Load inventory
        character.inventory = [Item.from_dict(item_data) for item_data in data["inventory"]]
        
        # Load equipment
        for slot, item_data in data["equipment"].items():
            if item_data:
                character.equipment[slot] = Item.from_dict(item_data)
        
        # Load quests
        character.quests = [Quest.from_dict(quest_data) for quest_data in data["quests"]]
        
        return character


class Stats:
    """Character statistics system."""
    def __init__(self, race, character_class):
        """Initialize stats based on race and class."""
        self.race = race
        self.character_class = character_class
        
        # Primary attributes
        self.strength = 10  # Physical power, carrying capacity
        self.intelligence = 10  # Magic power, puzzle solving
        self.wisdom = 10  # Magic resistance, perception
        self.constitution = 10  # Health, physical resistance
        self.agility = 10  # Speed, dodge, critical chance
        self.perception = 10  # Find hidden things, accuracy
        self.charisma = 10  # NPC interactions, prices
        
        # Apply racial modifiers
        self.apply_racial_modifiers()
        
        # Apply class modifiers
        self.apply_class_modifiers()
        
        # Derived stats
        self.max_health = 0
        self.max_mana = 0
        self.health = 0
        self.mana = 0
        self.physical_attack = 0
        self.magical_attack = 0
        self.physical_defense = 0
        self.magical_defense = 0
        self.speed = 0
        
        # Open-world simulation specific stats
        self.rebelliousness = random.randint(1, 20)
        self.strategy = random.randint(1, 20)
        self.loyalty = random.randint(1, 20)
        self.diplomacy = random.randint(1, 20)
        
        # Calculate initial derived stats
        self.update_derived_stats()
    
    def apply_racial_modifiers(self):
        """Apply stat modifiers based on character race."""
        if self.race == "Human":
            # Humans are versatile
            self.strength += 1
            self.intelligence += 1
            self.wisdom += 1
            self.constitution += 1
            self.agility += 1
            self.charisma += 1
            
        elif self.race == "Dwarf":
            # Dwarves are tough and strong
            self.strength += 3
            self.constitution += 4
            self.agility -= 1
            self.intelligence -= 1
            
        elif self.race == "Elf":
            # Elves are intelligent and agile
            self.intelligence += 3
            self.agility += 3
            self.perception += 2
            self.constitution -= 2
            
        elif self.race == "Demon":
            # Demons are strong and charismatic but less wise
            self.strength += 4
            self.charisma += 2
            self.wisdom -= 3
            
        elif self.race == "Angel":
            # Angels are wise and charismatic
            self.wisdom += 4
            self.charisma += 3
            self.strength -= 1
            
        elif self.race == "Demigod":
            # Demigods have enhanced abilities across the board
            self.strength += 2
            self.intelligence += 2
            self.wisdom += 2
            self.constitution += 2
            
        elif self.race == "Messiah":
            # Messiahs are wise leaders
            self.wisdom += 5
            self.charisma += 5
            self.strength -= 2
            
        elif self.race == "Dragon":
            # Dragons are powerful but slow
            self.strength += 5
            self.constitution += 5
            self.intelligence += 3
            self.agility -= 3
            
        elif self.race == "Beastman":
            # Beastmen are strong and perceptive
            self.strength += 3
            self.perception += 3
            self.intelligence -= 2
            
        elif self.race == "Kaosborne":
            # Kaosborne have random stat distribution
            random_stats = ["strength", "intelligence", "wisdom", 
                          "constitution", "agility", "perception", "charisma"]
            for _ in range(3):
                stat = random.choice(random_stats)
                boost = random.randint(1, 5)
                setattr(self, stat, getattr(self, stat) + boost)
                
            for _ in range(2):
                stat = random.choice(random_stats)
                penalty = random.randint(1, 3)
                current = getattr(self, stat)
                # Don't reduce below 5
                setattr(self, stat, max(5, current - penalty))
    
    def apply_class_modifiers(self):
        """Apply stat modifiers based on character class."""
        if self.character_class == "Warrior":
            self.strength += 3
            self.constitution += 2
            self.intelligence -= 1
            
        elif self.character_class == "Mage":
            self.intelligence += 4
            self.wisdom += 2
            self.strength -= 2
            self.constitution -= 1
            
        elif self.character_class == "Ranger":
            self.agility += 3
            self.perception += 3
            self.constitution -= 1
            
        elif self.character_class == "Cleric":
            self.wisdom += 4
            self.charisma += 2
            self.agility -= 1
            
        elif self.character_class == "Rogue":
            self.agility += 4
            self.perception += 2
            self.constitution -= 1
            self.charisma += 1
            
        elif self.character_class == "Paladin":
            self.strength += 2
            self.constitution += 2
            self.wisdom += 2
            self.intelligence -= 1
            
        elif self.character_class == "Warlock":
            self.intelligence += 3
            self.wisdom -= 1
            self.charisma += 2
            self.constitution += 1
            
        elif self.character_class == "Bard":
            self.charisma += 4
            self.agility += 1
            self.intelligence += 1
            self.strength -= 1
            
        elif self.character_class == "Monk":
            self.agility += 3
            self.wisdom += 3
            self.strength += 1
            self.intelligence -= 1
            
        elif self.character_class == "Berserker":
            self.strength += 5
            self.constitution += 2
            self.wisdom -= 3
            self.intelligence -= 2
    
    def update_derived_stats(self):
        """Update all stats derived from primary attributes."""
        # Health calculation based on constitution and race
        base_health = 50 + (self.constitution * 10)
        if self.race == "Dwarf":
            base_health *= 1.2
        elif self.race == "Elf":
            base_health *= 0.9
        elif self.race == "Demon":
            base_health = 666 + (self.constitution * 6.66)
        elif self.race == "Angel":
            base_health = 333 + (self.constitution * 3.33)
        
        # Mana calculation based on intelligence/wisdom and class
        base_mana = 30 + (self.intelligence * 5) + (self.wisdom * 3)
        if self.character_class in ["Mage", "Warlock"]:
            base_mana *= 1.5
        elif self.character_class in ["Warrior", "Berserker"]:
            base_mana *= 0.5
        
        # Set the derived stats
        self.max_health = int(base_health)
        self.max_mana = int(base_mana)
        
        # Set current health/mana to max if they're zero (new character)
        if self.health == 0:
            self.health = self.max_health
        if self.mana == 0:
            self.mana = self.max_mana
        
        # Calculate attack stats
        self.physical_attack = int(5 + (self.strength * 1.5))
        self.magical_attack = int(5 + (self.intelligence * 1.2) + (self.wisdom * 0.8))
        
        # Calculate defense stats
        self.physical_defense = int(5 + (self.constitution * 1.2) + (self.strength * 0.5))
        self.magical_defense = int(5 + (self.wisdom * 1.5) + (self.intelligence * 0.3))
        
        # Calculate speed
        self.speed = int(10 + (self.agility * 2))
        self.leadership = (self.charisma + self.wisdom) / 2

        
    def apply_equipment_bonuses(self):
        """
        Recalculate stats based on equipped items.
        This would be called after equipping or unequipping items.
        """
        # This is a placeholder. In a full implementation, 
        # you would first reset bonuses then apply new ones from current equipment.
        self.update_derived_stats()
    
    def to_dict(self):
        """Convert stats to dictionary for saving."""
        return {
            "race": self.race,
            "character_class": self.character_class,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "constitution": self.constitution,
            "agility": self.agility,
            "perception": self.perception,
            "charisma": self.charisma,
            "health": self.health,
            "mana": self.mana,
            "max_health": self.max_health,
            "max_mana": self.max_mana,
            "rebelliousness": self.rebelliousness,
            "strategy": self.strategy,
            "loyalty": self.loyalty,
            "diplomacy": self.diplomacy
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create stats from dictionary data."""
        stats = cls(data["race"], data["character_class"])
        
        # Set all attributes from the data
        stats.strength = data["strength"]
        stats.intelligence = data["intelligence"]
        stats.wisdom = data["wisdom"]
        stats.constitution = data["constitution"]
        stats.agility = data["agility"]
        stats.perception = data["perception"]
        stats.charisma = data["charisma"]
        stats.health = data["health"]
        stats.mana = data["mana"]
        stats.max_health = data["max_health"]
        stats.max_mana = data["max_mana"]
        stats.rebelliousness = data["rebelliousness"]
        stats.strategy = data["strategy"]
        stats.loyalty = data["loyalty"]
        stats.diplomacy = data["diplomacy"]
        
        return stats


class PlayerCharacter(Character):
    """Player character with additional functionality."""
    def __init__(self, name, race=None, character_class=None):
        super().__init__(name, race, character_class)
        self.quests=[]
        self.location = "Starting Village"
        self.reputation = {"Starting Village": 0}  # Neutral reputation
        
    def rest(self):
        """Rest to recover health and mana."""
        old_health = self.stats.health
        old_mana = self.stats.mana
        
        self.stats.health = self.stats.max_health
        self.stats.mana = self.stats.max_mana
        
        health_recovered = self.stats.health - old_health
        mana_recovered = self.stats.mana - old_mana
        
        return f"You rested and recovered {health_recovered} health and {mana_recovered} mana."
    
    def change_location(self, new_location):
        """Move to a new location."""
        old_location = self.location
        self.location = new_location
        
        # Initialize reputation for new locations
        if new_location not in self.reputation:
            self.reputation[new_location] = 0
            
        return f"Traveled from {old_location} to {new_location}."
    
    def modify_reputation(self, location, amount):
        """Change reputation in a specific location."""
        if location in self.reputation:
            self.reputation[location] += amount
            return f"Reputation in {location} changed by {amount}. New reputation: {self.reputation[location]}"
        else:
            self.reputation[location] = amount
            return f"Established reputation in {location}: {amount}"
    
    def to_dict(self):
        """Convert player character to dictionary for saving."""
        data = super().to_dict()
        data.update({
            "location": self.location,
            "reputation": self.reputation
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create a player character from dictionary data."""
        character = super().from_dict(data)
        character.location = data["location"]
        character.reputation = data["reputation"]
        return character


def create_character():
    """Guide the user through character creation."""
    clear_screen()
    typewriter_effect("=== Character Creation ===\n")
    
    # Get character name
    name = input("Enter your character's name: ")
    
    # Choose race
    print("\nAvailable Races:")
    for i, race in enumerate(Character.races, 1):
        print(f"{i}. {race}")
    
    race_choice = input("\nChoose a race (number) or 'r' for random: ")
    if race_choice.lower() == 'r':
        race = Character.get_race()
        print(f"Random race selected: {race}")
    else:
        try:
            race_index = int(race_choice) - 1
            if 0 <= race_index < len(Character.races):
                race = Character.races[race_index]
            else:
                race = Character.get_race()
                print(f"Invalid selection. Random race assigned: {race}")
        except ValueError:
            race = Character.get_race()
            print(f"Invalid input. Random race assigned: {race}")
    
    # Choose class
    print("\nAvailable Classes:")
    for i, char_class in enumerate(Character.classes, 1):
        print(f"{i}. {char_class}")
    
    class_choice = input("\nChoose a class (number) or 'r' for random: ")
    if class_choice.lower() == 'r':
        character_class = Character.get_class()
        print(f"Random class selected: {character_class}")
    else:
        try:
            class_index = int(class_choice) - 1
            if 0 <= class_index < len(Character.classes):
                character_class = Character.classes[class_index]
            else:
                character_class = Character.get_class()
                print(f"Invalid selection. Random class assigned: {character_class}")
        except ValueError:
            character_class = Character.get_class()
            print(f"Invalid input. Random class assigned: {character_class}")
    
    # Create the character
    player = PlayerCharacter(name, race, character_class)
    
    # Initialize new systems
    from crafting import CraftingSystem
    from housing import HousingSystem
    from companions import CompanionSystem
    from achievements import AchievementSystem
    
    player.crafting_system = CraftingSystem()
    player.housing_system = HousingSystem()
    player.companion_system = CompanionSystem()
    player.achievement_system = AchievementSystem()
    
    # Display character info
    typewriter_effect(f"\nCharacter created: {player.name} the {player.race} {player.character_class}")
    input("\nPress Enter to continue...")
    
    return player
