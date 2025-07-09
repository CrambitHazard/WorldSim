# magic_system.py
import random
from items import Item

class Spell:
    """Represents a magical spell that can be learned and cast."""
    def __init__(self, name, description, mana_cost, spell_type, effect, level_required=1):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost
        self.spell_type = spell_type  # "damage", "heal", "buff", "debuff", "utility"
        self.effect = effect
        self.level_required = level_required
        self.cast_count = 0
    
    def cast(self, caster, target=None):
        """Cast the spell and return the result."""
        if caster.stats.mana < self.mana_cost:
            return f"Insufficient mana to cast {self.name}!"
        
        caster.stats.mana -= self.mana_cost
        self.cast_count += 1
        
        if self.spell_type == "damage":
            damage = self.effect["damage"]
            if target:
                target.stats.health = max(0, target.stats.health - damage)
                return f"{caster.name} casts {self.name} at {target.name} for {damage} damage!"
            else:
                return f"{caster.name} casts {self.name} for {damage} damage!"
        
        elif self.spell_type == "heal":
            healing = self.effect["healing"]
            if target:
                target.stats.health = min(target.stats.max_health, target.stats.health + healing)
                return f"{caster.name} casts {self.name} on {target.name}, healing {healing} health!"
            else:
                caster.stats.health = min(caster.stats.max_health, caster.stats.health + healing)
                return f"{caster.name} casts {self.name}, healing {healing} health!"
        
        elif self.spell_type == "buff":
            stat = self.effect["stat"]
            bonus = self.effect["bonus"]
            duration = self.effect.get("duration", 3)
            
            if target:
                # Apply buff to target
                from combat import BuffEffect
                buff = BuffEffect(self.name, duration, stat, bonus)
                buff.apply(target)
                return f"{caster.name} casts {self.name} on {target.name}, granting +{bonus} {stat}!"
            else:
                # Apply buff to caster
                from combat import BuffEffect
                buff = BuffEffect(self.name, duration, stat, bonus)
                buff.apply(caster)
                return f"{caster.name} casts {self.name}, gaining +{bonus} {stat}!"
        
        elif self.spell_type == "debuff":
            stat = self.effect["stat"]
            penalty = self.effect["penalty"]
            duration = self.effect.get("duration", 3)
            
            if target:
                # Apply debuff to target
                from combat import BuffEffect
                debuff = BuffEffect(self.name, duration, stat, -penalty)
                debuff.apply(target)
                return f"{caster.name} casts {self.name} on {target.name}, reducing {stat} by {penalty}!"
            else:
                return f"{caster.name} casts {self.name}!"
        
        elif self.spell_type == "utility":
            effect_desc = self.effect.get("description", "mystical effect")
            return f"{caster.name} casts {self.name}, creating {effect_desc}!"
        
        return f"{caster.name} casts {self.name}!"

