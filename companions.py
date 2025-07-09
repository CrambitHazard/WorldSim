# companions.py
import random
from character import Character

class Companion(Character):
    """Represents a companion animal that can fight alongside the player."""
    
    def __init__(self, name, species, level=1):
        super().__init__(name, race="Beast", character_class="Companion")
        self.species = species
        self.loyalty = 50  # 0-100 scale
        self.happiness = 80  # 0-100 scale
        self.training_level = 1
        self.special_abilities = []
        self.owner = None
        
        # Set species-specific stats
        self.setup_species_stats()
    
    def setup_species_stats(self):
        """Set up stats based on species."""
        species_stats = {
            "Wolf": {
                "strength": 8, "agility": 12, "intelligence": 6, "wisdom": 8,
                "constitution": 10, "perception": 14, "charisma": 4,
                "special_abilities": ["Pack Tactics", "Night Vision"]
            },
            "Eagle": {
                "strength": 6, "agility": 16, "intelligence": 8, "wisdom": 10,
                "constitution": 8, "perception": 18, "charisma": 6,
                "special_abilities": ["Aerial Attack", "Sharp Vision"]
            },
            "Bear": {
                "strength": 14, "agility": 6, "intelligence": 8, "wisdom": 10,
                "constitution": 12, "perception": 8, "charisma": 4,
                "special_abilities": ["Thick Hide", "Powerful Claws"]
            },
            "Fox": {
                "strength": 6, "agility": 14, "intelligence": 12, "wisdom": 10,
                "constitution": 8, "perception": 16, "charisma": 8,
                "special_abilities": ["Stealth", "Quick Reflexes"]
            },
            "Horse": {
                "strength": 10, "agility": 12, "intelligence": 8, "wisdom": 10,
                "constitution": 12, "perception": 10, "charisma": 6,
                "special_abilities": ["Swift Movement", "Carrying Capacity"]
            },
            "Cat": {
                "strength": 6, "agility": 16, "intelligence": 10, "wisdom": 8,
                "constitution": 8, "perception": 14, "charisma": 8,
                "special_abilities": ["Stealth", "Agile Movement"]
            }
        }
        
        if self.species in species_stats:
            stats = species_stats[self.species]
            for stat, value in stats.items():
                if stat != "special_abilities":
                    setattr(self.stats, stat, value)
            
            self.special_abilities = stats.get("special_abilities", [])
        
        # Update derived stats
        self.stats.update_derived_stats()
    
    def train(self, training_type):
        """Train the companion to improve its abilities."""
        training_effects = {
            "combat": {
                "strength": 1, "agility": 1, "constitution": 1,
                "message": "Combat training improves fighting abilities"
            },
            "obedience": {
                "loyalty": 5, "happiness": 3,
                "message": "Obedience training improves loyalty"
            },
            "agility": {
                "agility": 2, "perception": 1,
                "message": "Agility training improves movement and awareness"
            },
            "intelligence": {
                "intelligence": 2, "wisdom": 1,
                "message": "Intelligence training improves problem-solving"
            }
        }
        
        if training_type in training_effects:
            effects = training_effects[training_type]
            for stat, bonus in effects.items():
                if hasattr(self, stat):
                    current = getattr(self, stat)
                    setattr(self, stat, min(100, current + bonus))
                elif hasattr(self.stats, stat):
                    current = getattr(self.stats, stat)
                    setattr(self.stats, stat, current + bonus)
            
            self.training_level += 1
            self.loyalty = min(100, self.loyalty + 2)
            self.happiness = min(100, self.happiness + 1)
            
            return effects["message"]
        
        return "Invalid training type"
    
    def feed(self, food_quality):
        """Feed the companion to improve happiness and health."""
        if food_quality == "poor":
            health_gain = 5
            happiness_gain = 2
        elif food_quality == "good":
            health_gain = 15
            happiness_gain = 5
        elif food_quality == "excellent":
            health_gain = 25
            happiness_gain = 10
        else:
            return "Invalid food quality"
        
        self.stats.health = min(self.stats.max_health, self.stats.health + health_gain)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.loyalty = min(100, self.loyalty + 1)
        
        return f"Fed {self.name} with {food_quality} food. Health +{health_gain}, Happiness +{happiness_gain}"
    
    def use_special_ability(self, ability_name, target=None):
        """Use a special ability in combat."""
        if ability_name not in self.special_abilities:
            return f"{self.name} doesn't know {ability_name}"
        
        if ability_name == "Pack Tactics":
            # Bonus damage when fighting alongside owner
            return f"{self.name} uses Pack Tactics for coordinated attack!"
        elif ability_name == "Aerial Attack":
            # High damage attack from above
            return f"{self.name} performs an aerial attack!"
        elif ability_name == "Thick Hide":
            # Damage reduction
            return f"{self.name} uses Thick Hide to reduce damage!"
        elif ability_name == "Stealth":
            # Sneak attack bonus
            return f"{self.name} uses Stealth for a surprise attack!"
        elif ability_name == "Swift Movement":
            # Movement bonus
            return f"{self.name} uses Swift Movement to move quickly!"
        elif ability_name == "Agile Movement":
            # Dodge bonus
            return f"{self.name} uses Agile Movement to dodge attacks!"
        
        return f"{self.name} uses {ability_name}!"
    
    def get_status(self):
        """Get companion status information."""
        return {
            "name": self.name,
            "species": self.species,
            "level": self.level,
            "health": f"{self.stats.health}/{self.stats.max_health}",
            "loyalty": self.loyalty,
            "happiness": self.happiness,
            "training_level": self.training_level,
            "special_abilities": self.special_abilities
        }
    
    def to_dict(self):
        """Convert companion to dictionary for saving."""
        data = super().to_dict()
        data.update({
            "species": self.species,
            "loyalty": self.loyalty,
            "happiness": self.happiness,
            "training_level": self.training_level,
            "special_abilities": self.special_abilities
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create companion from dictionary."""
        companion = cls(data["name"], data["species"], data["level"])
        companion.loyalty = data.get("loyalty", 50)
        companion.happiness = data.get("happiness", 80)
        companion.training_level = data.get("training_level", 1)
        companion.special_abilities = data.get("special_abilities", [])
        
        # Load stats
        from character import Stats
        companion.stats = Stats.from_dict(data["stats"])
        
        return companion

class CompanionSystem:
    """Manages the companion system."""
    
    def __init__(self):
        self.available_species = ["Wolf", "Eagle", "Bear", "Fox", "Horse", "Cat"]
        self.companion_names = [
            "Shadow", "Storm", "Thunder", "Lightning", "Frost", "Flame",
            "River", "Mountain", "Forest", "Sky", "Wind", "Earth",
            "Swift", "Brave", "Wise", "Strong", "Clever", "Noble"
        ]
    
    def find_companion(self, player):
        """Find a new companion in the wild."""
        if hasattr(player, 'companion') and player.companion:
            print("You already have a companion!")
            return
        
        print("\n=== FINDING COMPANION ===")
        print("You search for a companion in the wilderness...")
        
        # Random chance to find a companion
        if random.random() < 0.3:  # 30% chance
            species = random.choice(self.available_species)
            name = random.choice(self.companion_names)
            
            print(f"You found a {species.lower()} named {name}!")
            print("Do you want to try to tame it? (y/n)")
            
            choice = input().lower()
            if choice == 'y':
                success_chance = 0.6  # 60% chance to tame
                if random.random() < success_chance:
                    companion = Companion(name, species)
                    companion.owner = player
                    player.companion = companion
                    print(f"Successfully tamed {name} the {species}!")
                    print(f"{name} is now your loyal companion!")
                else:
                    print(f"The {species} ran away!")
            else:
                print("You leave the animal alone.")
        else:
            print("You didn't find any suitable companions.")
    
    def train_companion(self, player):
        """Train the player's companion."""
        if not hasattr(player, 'companion') or not player.companion:
            print("You don't have a companion to train!")
            return
        
        companion = player.companion
        
        print(f"\n=== TRAINING {companion.name.upper()} ===")
        print(f"Training Level: {companion.training_level}")
        print(f"Loyalty: {companion.loyalty}/100")
        print(f"Happiness: {companion.happiness}/100")
        
        print("\nTraining Options:")
        print("1. Combat Training (Improves fighting abilities)")
        print("2. Obedience Training (Improves loyalty)")
        print("3. Agility Training (Improves movement)")
        print("4. Intelligence Training (Improves problem-solving)")
        print("5. Back")
        
        try:
            choice = int(input("\nChoose training type: "))
            
            training_types = ["combat", "obedience", "agility", "intelligence"]
            if 1 <= choice <= 4:
                training_type = training_types[choice - 1]
                message = companion.train(training_type)
                print(f"\n{message}")
                print(f"{companion.name}'s training level is now {companion.training_level}!")
            elif choice == 5:
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def feed_companion(self, player):
        """Feed the player's companion."""
        if not hasattr(player, 'companion') or not player.companion:
            print("You don't have a companion to feed!")
            return
        
        companion = player.companion
        
        print(f"\n=== FEEDING {companion.name.upper()} ===")
        print("Food Options:")
        print("1. Poor Food (5 gold) - Basic nutrition")
        print("2. Good Food (15 gold) - Nutritious meal")
        print("3. Excellent Food (30 gold) - Premium feast")
        print("4. Back")
        
        try:
            choice = int(input("\nChoose food quality: "))
            
            food_options = {
                1: ("poor", 5),
                2: ("good", 15),
                3: ("excellent", 30)
            }
            
            if choice in food_options:
                quality, cost = food_options[choice]
                
                if player.gold >= cost:
                    player.gold -= cost
                    message = companion.feed(quality)
                    print(f"\n{message}")
                else:
                    print(f"Not enough gold! Need {cost} gold.")
            elif choice == 4:
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def companion_status(self, player):
        """Show companion status."""
        if not hasattr(player, 'companion') or not player.companion:
            print("You don't have a companion!")
            return
        
        companion = player.companion
        status = companion.get_status()
        
        print(f"\n=== {companion.name.upper()} STATUS ===")
        print(f"Species: {status['species']}")
        print(f"Level: {status['level']}")
        print(f"Health: {status['health']}")
        print(f"Loyalty: {status['loyalty']}/100")
        print(f"Happiness: {status['happiness']}/100")
        print(f"Training Level: {status['training_level']}")
        print(f"Special Abilities: {', '.join(status['special_abilities'])}")
        
        # Show stats
        print(f"\nStats:")
        print(f"Strength: {companion.stats.strength}")
        print(f"Agility: {companion.stats.agility}")
        print(f"Intelligence: {companion.stats.intelligence}")
        print(f"Constitution: {companion.stats.constitution}")
        print(f"Perception: {companion.stats.perception}")
    
    def show_companion_menu(self, player):
        """Display the companion menu."""
        while True:
            print("\n=== COMPANION MENU ===")
            if hasattr(player, 'companion') and player.companion:
                print(f"Current Companion: {player.companion.name} the {player.companion.species}")
            else:
                print("No companion")
            
            print("1. Find Companion")
            print("2. Train Companion")
            print("3. Feed Companion")
            print("4. Companion Status")
            print("5. Back")
            
            choice = input("\nChoose option: ")
            
            if choice == "1":
                self.find_companion(player)
            elif choice == "2":
                self.train_companion(player)
            elif choice == "3":
                self.feed_companion(player)
            elif choice == "4":
                self.companion_status(player)
                input("\nPress Enter to continue...")
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

def generate_companion_food():
    """Generate random companion food."""
    from items import Item
    food_types = [
        ("Poor Food", "Basic animal feed", 5, "poor"),
        ("Good Food", "Quality pet food", 15, "good"),
        ("Excellent Food", "Premium companion feast", 30, "excellent")
    ]
    
    name, description, value, quality = random.choice(food_types)
    return Item(name, description, value, "consumable", {"companion_food": quality})