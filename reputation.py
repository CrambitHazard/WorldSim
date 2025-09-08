# reputation.py
import random
from items import Item

class Faction:
    """Represents a faction in the game world."""
    def __init__(self, name, description, alignment, base_reputation=0):
        self.name = name
        self.description = description
        self.alignment = alignment  # "Good", "Neutral", "Evil"
        self.base_reputation = base_reputation
        self.members = []
        self.territory = []
        self.quests = []
        self.rewards = {}
    
    def get_reputation_level(self, reputation):
        """Get reputation level based on reputation value."""
        if reputation >= 100:
            return "Exalted"
        elif reputation >= 75:
            return "Honored"
        elif reputation >= 50:
            return "Friendly"
        elif reputation >= 25:
            return "Neutral"
        elif reputation >= 0:
            return "Unfriendly"
        else:
            return "Hostile"

class ReputationSystem:
    """Manages reputation with factions and NPCs."""
    
    def __init__(self):
        self.factions = self.initialize_factions()
        self.player_reputation = {}  # faction_name -> reputation_value
        self.npc_reputation = {}     # npc_name -> reputation_value
        self.reputation_events = []
    
    def initialize_factions(self):
        """Initialize all factions in the game world."""
        factions = []
        
        # Good factions
        factions.append(Faction("Guardians of Light", "Protectors of the realm", "Good", 25))
        factions.append(Faction("Merchant Guild", "Traders and craftsmen", "Good", 10))
        factions.append(Faction("Scholars Guild", "Keepers of knowledge", "Good", 15))
        
        # Neutral factions
        factions.append(Faction("Adventurers Guild", "Mercenaries and explorers", "Neutral", 0))
        factions.append(Faction("Thieves Guild", "Underground network", "Neutral", -10))
        factions.append(Faction("Mages Circle", "Arcane practitioners", "Neutral", 5))
        
        # Evil factions
        factions.append(Faction("Cult of Darkness", "Worshippers of evil", "Evil", -50))
        factions.append(Faction("Bandit Brotherhood", "Highway robbers", "Evil", -25))
        factions.append(Faction("Necromancer Order", "Masters of death", "Evil", -75))
        
        return factions
    
    def get_faction(self, faction_name):
        """Get a faction by name."""
        for faction in self.factions:
            if faction.name.lower() == faction_name.lower():
                return faction
        return None
    
    def get_player_reputation(self, faction_name):
        """Get player's reputation with a faction."""
        return self.player_reputation.get(faction_name, 0)
    
    def change_reputation(self, faction_name, amount, reason=""):
        """Change player's reputation with a faction."""
        current = self.get_player_reputation(faction_name)
        new_reputation = max(-100, min(100, current + amount))
        self.player_reputation[faction_name] = new_reputation
        
        # Record the event
        event = {
            "faction": faction_name,
            "change": amount,
            "new_total": new_reputation,
            "reason": reason
        }
        self.reputation_events.append(event)
        
        return new_reputation
    
    def get_reputation_level(self, faction_name):
        """Get the reputation level with a faction."""
        faction = self.get_faction(faction_name)
        if not faction:
            return "Unknown"
        
        reputation = self.get_player_reputation(faction_name)
        return faction.get_reputation_level(reputation)
    
    def can_access_faction_services(self, faction_name):
        """Check if player can access faction services."""
        reputation = self.get_player_reputation(faction_name)
        return reputation >= 25  # Friendly or higher
    
    def get_faction_rewards(self, faction_name):
        """Get available rewards from a faction based on reputation."""
        faction = self.get_faction(faction_name)
        if not faction:
            return []
        
        reputation = self.get_player_reputation(faction_name)
        rewards = []
        
        if reputation >= 100:  # Exalted
            rewards.extend([
                "Access to exclusive quests",
                "Special equipment discounts",
                "Unique faction items",
                "Faction companion recruitment"
            ])
        elif reputation >= 75:  # Honored
            rewards.extend([
                "Access to rare quests",
                "Equipment discounts",
                "Faction training"
            ])
        elif reputation >= 50:  # Friendly
            rewards.extend([
                "Basic quests",
                "Minor discounts",
                "Faction information"
            ])
        elif reputation >= 25:  # Neutral
            rewards.extend([
                "Basic services"
            ])
        
        return rewards
    
    def show_reputation_menu(self, player):
        """Display the reputation menu."""
        while True:
            print("\n=== REPUTATION MENU ===")
            print("Your Reputation:")
            
            for faction in self.factions:
                reputation = self.get_player_reputation(faction.name)
                level = self.get_reputation_level(faction.name)
                print(f"  {faction.name}: {reputation} ({level})")
            
            print("\nOptions:")
            print("1. View Faction Details")
            print("2. View Reputation History")
            print("3. Check Faction Rewards")
            print("4. Back")
            
            choice = input("\nChoose option: ")
            
            if choice == "1":
                self.view_faction_details()
            elif choice == "2":
                self.view_reputation_history()
            elif choice == "3":
                self.check_faction_rewards()
            elif choice == "4":
                break
            else:
                print("Invalid choice!")
    
    def view_faction_details(self):
        """View detailed information about factions."""
        print("\n=== FACTION DETAILS ===")
        
        for i, faction in enumerate(self.factions, 1):
            print(f"\n{i}. {faction.name}")
            print(f"   Alignment: {faction.alignment}")
            print(f"   Description: {faction.description}")
            
            reputation = self.get_player_reputation(faction.name)
            level = self.get_reputation_level(faction.name)
            print(f"   Your Reputation: {reputation} ({level})")
            
            if self.can_access_faction_services(faction.name):
                print("   ✓ Can access services")
            else:
                print("   ✗ Cannot access services")
    
    def view_reputation_history(self):
        """View recent reputation changes."""
        print("\n=== REPUTATION HISTORY ===")
        
        if not self.reputation_events:
            print("No reputation events recorded.")
            return
        
        # Show last 10 events
        recent_events = self.reputation_events[-10:]
        
        for event in recent_events:
            change = event["change"]
            sign = "+" if change > 0 else ""
            print(f"{event['faction']}: {sign}{change} ({event['reason']})")
    
    def check_faction_rewards(self):
        """Check available rewards from factions."""
        print("\n=== FACTION REWARDS ===")
        
        for faction in self.factions:
            reputation = self.get_player_reputation(faction.name)
            level = self.get_reputation_level(faction.name)
            
            print(f"\n{faction.name} ({level}):")
            rewards = self.get_faction_rewards(faction.name)
            
            if rewards:
                for reward in rewards:
                    print(f"  • {reward}")
            else:
                print("  No rewards available")
    
    def handle_quest_completion(self, player, quest_type, faction_name=None):
        """Handle reputation changes for quest completion."""
        if not faction_name:
            # Determine faction based on quest type
            if "guard" in quest_type.lower() or "protect" in quest_type.lower():
                faction_name = "Guardians of Light"
            elif "trade" in quest_type.lower() or "merchant" in quest_type.lower():
                faction_name = "Merchant Guild"
            elif "research" in quest_type.lower() or "knowledge" in quest_type.lower():
                faction_name = "Scholars Guild"
            elif "adventure" in quest_type.lower() or "explore" in quest_type.lower():
                faction_name = "Adventurers Guild"
            elif "steal" in quest_type.lower() or "thief" in quest_type.lower():
                faction_name = "Thieves Guild"
            elif "magic" in quest_type.lower() or "spell" in quest_type.lower():
                faction_name = "Mages Circle"
            else:
                faction_name = "Adventurers Guild"
        
        # Award reputation based on quest type
        reputation_gain = random.randint(5, 15)
        self.change_reputation(faction_name, reputation_gain, f"Completed {quest_type} quest")
        
        return f"Gained {reputation_gain} reputation with {faction_name}!"
    
    def handle_combat_action(self, player, action_type, target_faction=None):
        """Handle reputation changes for combat actions."""
        if action_type == "help_innocent":
            self.change_reputation("Guardians of Light", 10, "Helped innocent")
            return "Gained reputation with Guardians of Light"
        
        elif action_type == "attack_guard":
            self.change_reputation("Guardians of Light", -20, "Attacked guard")
            return "Lost reputation with Guardians of Light"
        
        elif action_type == "rob_merchant":
            self.change_reputation("Merchant Guild", -15, "Robbed merchant")
            return "Lost reputation with Merchant Guild"
        
        elif action_type == "help_merchant":
            self.change_reputation("Merchant Guild", 10, "Helped merchant")
            return "Gained reputation with Merchant Guild"
        
        elif action_type == "steal_success":
            self.change_reputation("Thieves Guild", 5, "Successful theft")
            return "Gained reputation with Thieves Guild"
        
        elif action_type == "kill_innocent":
            self.change_reputation("Guardians of Light", -30, "Killed innocent")
            return "Lost reputation with Guardians of Light"
        
        return "No reputation change"
    
    def get_faction_quest(self, faction_name):
        """Get a quest from a faction based on reputation."""
        faction = self.get_faction(faction_name)
        if not faction:
            return None
        
        reputation = self.get_player_reputation(faction_name)
        
        if reputation < 25:
            return None  # Not friendly enough
        
        # Generate quest based on faction
        if faction.name == "Guardians of Light":
            quests = [
                "Patrol the town for threats",
                "Escort a merchant caravan",
                "Investigate suspicious activity",
                "Defend against bandit attack"
            ]
        elif faction.name == "Merchant Guild":
            quests = [
                "Deliver goods to another town",
                "Negotiate trade deals",
                "Protect merchant from thieves",
                "Collect outstanding debts"
            ]
        elif faction.name == "Scholars Guild":
            quests = [
                "Recover ancient texts",
                "Research magical artifacts",
                "Translate ancient scrolls",
                "Map unexplored ruins"
            ]
        elif faction.name == "Adventurers Guild":
            quests = [
                "Explore dangerous dungeon",
                "Hunt down a monster",
                "Retrieve lost treasure",
                "Clear bandit camp"
            ]
        elif faction.name == "Thieves Guild":
            quests = [
                "Steal valuable item",
                "Plant evidence",
                "Gather information",
                "Sabotage rival operation"
            ]
        elif faction.name == "Mages Circle":
            quests = [
                "Collect rare ingredients",
                "Test experimental spells",
                "Investigate magical disturbance",
                "Recruit new mage"
            ]
        else:
            quests = ["Generic quest"]
        
        return random.choice(quests)
    
    def can_join_faction(self, faction_name):
        """Check if player can join a faction."""
        reputation = self.get_player_reputation(faction_name)
        return reputation >= 50  # Friendly or higher
    
    def join_faction(self, player, faction_name):
        """Join a faction."""
        if not self.can_join_faction(faction_name):
            return f"Reputation too low to join {faction_name}"
        
        if not hasattr(player, 'factions'):
            player.factions = []
        
        if faction_name not in player.factions:
            player.factions.append(faction_name)
            return f"Successfully joined {faction_name}!"
        else:
            return f"Already a member of {faction_name}"

