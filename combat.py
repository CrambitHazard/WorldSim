import random
import time
from utils import typewriter_effect, clear_screen, format_bar

class StatusEffect:
    """Base class for status effects in combat."""
    def __init__(self, name, duration, effect_type, magnitude):
        self.name = name
        self.duration = duration
        self.effect_type = effect_type  # "buff", "debuff", "damage_over_time"
        self.magnitude = magnitude
        self.description = ""
    
    def apply(self, target):
        """Apply the status effect to a target."""
        pass
    
    def tick(self, target):
        """Process one turn of the status effect."""
        pass
    
    def remove(self, target):
        """Remove the status effect from target."""
        pass

class PoisonEffect(StatusEffect):
    def __init__(self, duration, damage_per_turn):
        super().__init__("Poison", duration, "damage_over_time", damage_per_turn)
        self.description = f"Takes {damage_per_turn} damage per turn"
    
    def apply(self, target):
        target.status_effects.append(self)
    
    def tick(self, target):
        damage = self.magnitude
        target.stats.health = max(0, target.stats.health - damage)
        self.duration -= 1
        return f"{target.name} takes {damage} poison damage!"
    
    def remove(self, target):
        if self in target.status_effects:
            target.status_effects.remove(self)

class StunEffect(StatusEffect):
    def __init__(self, duration):
        super().__init__("Stunned", duration, "debuff", 0)
        self.description = "Cannot take actions"
    
    def apply(self, target):
        target.status_effects.append(self)
        target.stunned = True
    
    def tick(self, target):
        self.duration -= 1
        if self.duration <= 0:
            self.remove(target)
        return f"{target.name} is stunned and cannot act!"
    
    def remove(self, target):
        if self in target.status_effects:
            target.status_effects.remove(self)
        target.stunned = False

class BuffEffect(StatusEffect):
    def __init__(self, name, duration, stat, bonus):
        super().__init__(name, duration, "buff", bonus)
        self.stat = stat
        self.description = f"+{bonus} to {stat}"
    
    def apply(self, target):
        target.status_effects.append(self)
        setattr(target.stats, self.stat, getattr(target.stats, self.stat) + self.magnitude)
    
    def remove(self, target):
        if self in target.status_effects:
            target.status_effects.remove(self)
            setattr(target.stats, self.stat, getattr(target.stats, self.stat) - self.magnitude)

