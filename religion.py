# religion.py
import random
from items import Item

class God:
    """Represents a deity in the game world."""
    def __init__(self, name, domain, description, alignment, favored_class=None):
        self.name = name
        self.domain = domain  # e.g., "War", "Healing", "Nature", "Death"
        self.description = description
        self.alignment = alignment  # "Good", "Neutral", "Evil"
        self.favored_class = favored_class
        self.followers = []
        self.power = 100  # Divine power level
        self.miracles = []
    
    def grant_miracle(self, follower):
        """Grant a miracle to a follower."""
        if self.power < 10:
            return f"{self.name} is too weak to grant miracles."
        
        miracle = random.choice(self.miracles)
        self.power -= 10
        
        if miracle["type"] == "heal":
            healing = miracle["value"]
            follower.stats.health = min(follower.stats.max_health, follower.stats.health + healing)
            return f"{self.name} grants healing! +{healing} health."
        
        elif miracle["type"] == "bless":
            stat = miracle["stat"]
            bonus = miracle["value"]
            setattr(follower.stats, stat, getattr(follower.stats, stat) + bonus)
            return f"{self.name} grants a blessing! +{bonus} to {stat}."
        
        elif miracle["type"] == "protection":
            duration = miracle["duration"]
            from combat import BuffEffect
            protection = BuffEffect(f"{self.name}'s Protection", duration, "physical_defense", miracle["value"])
            protection.apply(follower)
            return f"{self.name} grants protection for {duration} turns."
        
        return f"{self.name} grants a miracle!"

class Religion:
    """Represents a religion with followers and beliefs."""
    def __init__(self, name, god, description):
        self.name = name
        self.god = god
        self.description = description
        self.followers = []
        self.temples = []
        self.holy_days = []
        self.rituals = []
    
    def add_follower(self, character):
        """Add a character as a follower."""
        if character not in self.followers:
            self.followers.append(character)
            self.god.followers.append(character)
            character.religion = self
            return f"{character.name} has converted to {self.name}!"
        return f"{character.name} is already a follower of {self.name}."
    
    def remove_follower(self, character):
        """Remove a character as a follower."""
        if character in self.followers:
            self.followers.remove(character)
            if character in self.god.followers:
                self.god.followers.remove(character)
            character.religion = None
            return f"{character.name} has left {self.name}."
        return f"{character.name} is not a follower of {self.name}."