class MagicSystem:
    """Manages the magic system and spell learning."""
    
    def __init__(self):
        self.available_spells = self.initialize_spells()
        self.magic_schools = ["Evocation", "Abjuration", "Conjuration", "Divination", "Enchantment", "Illusion", "Necromancy", "Transmutation"]
    
    def initialize_spells(self):
        """Initialize all available spells."""
        spells = []
        
        # Evocation (damage spells)
        spells.extend([
            Spell("Fireball", "A ball of fire that explodes on impact", 25, "damage", 
                  {"damage": 35}, 3),
            Spell("Lightning Bolt", "A bolt of lightning that strikes the target", 30, "damage", 
                  {"damage": 40}, 5),
            Spell("Ice Shard", "A sharp shard of ice", 15, "damage", 
                  {"damage": 25}, 2),
            Spell("Thunderclap", "A deafening blast of sound", 20, "damage", 
                  {"damage": 30}, 4),
        ])
        
        # Abjuration (protection spells)
        spells.extend([
            Spell("Shield", "Creates a magical barrier", 15, "buff", 
                  {"stat": "physical_defense", "bonus": 20, "duration": 5}, 2),
            Spell("Magic Armor", "Enchants armor with magical protection", 25, "buff", 
                  {"stat": "magical_defense", "bonus": 25, "duration": 8}, 4),
            Spell("Dispel Magic", "Removes magical effects", 20, "utility", 
                  {"description": "magical dispelling"}, 6),
        ])
        
        # Conjuration (summoning spells)
        spells.extend([
            Spell("Summon Familiar", "Summons a magical familiar", 40, "utility", 
                  {"description": "a magical familiar"}, 8),
            Spell("Create Food", "Conjures food and water", 15, "utility", 
                  {"description": "food and water"}, 3),
            Spell("Teleport", "Instantly transports the caster", 50, "utility", 
                  {"description": "instant transportation"}, 10),
        ])
        
        # Divination (information spells)
        spells.extend([
            Spell("Detect Magic", "Reveals magical auras", 10, "utility", 
                  {"description": "magical detection"}, 1),
            Spell("Clairvoyance", "Allows seeing through walls", 30, "utility", 
                  {"description": "enhanced vision"}, 7),
            Spell("Identify", "Reveals item properties", 20, "utility", 
                  {"description": "item identification"}, 5),
        ])
        
        # Enchantment (mind-affecting spells)
        spells.extend([
            Spell("Charm Person", "Makes a person friendly", 25, "debuff", 
                  {"stat": "charisma", "penalty": 15, "duration": 5}, 4),
            Spell("Sleep", "Puts targets to sleep", 20, "debuff", 
                  {"stat": "agility", "penalty": 20, "duration": 3}, 3),
            Spell("Confusion", "Confuses the target", 30, "debuff", 
                  {"stat": "intelligence", "penalty": 10, "duration": 4}, 6),
        ])
        
        # Healing spells
        spells.extend([
            Spell("Cure Light Wounds", "Heals minor injuries", 20, "heal", 
                  {"healing": 30}, 2),
            Spell("Cure Serious Wounds", "Heals major injuries", 35, "heal", 
                  {"healing": 50}, 5),
            Spell("Heal", "Fully restores health", 60, "heal", 
                  {"healing": 999}, 8),
            Spell("Regeneration", "Gradually heals over time", 40, "buff", 
                  {"stat": "health", "bonus": 10, "duration": 10}, 7),
        ])
        
        return spells
    
    def learn_spell(self, player, spell_name):
        """Attempt to learn a spell."""
        spell = None
        for s in self.available_spells:
            if s.name.lower() == spell_name.lower():
                spell = s
                break
        
        if not spell:
            return False, "Spell not found"
        
        if player.level < spell.level_required:
            return False, f"Requires level {spell.level_required} to learn {spell.name}"
        
        if not hasattr(player, 'known_spells'):
            player.known_spells = []
        
        if spell.name in [s.name for s in player.known_spells]:
            return False, f"You already know {spell.name}"
        
        # Check if player has enough intelligence
        if player.stats.intelligence < 10:
            return False, "Requires at least 10 intelligence to learn spells"
        
        player.known_spells.append(spell)
        return True, f"Successfully learned {spell.name}!"
    
    def cast_spell(self, player, spell_name, target=None):
        """Cast a known spell."""
        if not hasattr(player, 'known_spells'):
            return "You don't know any spells"
        
        spell = None
        for s in player.known_spells:
            if s.name.lower() == spell_name.lower():
                spell = s
                break
        
        if not spell:
            return f"You don't know the spell '{spell_name}'"
        
        return spell.cast(player, target)
    
    def show_magic_menu(self, player):
        """Display the magic menu."""
        while True:
            print("\n=== MAGIC MENU ===")
            print(f"Known Spells: {len(getattr(player, 'known_spells', []))}")
            print(f"Available Spells: {len(self.available_spells)}")
            
            print("\nOptions:")
            print("1. Cast Spell")
            print("2. Learn New Spell")
            print("3. View Known Spells")
            print("4. View All Spells")
            print("5. Research Magic")
            print("6. Back")
            
            choice = input("\nChoose option: ")
            
            if choice == "1":
                self.cast_spell_menu(player)
            elif choice == "2":
                self.learn_spell_menu(player)
            elif choice == "3":
                self.view_known_spells(player)
            elif choice == "4":
                self.view_all_spells()
            elif choice == "5":
                self.research_magic(player)
            elif choice == "6":
                break
            else:
                print("Invalid choice!")
    
    def cast_spell_menu(self, player):
        """Menu for casting spells."""
        if not hasattr(player, 'known_spells') or not player.known_spells:
            print("You don't know any spells!")
            return
        
        print("\n=== CAST SPELL ===")
        print("Known Spells:")
        for i, spell in enumerate(player.known_spells, 1):
            print(f"{i}. {spell.name} (Mana: {spell.mana_cost}) - {spell.description}")
        
        try:
            choice = int(input("\nChoose spell to cast (or 0 to cancel): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(player.known_spells):
                spell = player.known_spells[choice]
                result = spell.cast(player)
                print(f"\n{result}")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def learn_spell_menu(self, player):
        """Menu for learning new spells."""
        print("\n=== LEARN SPELL ===")
        print("Available Spells:")
        
        learnable_spells = []
        for spell in self.available_spells:
            if not hasattr(player, 'known_spells') or spell.name not in [s.name for s in player.known_spells]:
                if player.level >= spell.level_required:
                    learnable_spells.append(spell)
        
        if not learnable_spells:
            print("No spells available to learn!")
            return
        
        for i, spell in enumerate(learnable_spells, 1):
            print(f"{i}. {spell.name} (Level {spell.level_required}) - {spell.description}")
        
        try:
            choice = int(input("\nChoose spell to learn (or 0 to cancel): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(learnable_spells):
                spell = learnable_spells[choice]
                success, message = self.learn_spell(player, spell.name)
                print(f"\n{message}")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def view_known_spells(self, player):
        """View spells the player knows."""
        if not hasattr(player, 'known_spells') or not player.known_spells:
            print("You don't know any spells!")
            return
        
        print("\n=== KNOWN SPELLS ===")
        for spell in player.known_spells:
            print(f"{spell.name} (Mana: {spell.mana_cost})")
            print(f"  {spell.description}")
            print(f"  Cast {spell.cast_count} times")
            print()
    
    def view_all_spells(self):
        """View all available spells."""
        print("\n=== ALL SPELLS ===")
        for school in self.magic_schools:
            print(f"\n{school}:")
            school_spells = [s for s in self.available_spells if school.lower() in s.description.lower()]
            for spell in school_spells:
                print(f"  {spell.name} (Level {spell.level_required}) - {spell.description}")
    
    def research_magic(self, player):
        """Research new magical knowledge."""
        if not hasattr(player, 'magic_research'):
            player.magic_research = 0
        
        print(f"\n=== MAGIC RESEARCH ===")
        print(f"Current Research Points: {player.magic_research}")
        
        if player.gold >= 50:
            choice = input("Spend 50 gold to research magic? (y/n): ")
            if choice.lower() == 'y':
                player.gold -= 50
                research_gain = random.randint(5, 15)
                player.magic_research += research_gain
                print(f"Gained {research_gain} research points!")
                
                # Chance to discover a new spell
                if random.random() < 0.3:  # 30% chance
                    new_spell = random.choice(self.available_spells)
                    success, message = self.learn_spell(player, new_spell.name)
                    if success:
                        print(f"Discovered new spell: {new_spell.name}!")
            else:
                print("Research cancelled.")
        else:
            print("Not enough gold for research (requires 50 gold).")

def generate_magic_scroll(player_level):
    """Generate a random magic scroll."""
    from magic_system import MagicSystem
    magic_system = MagicSystem()
    
    # Filter spells by level requirement
    available_spells = [spell for spell in magic_system.available_spells if spell.level_required <= player_level]
    
    if not available_spells:
        return None
    
    spell = random.choice(available_spells)
    scroll = Item(f"Scroll of {spell.name}", f"A scroll containing the {spell.name} spell", 
                  50 + spell.level_required * 10, "scroll", {"spell_name": spell.name})
    
    return scroll