class Combat:
    """Enhanced combat system with special abilities, status effects, and tactical combat."""
    
    def __init__(self):
        self.combat_log = []
        self.round = 0
        self.positions = {}  # For tactical positioning
        self.cover_bonuses = {}  # For cover mechanics
    
    def start_combat(self, player, enemies):
        """Start a combat encounter with multiple enemies."""
        clear_screen()
        print("=== COMBAT ENCOUNTER ===")
        
        # Initialize combat state
        all_combatants = [player] + enemies
        for combatant in all_combatants:
            combatant.status_effects = []
            combatant.stunned = False
            combatant.position = {"x": 0, "y": 0}
        
        # Set up tactical positions
        self.setup_positions(all_combatants)
        
        while True:
            self.round += 1
            print(f"\n=== ROUND {self.round} ===")
            
            # Process status effects
            self.process_status_effects(all_combatants)
            
            # Check for combat end
            if self.check_combat_end(player, enemies):
                break
            
            # Player turn
            if not player.stunned:
                self.player_turn(player, enemies)
            else:
                print(f"{player.name} is stunned and cannot act!")
            
            # Check for combat end after player turn
            if self.check_combat_end(player, enemies):
                break
            
            # Enemy turns
            for enemy in enemies:
                if enemy.stats.health > 0 and not enemy.stunned:
                    self.enemy_turn(enemy, player)
                elif enemy.stunned:
                    print(f"{enemy.name} is stunned and cannot act!")
            
            # Check for combat end after enemy turns
            if self.check_combat_end(player, enemies):
                break
            
            input("\nPress Enter to continue...")
        
        return self.end_combat(player, enemies)
    
    def setup_positions(self, combatants):
        """Set up tactical positions for combat."""
        positions = [
            {"x": 0, "y": 0},   # Front line
            {"x": 1, "y": 0},   # Right flank
            {"x": -1, "y": 0},  # Left flank
            {"x": 0, "y": 1},   # Back line
        ]
        
        for i, combatant in enumerate(combatants):
            if i < len(positions):
                combatant.position = positions[i]
            else:
                # Random position for additional combatants
                combatant.position = {
                    "x": random.randint(-2, 2),
                    "y": random.randint(0, 2)
                }
    
    def process_status_effects(self, combatants):
        """Process all status effects for the round."""
        for combatant in combatants:
            if combatant.stats.health <= 0:
                continue
                
            effects_to_remove = []
            for effect in combatant.status_effects:
                result = effect.tick(combatant)
                if result:
                    print(result)
                
                if effect.duration <= 0:
                    effects_to_remove.append(effect)
            
            # Remove expired effects
            for effect in effects_to_remove:
                effect.remove(combatant)
    
    def player_turn(self, player, enemies):
        """Handle player's turn with enhanced options."""
        print(f"\n{player.name}'s turn!")
        print(f"Health: {format_bar(player.stats.health, player.stats.max_health)} {player.stats.health}/{player.stats.max_health}")
        print(f"Mana: {format_bar(player.stats.mana, player.stats.max_mana)} {player.stats.mana}/{player.stats.max_mana}")
        
        # Show enemies
        print("\nEnemies:")
        for i, enemy in enumerate(enemies):
            if enemy.stats.health > 0:
                status = ""
                if enemy.stunned:
                    status = " [STUNNED]"
                print(f"{i+1}. {enemy.name} - HP: {enemy.stats.health}/{enemy.stats.max_health}{status}")
        
        print("\nActions:")
        print("1. Attack")
        print("2. Special Ability")
        print("3. Use Item")
        print("4. Move Position")
        print("5. Defend")
        print("6. Flee")
        
        choice = input("\nChoose action (1-6): ")
        
        if choice == "1":
            self.basic_attack(player, enemies)
        elif choice == "2":
            self.special_ability(player, enemies)
        elif choice == "3":
            self.use_item(player, enemies)
        elif choice == "4":
            self.move_position(player)
        elif choice == "5":
            self.defend(player)
        elif choice == "6":
            return self.flee_combat(player)
        else:
            print("Invalid choice. Defaulting to attack.")
            self.basic_attack(player, enemies)
    
    def basic_attack(self, attacker, targets):
        """Perform a basic attack with tactical considerations."""
        if len(targets) == 1:
            target = targets[0]
        else:
            print("Choose target:")
            for i, target in enumerate(targets):
                if target.stats.health > 0:
                    print(f"{i+1}. {target.name}")
            try:
                choice = int(input("Enter target number: ")) - 1
                target = targets[choice]
            except:
                target = targets[0]
        
        if target.stats.health <= 0:
            print("Target is already defeated!")
            return
        
        # Calculate damage with tactical modifiers
        base_damage = attacker.stats.physical_attack
        distance = self.calculate_distance(attacker, target)
        
        # Distance penalty
        if distance > 1:
            base_damage *= 0.7
        
        # Cover bonus
        cover_bonus = self.get_cover_bonus(target)
        if cover_bonus > 0:
            base_damage *= (1 - cover_bonus)
            print(f"{target.name} has cover! Damage reduced.")
        
        # Critical hit chance
        crit_chance = 0.1  # 10% base crit chance
        if random.random() < crit_chance:
            base_damage *= 2
            print("Critical hit!")
        
        damage = max(1, int(base_damage * random.uniform(0.8, 1.2)))
        target.stats.health = max(0, target.stats.health - damage)
        
        print(f"{attacker.name} attacks {target.name} for {damage} damage!")
        
        if target.stats.health <= 0:
            print(f"{target.name} is defeated!")
    
    def special_ability(self, player, enemies):
        """Use a special ability based on character class."""
        abilities = self.get_class_abilities(player.character_class)
        
        if not abilities:
            print("No special abilities available!")
            return
        
        print("\nSpecial Abilities:")
        for i, ability in enumerate(abilities):
            mana_cost = ability.get("mana_cost", 0)
            if player.stats.mana >= mana_cost:
                print(f"{i+1}. {ability['name']} (Mana: {mana_cost})")
            else:
                print(f"{i+1}. {ability['name']} (Mana: {mana_cost}) - INSUFFICIENT MANA")
        
        try:
            choice = int(input("Choose ability: ")) - 1
            if 0 <= choice < len(abilities):
                ability = abilities[choice]
                if player.stats.mana >= ability.get("mana_cost", 0):
                    self.execute_ability(player, ability, enemies)
                else:
                    print("Insufficient mana!")
            else:
                print("Invalid choice!")
        except:
            print("Invalid input!")
    
    def get_class_abilities(self, character_class):
        """Get special abilities for a character class."""
        abilities = {
            "Mage": [
                {"name": "Fireball", "mana_cost": 20, "type": "damage", "target": "all_enemies", "damage": 30},
                {"name": "Ice Shield", "mana_cost": 15, "type": "buff", "target": "self", "effect": "defense", "bonus": 10},
                {"name": "Lightning Bolt", "mana_cost": 25, "type": "damage", "target": "single", "damage": 40}
            ],
            "Warrior": [
                {"name": "Power Strike", "mana_cost": 10, "type": "damage", "target": "single", "damage": 25},
                {"name": "Battle Cry", "mana_cost": 15, "type": "buff", "target": "self", "effect": "attack", "bonus": 15},
                {"name": "Shield Wall", "mana_cost": 20, "type": "buff", "target": "self", "effect": "defense", "bonus": 20}
            ],
            "Paladin": [
                {"name": "Divine Smite", "mana_cost": 25, "type": "damage", "target": "single", "damage": 35},
                {"name": "Lay on Hands", "mana_cost": 30, "type": "heal", "target": "self", "healing": 50},
                {"name": "Divine Shield", "mana_cost": 20, "type": "buff", "target": "self", "effect": "defense", "bonus": 25}
            ],
            "Rogue": [
                {"name": "Backstab", "mana_cost": 15, "type": "damage", "target": "single", "damage": 30},
                {"name": "Poison Dart", "mana_cost": 20, "type": "status", "target": "single", "effect": "poison", "duration": 3},
                {"name": "Stealth", "mana_cost": 10, "type": "buff", "target": "self", "effect": "evasion", "bonus": 50}
            ],
            "Cleric": [
                {"name": "Heal", "mana_cost": 25, "type": "heal", "target": "self", "healing": 40},
                {"name": "Turn Undead", "mana_cost": 20, "type": "damage", "target": "all_enemies", "damage": 20},
                {"name": "Bless", "mana_cost": 15, "type": "buff", "target": "self", "effect": "attack", "bonus": 10}
            ]
        }
        
        return abilities.get(character_class, [])
    
    def execute_ability(self, caster, ability, enemies):
        """Execute a special ability."""
        mana_cost = ability.get("mana_cost", 0)
        caster.stats.mana -= mana_cost
        
        ability_type = ability.get("type", "damage")
        target_type = ability.get("target", "single")
        
        if ability_type == "damage":
            damage = ability.get("damage", 20)
            if target_type == "all_enemies":
                for enemy in enemies:
                    if enemy.stats.health > 0:
                        enemy.stats.health = max(0, enemy.stats.health - damage)
                        print(f"{caster.name}'s {ability['name']} hits {enemy.name} for {damage} damage!")
            else:
                # Single target
                if len(enemies) == 1:
                    target = enemies[0]
                else:
                    print("Choose target:")
                    for i, enemy in enumerate(enemies):
                        if enemy.stats.health > 0:
                            print(f"{i+1}. {enemy.name}")
                    try:
                        choice = int(input("Enter target number: ")) - 1
                        target = enemies[choice]
                    except:
                        target = enemies[0]
                
                target.stats.health = max(0, target.stats.health - damage)
                print(f"{caster.name}'s {ability['name']} hits {target.name} for {damage} damage!")
        
        elif ability_type == "heal":
            healing = ability.get("healing", 30)
            caster.stats.health = min(caster.stats.max_health, caster.stats.health + healing)
            print(f"{caster.name}'s {ability['name']} heals for {healing} health!")
        
        elif ability_type == "buff":
            effect = ability.get("effect", "attack")
            bonus = ability.get("bonus", 10)
            buff = BuffEffect(ability['name'], 3, effect, bonus)
            buff.apply(caster)
            print(f"{caster.name} gains {ability['name']} (+{bonus} {effect})!")
        
        elif ability_type == "status":
            effect_name = ability.get("effect", "poison")
            duration = ability.get("duration", 3)
            
            if effect_name == "poison":
                status_effect = PoisonEffect(duration, 5)
            elif effect_name == "stun":
                status_effect = StunEffect(duration)
            else:
                return
            
            # Apply to target
            if target_type == "all_enemies":
                for enemy in enemies:
                    if enemy.stats.health > 0:
                        status_effect.apply(enemy)
                        print(f"{enemy.name} is affected by {ability['name']}!")
            else:
                # Single target logic here
                pass
    
    def use_item(self, player, enemies):
        """Use an item from inventory."""
        if not player.inventory:
            print("No items in inventory!")
            return
        
        print("\nItems:")
        for i, item in enumerate(player.inventory):
            print(f"{i+1}. {item.name}")
        
        try:
            choice = int(input("Choose item (or 0 to cancel): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(player.inventory):
                item = player.inventory[choice]
                self.use_combat_item(player, item, enemies)
                player.inventory.remove(item)
            else:
                print("Invalid choice!")
        except:
            print("Invalid input!")
    
    def use_combat_item(self, player, item, enemies):
        """Use an item during combat."""
        if hasattr(item, 'combat_effect'):
            effect = item.combat_effect
            if effect == "heal":
                healing = getattr(item, 'healing_value', 20)
                player.stats.health = min(player.stats.max_health, player.stats.health + healing)
                print(f"{player.name} uses {item.name} and heals for {healing}!")
            elif effect == "mana":
                mana = getattr(item, 'mana_value', 20)
                player.stats.mana = min(player.stats.max_mana, player.stats.mana + mana)
                print(f"{player.name} uses {item.name} and restores {mana} mana!")
        else:
            print(f"{player.name} uses {item.name} but nothing happens...")
    
    def move_position(self, player):
        """Move to a different tactical position."""
        print("\nCurrent position:", player.position)
        print("Available positions:")
        positions = [
            {"x": 0, "y": 0, "name": "Front Line"},
            {"x": 1, "y": 0, "name": "Right Flank"},
            {"x": -1, "y": 0, "name": "Left Flank"},
            {"x": 0, "y": 1, "name": "Back Line"}
        ]
        
        for i, pos in enumerate(positions):
            print(f"{i+1}. {pos['name']} ({pos['x']}, {pos['y']})")
        
        try:
            choice = int(input("Choose position: ")) - 1
            if 0 <= choice < len(positions):
                player.position = positions[choice]
                print(f"{player.name} moves to {positions[choice]['name']}!")
            else:
                print("Invalid choice!")
        except:
            print("Invalid input!")
    
    def defend(self, player):
        """Take a defensive stance."""
        defense_buff = BuffEffect("Defensive Stance", 2, "physical_defense", 15)
        defense_buff.apply(player)
        print(f"{player.name} takes a defensive stance!")
    
    def flee_combat(self, player):
        """Attempt to flee from combat."""
        flee_chance = 0.6  # 60% chance to flee
        if random.random() < flee_chance:
            print(f"{player.name} successfully flees from combat!")
            return "fled"
        else:
            print(f"{player.name} fails to flee!")
            return None
    
    def enemy_turn(self, enemy, player):
        """Handle enemy turn with AI decision making."""
        print(f"\n{enemy.name}'s turn!")
        
        # Simple AI: 70% attack, 20% special ability, 10% defend
        action_roll = random.random()
        
        if action_roll < 0.7:
            self.basic_attack(enemy, [player])
        elif action_roll < 0.9:
            # Try to use special ability
            abilities = self.get_class_abilities(enemy.character_class)
            if abilities and enemy.stats.mana >= abilities[0].get("mana_cost", 0):
                self.execute_ability(enemy, abilities[0], [player])
            else:
                self.basic_attack(enemy, [player])
        else:
            # Defend
            defense_buff = BuffEffect("Defensive Stance", 2, "physical_defense", 10)
            defense_buff.apply(enemy)
            print(f"{enemy.name} takes a defensive stance!")
    
    def calculate_distance(self, attacker, target):
        """Calculate distance between two combatants."""
        dx = attacker.position["x"] - target.position["x"]
        dy = attacker.position["y"] - target.position["y"]
        return (dx**2 + dy**2)**0.5
    
    def get_cover_bonus(self, target):
        """Calculate cover bonus for a target."""
        # Simple cover system based on position
        if target.position["y"] > 0:  # Back line has cover
            return 0.3
        return 0
    
    def check_combat_end(self, player, enemies):
        """Check if combat should end."""
        if player.stats.health <= 0:
            return True
        
        alive_enemies = [e for e in enemies if e.stats.health > 0]
        if not alive_enemies:
            return True
        
        return False
    
    def end_combat(self, player, enemies):
        """End combat and calculate results."""
        if player.stats.health <= 0:
            print(f"\n{player.name} has been defeated!")
            return "defeat"
        
        alive_enemies = [e for e in enemies if e.stats.health > 0]
        if not alive_enemies:
            print(f"\nVictory! All enemies defeated!")
            
            # Calculate experience and loot
            total_exp = sum(enemy.level * 10 for enemy in enemies)
            player.gain_exp(total_exp)
            
                    # Generate loot
        from items import generate_random_item
        loot = generate_random_item(player.level)
        player.add_to_inventory(loot)
        
        # Track achievements
        from achievements import track_player_stats
        track_player_stats(player, "combat_wins", 1)
        
        print(f"Gained {total_exp} experience!")
        print(f"Found {loot.name}!")
        
        return "victory"
        
        return "ongoing"