def generate_faction_item(faction_name, player_level):
    """Generate a faction-specific item."""
    faction = None
    for f in ReputationSystem().factions:
        if f.name.lower() == faction_name.lower():
            faction = f
            break
    
    if not faction:
        return None
    
    # Generate items based on faction
    if faction.name == "Guardians of Light":
        items = [
            ("Guardian's Shield", "A blessed shield of protection", 150),
            ("Light Blade", "A sword that glows with holy light", 200),
            ("Protection Amulet", "Wards against evil", 100)
        ]
    elif faction.name == "Merchant Guild":
        items = [
            ("Merchant's Scale", "Ensures fair trade", 75),
            ("Trade Ledger", "Records all transactions", 50),
            ("Lucky Coin", "Brings good fortune", 125)
        ]
    elif faction.name == "Scholars Guild":
        items = [
            ("Scholar's Quill", "Never runs out of ink", 80),
            ("Ancient Tome", "Contains forgotten knowledge", 300),
            ("Memory Crystal", "Stores information", 200)
        ]
    elif faction.name == "Adventurers Guild":
        items = [
            ("Adventurer's Map", "Shows hidden paths", 120),
            ("Survival Kit", "Essential for exploration", 90),
            ("Monster Manual", "Information on creatures", 150)
        ]
    elif faction.name == "Thieves Guild":
        items = [
            ("Shadow Cloak", "Aids in stealth", 180),
            ("Lockpick Set", "Opens any lock", 100),
            ("Silent Boots", "Makes no sound", 140)
        ]
    elif faction.name == "Mages Circle":
        items = [
            ("Mage's Staff", "Channels magical power", 250),
            ("Spellbook", "Contains arcane knowledge", 400),
            ("Mana Crystal", "Stores magical energy", 175)
        ]
    else:
        items = [
            ("Faction Badge", "Shows membership", 50),
            ("Faction Ring", "Symbol of loyalty", 75)
        ]
    
    name, description, base_value = random.choice(items)
    value = base_value + player_level * 5
    
    return Item(name, description, value, "faction_item", {"faction": faction_name})