class Temple:
    """Represents a temple where followers can worship."""
    def __init__(self, name, religion, location, size="medium"):
        self.name = name
        self.religion = religion
        self.location = location
        self.size = size  # "small", "medium", "large"
        self.priests = []
        self.visitors = []
        self.donations = 0
        self.influence = 50  # 0-100 scale
    
    def pray(self, character):
        """Allow a character to pray at the temple."""
        if not hasattr(character, 'religion') or character.religion != self.religion:
            return f"{character.name} is not a follower of {self.religion.name}."
        
        # Prayer effects
        effects = []
        
        # Restore some health and mana
        health_gain = random.randint(5, 15)
        mana_gain = random.randint(5, 15)
        character.stats.health = min(character.stats.max_health, character.stats.health + health_gain)
        character.stats.mana = min(character.stats.max_mana, character.stats.mana + mana_gain)
        effects.append(f"Restored {health_gain} health and {mana_gain} mana")
        
        # Chance for divine intervention
        if random.random() < 0.1:  # 10% chance
            miracle = self.religion.god.grant_miracle(character)
            effects.append(miracle)
        
        # Increase temple influence
        self.influence = min(100, self.influence + 1)
        
        return f"{character.name} prays at {self.name}. " + ". ".join(effects)
    
    def donate(self, character, amount):
        """Allow a character to donate to the temple."""
        if character.gold < amount:
            return f"{character.name} doesn't have enough gold to donate {amount}."
        
        character.gold -= amount
        self.donations += amount
        self.influence = min(100, self.influence + amount // 10)
        
        # Blessing for generous donations
        if amount >= 100:
            blessing = random.randint(1, 3)
            setattr(character.stats, "charisma", getattr(character.stats, "charisma") + blessing)
            return f"{character.name} donates {amount} gold. The temple is grateful! +{blessing} charisma."
        
        return f"{character.name} donates {amount} gold to {self.name}."

class ReligionSystem:
    """Manages the religion system."""
    
    def __init__(self):
        self.gods = self.initialize_gods()
        self.religions = self.initialize_religions()
        self.temples = self.initialize_temples()
    
    def initialize_gods(self):
        """Initialize the pantheon of gods."""
        gods = []
        
        # Good gods
        gods.append(God("Aethon", "Light", "God of light and healing", "Good", "Cleric"))
        gods.append(God("Valeria", "War", "Goddess of honorable combat", "Good", "Paladin"))
        gods.append(God("Sylvan", "Nature", "God of nature and growth", "Good", "Ranger"))
        
        # Neutral gods
        gods.append(God("Thorne", "Knowledge", "God of wisdom and learning", "Neutral", "Mage"))
        gods.append(God("Raven", "Death", "God of death and the afterlife", "Neutral", "Necromancer"))
        gods.append(God("Forge", "Crafting", "God of smithing and creation", "Neutral", "Blacksmith"))
        
        # Evil gods
        gods.append(God("Malice", "Destruction", "God of chaos and destruction", "Evil", "Warlock"))
        gods.append(God("Shadow", "Deception", "Goddess of lies and trickery", "Evil", "Rogue"))
        gods.append(God("Plague", "Disease", "God of sickness and decay", "Evil", "Necromancer"))
        
        # Add miracles to gods
        for god in gods:
            if god.domain == "Light":
                god.miracles = [
                    {"type": "heal", "value": 50},
                    {"type": "bless", "stat": "wisdom", "value": 5},
                    {"type": "protection", "value": 15, "duration": 5}
                ]
            elif god.domain == "War":
                god.miracles = [
                    {"type": "bless", "stat": "strength", "value": 10},
                    {"type": "bless", "stat": "agility", "value": 5},
                    {"type": "protection", "value": 20, "duration": 3}
                ]
            elif god.domain == "Nature":
                god.miracles = [
                    {"type": "heal", "value": 30},
                    {"type": "bless", "stat": "constitution", "value": 5},
                    {"type": "protection", "value": 10, "duration": 8}
                ]
            elif god.domain == "Knowledge":
                god.miracles = [
                    {"type": "bless", "stat": "intelligence", "value": 8},
                    {"type": "bless", "stat": "wisdom", "value": 5},
                    {"type": "heal", "value": 20}
                ]
            elif god.domain == "Death":
                god.miracles = [
                    {"type": "bless", "stat": "intelligence", "value": 5},
                    {"type": "protection", "value": 25, "duration": 2},
                    {"type": "heal", "value": 40}
                ]
            elif god.domain == "Crafting":
                god.miracles = [
                    {"type": "bless", "stat": "strength", "value": 5},
                    {"type": "bless", "stat": "intelligence", "value": 5},
                    {"type": "heal", "value": 25}
                ]
            elif god.domain == "Destruction":
                god.miracles = [
                    {"type": "bless", "stat": "strength", "value": 15},
                    {"type": "bless", "stat": "agility", "value": 10},
                    {"type": "protection", "value": 30, "duration": 1}
                ]
            elif god.domain == "Deception":
                god.miracles = [
                    {"type": "bless", "stat": "agility", "value": 15},
                    {"type": "bless", "stat": "charisma", "value": 10},
                    {"type": "protection", "value": 15, "duration": 4}
                ]
            elif god.domain == "Disease":
                god.miracles = [
                    {"type": "bless", "stat": "constitution", "value": 10},
                    {"type": "bless", "stat": "intelligence", "value": 8},
                    {"type": "heal", "value": 35}
                ]
        
        return gods
    
    def initialize_religions(self):
        """Initialize religions based on gods."""
        religions = []
        
        for god in self.gods:
            religion_name = f"Church of {god.name}"
            description = f"Followers of {god.name}, the {god.domain} god."
            religions.append(Religion(religion_name, god, description))
        
        return religions
    
    def initialize_temples(self):
        """Initialize temples in the world."""
        temples = []
        
        locations = ["Starting Village", "Eldenvale", "Stormwatch", "Duskridge", "Ironhold"]
        
        for religion in self.religions:
            location = random.choice(locations)
            temple_name = f"Temple of {religion.god.name}"
            size = random.choice(["small", "medium", "large"])
            temples.append(Temple(temple_name, religion, location, size))
        
        return temples
    
    def find_temple(self, location):
        """Find a temple in a specific location."""
        for temple in self.temples:
            if temple.location == location:
                return temple
        return None
    
    def convert_player(self, player, religion_name):
        """Convert the player to a religion."""
        religion = None
        for r in self.religions:
            if r.name.lower() == religion_name.lower():
                religion = r
                break
        
        if not religion:
            return f"Religion '{religion_name}' not found."
        
        if hasattr(player, 'religion') and player.religion:
            old_religion = player.religion.name
            player.religion.remove_follower(player)
        
        result = religion.add_follower(player)
        return result
    
    def show_religion_menu(self, player):
        """Display the religion menu."""
        while True:
            print("\n=== RELIGION MENU ===")
            
            if hasattr(player, 'religion') and player.religion:
                print(f"Current Religion: {player.religion.name}")
                print(f"God: {player.religion.god.name} ({player.religion.god.domain})")
                print(f"Alignment: {player.religion.god.alignment}")
            else:
                print("No religion")
            
            print("\nOptions:")
            print("1. Visit Temple")
            print("2. Convert to Religion")
            print("3. View All Religions")
            print("4. Pray")
            print("5. Donate")
            print("6. Back")
            
            choice = input("\nChoose option: ")
            
            if choice == "1":
                self.visit_temple(player)
            elif choice == "2":
                self.convert_menu(player)
            elif choice == "3":
                self.view_religions()
            elif choice == "4":
                self.pray(player)
            elif choice == "5":
                self.donate_menu(player)
            elif choice == "6":
                break
            else:
                print("Invalid choice!")
    
    def visit_temple(self, player):
        """Visit a temple in the current location."""
        temple = self.find_temple(player.location)
        
        if not temple:
            print(f"No temple found in {player.location}.")
            return
        
        print(f"\n=== {temple.name.upper()} ===")
        print(f"Religion: {temple.religion.name}")
        print(f"God: {temple.religion.god.name}")
        print(f"Size: {temple.size}")
        print(f"Influence: {temple.influence}/100")
        print(f"Donations: {temple.donations} gold")
        
        print("\nOptions:")
        print("1. Pray")
        print("2. Donate")
        print("3. Convert")
        print("4. Back")
        
        choice = input("\nChoose option: ")
        
        if choice == "1":
            result = temple.pray(player)
            print(f"\n{result}")
        elif choice == "2":
            self.donate_menu(player, temple)
        elif choice == "3":
            if not hasattr(player, 'religion') or player.religion != temple.religion:
                result = temple.religion.add_follower(player)
                print(f"\n{result}")
            else:
                print("You are already a follower of this religion.")
        elif choice == "4":
            return
        else:
            print("Invalid choice!")
    
    def convert_menu(self, player):
        """Menu for converting to a religion."""
        print("\n=== CONVERT TO RELIGION ===")
        print("Available Religions:")
        
        for i, religion in enumerate(self.religions, 1):
            print(f"{i}. {religion.name} - {religion.god.name} ({religion.god.domain})")
        
        try:
            choice = int(input("\nChoose religion (or 0 to cancel): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(self.religions):
                religion = self.religions[choice]
                result = self.convert_player(player, religion.name)
                print(f"\n{result}")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def view_religions(self):
        """View all available religions."""
        print("\n=== ALL RELIGIONS ===")
        
        for religion in self.religions:
            print(f"\n{religion.name}")
            print(f"  God: {religion.god.name}")
            print(f"  Domain: {religion.god.domain}")
            print(f"  Alignment: {religion.god.alignment}")
            print(f"  Followers: {len(religion.followers)}")
            print(f"  Description: {religion.description}")
    
    def pray(self, player):
        """Allow the player to pray."""
        if not hasattr(player, 'religion') or not player.religion:
            print("You don't follow any religion.")
            return
        
        temple = self.find_temple(player.location)
        if not temple or temple.religion != player.religion:
            print("No temple of your religion in this location.")
            return
        
        result = temple.pray(player)
        print(f"\n{result}")
    
    def donate_menu(self, player, temple=None):
        """Menu for donating to a temple."""
        if not temple:
            temple = self.find_temple(player.location)
            if not temple:
                print("No temple in this location.")
                return
        
        print(f"\n=== DONATE TO {temple.name.upper()} ===")
        print(f"Your gold: {player.gold}")
        print(f"Current donations: {temple.donations} gold")
        
        print("\nDonation amounts:")
        print("1. 10 gold")
        print("2. 25 gold")
        print("3. 50 gold")
        print("4. 100 gold")
        print("5. Custom amount")
        print("6. Back")
        
        try:
            choice = int(input("\nChoose amount: "))
            
            if choice == 1:
                amount = 10
            elif choice == 2:
                amount = 25
            elif choice == 3:
                amount = 50
            elif choice == 4:
                amount = 100
            elif choice == 5:
                amount = int(input("Enter custom amount: "))
            elif choice == 6:
                return
            else:
                print("Invalid choice!")
                return
            
            result = temple.donate(player, amount)
            print(f"\n{result}")
            
        except ValueError:
            print("Invalid input!")

def generate_holy_relic(player_level):
    """Generate a random holy relic."""
    relic_types = [
        ("Holy Symbol", "A blessed symbol of divine power", 100),
        ("Sacred Scroll", "Ancient text with divine wisdom", 150),
        ("Relic Fragment", "A piece of a powerful artifact", 200),
        ("Blessed Water", "Holy water with healing properties", 75),
        ("Divine Essence", "Pure divine energy in crystal form", 300)
    ]
    
    name, description, base_value = random.choice(relic_types)
    value = base_value + player_level * 10
    
    # Add religious bonuses
    bonuses = {"charisma": 2, "wisdom": 1}
    
    return Item(name, description, value, "relic", bonuses)