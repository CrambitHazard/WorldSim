import random
from utils import typewriter_effect, clear_screen

class Combat:
    """Handles combat encounters between entities."""
    
    def __init__(self, player, enemies):
        """Initialize a combat encounter."""
        self.player = player
        self.enemies = enemies if isinstance(enemies, list) else [enemies]
        self.turn_order = []
        self.round = 1
        self.active = True
        self.messages = []
        
    def start(self):
        """Start the combat encounter."""
        self.determine_turn_order()
        self.display_combat_start()
        
        while self.active:
            self.process_round()
            
            # Check if combat should end
            if not self.enemies or self.player.stats.health <= 0:
                self.active = False
                
        # Combat has ended
        self.end_combat()
    
    def determine_turn_order(self):
        """Determine the order in which combatants act based on speed."""
        # Add player and enemies to the turn order
        self.turn_order = [self.player] + self.enemies
        
        # Sort by speed, higher goes first
        self.turn_order.sort(key=lambda x: x.stats.speed, reverse=True)
    
    def display_combat_start(self):
        """Display the start of combat information."""
        clear_screen()
        enemy_names = ", ".join([enemy.name for enemy in self.enemies])
        typewriter_effect(f"Combat started: {self.player.name} vs {enemy_names}")
        
        print("\nTurn order:")
        for i, entity in enumerate(self.turn_order, 1):
            print(f"{i}. {entity.name} (Speed: {entity.stats.speed})")
            
        input("\nPress Enter to begin combat...")
    
    def process_round(self):
        """Process a single round of combat where each entity takes a turn."""
        clear_screen()
        print(f"=== Round {self.round} ===\n")
        
        # Display status
        self.display_combat_status()
        
        # Process each combatant's turn
        for entity in self.turn_order[:]:  # Create a copy to iterate over
            if entity.stats.health <= 0:
                continue  # Skip dead entities
                
            if entity == self.player:
                self.player_turn()
            else:
                self.enemy_turn(entity)
                
            # Check if combat should end after each turn
            if not self.enemies or self.player.stats.health <= 0:
                self.active = False
                break
        
        self.round += 1
        
        # Display messages from this round
        if self.messages:
            print("\n".join(self.messages))
            self.messages = []
            
        if self.active:
            input("\nPress Enter for next round...")
    
    def display_combat_status(self):
        """Display the current status of all combatants."""
        # Player status
        print(f"{self.player.name}: HP {self.player.stats.health}/{self.player.stats.max_health} | MP {self.player.stats.mana}/{self.player.stats.max_mana}")
        
        print("\nEnemies:")
        for enemy in self.enemies:
            print(f"{enemy.name}: HP {enemy.stats.health}/{enemy.stats.max_health}")
        print()
    
    def player_turn(self):
        """Handle the player's turn in combat."""
        typewriter_effect(f"It's {self.player.name}'s turn!")
        print("\nChoose your action:")
        print("1. Attack")
        print("2. Cast Spell")
        print("3. Use Item")
        print("4. Flee")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == "1":
            # Attack option
            if len(self.enemies) == 1:
                target = self.enemies[0]
            else:
                # Choose which enemy to attack
                print("\nChoose a target:")
                for i, enemy in enumerate(self.enemies, 1):
                    print(f"{i}. {enemy.name} (HP: {enemy.stats.health}/{enemy.stats.max_health})")
                
                target_choice = input(f"\nEnter target (1-{len(self.enemies)}): ")
                try:
                    target_index = int(target_choice) - 1
                    if 0 <= target_index < len(self.enemies):
                        target = self.enemies[target_index]
                    else:
                        target = random.choice(self.enemies)
                        self.messages.append(f"Invalid target. Randomly attacking {target.name}.")
                except ValueError:
                    target = random.choice(self.enemies)
                    self.messages.append(f"Invalid input. Randomly attacking {target.name}.")
            
            # Perform attack
            self.attack(self.player, target)
            
        elif choice == "2":
            # Cast spell option (simplified for example)
            spells = ["Fireball", "Ice Shard", "Healing Light"]
            print("\nChoose a spell:")
            for i, spell in enumerate(spells, 1):
                print(f"{i}. {spell}")
                
            spell_choice = input(f"\nEnter spell (1-{len(spells)}): ")
            try:
                spell_index = int(spell_choice) - 1
                if 0 <= spell_index < len(spells):
                    spell = spells[spell_index]
                    
                    # Select target for the spell
                    if spell == "Healing Light":
                        # Healing spell targets self
                        self.cast_spell(self.player, self.player, spell)
                    else:
                        # Offensive spell targets enemy
                        if len(self.enemies) == 1:
                            target = self.enemies[0]
                        else:
                            print("\nChoose a target:")
                            for i, enemy in enumerate(self.enemies, 1):
                                print(f"{i}. {enemy.name} (HP: {enemy.stats.health}/{enemy.stats.max_health})")
                            
                            target_choice = input(f"\nEnter target (1-{len(self.enemies)}): ")
                            try:
                                target_index = int(target_choice) - 1
                                if 0 <= target_index < len(self.enemies):
                                    target = self.enemies[target_index]
                                else:
                                    target = random.choice(self.enemies)
                                    self.messages.append(f"Invalid target. Randomly targeting {target.name}.")
                            except ValueError:
                                target = random.choice(self.enemies)
                                self.messages.append(f"Invalid input. Randomly targeting {target.name}.")
                        
                        self.cast_spell(self.player, target, spell)
                else:
                    self.messages.append("Invalid spell choice. Turn skipped.")
            except ValueError:
                self.messages.append("Invalid input. Turn skipped.")
                
        elif choice == "3":
            # Use item option (simplified)
            self.messages.append("No items available. Turn skipped.")
            
        elif choice == "4":
            # Flee option
            flee_chance = 0.3 + (self.player.stats.agility / 100)  # Base 30% + agility bonus
            if random.random() < flee_chance:
                self.messages.append(f"{self.player.name} successfully fled from combat!")
                self.active = False
            else:
                self.messages.append(f"{self.player.name} failed to flee!")
        
        else:
            self.messages.append("Invalid choice. Turn skipped.")
    
    def enemy_turn(self, enemy):
        """Handle an enemy's turn in combat."""
        typewriter_effect(f"\n{enemy.name}'s turn!")
        
        # Simple AI: Always attack the player
        self.attack(enemy, self.player)
    
    def attack(self, attacker, target):
        """Process a physical attack."""
        # Calculate hit chance
        base_hit_chance = 0.8  # 80% base hit chance
        hit_chance = base_hit_chance + (attacker.stats.perception / 200) - (target.stats.agility / 200)
        hit_chance = max(0.1, min(0.95, hit_chance))  # Clamp between 10% and 95%
        
        if random.random() <= hit_chance:
            # Hit! Calculate damage
            base_damage = attacker.stats.physical_attack
            defense = target.stats.physical_defense
            
            # Add some randomness (80%-120% of base damage)
            damage_multiplier = random.uniform(0.8, 1.2)
            
            # Critical hit chance based on agility
            crit_chance = attacker.stats.agility / 200  # 0-20% based on agility
            is_critical = random.random() <= crit_chance
            
            if is_critical:
                damage_multiplier *= 2  # Double damage on critical
                
            # Calculate final damage
            damage = max(1, int((base_damage * damage_multiplier) - (defense * 0.5)))
            
            # Apply damage
            target.stats.health = max(0, target.stats.health - damage)
            
            # Create message
            message = f"{attacker.name} attacks {target.name} for {damage} damage"
            if is_critical:
                message += " (CRITICAL HIT!)"
                
            # Check if target is defeated
            if target.stats.health <= 0:
                message += f"\n{target.name} has been defeated!"
                
                # Remove defeated enemy from the combat
                if target in self.enemies:
                    self.enemies.remove(target)
                    
                    # Give player experience and rewards
                    if attacker == self.player:
                        exp_gain = 10 * target.level
                        self.player.gain_exp(exp_gain)
                        message += f"\n{self.player.name} gained {exp_gain} experience!"
        else:
            # Miss
            message = f"{attacker.name} attacks {target.name} but misses!"
        
        self.messages.append(message)
    
    def cast_spell(self, caster, target, spell):
        """Process a spell cast."""
        # Check if caster has enough mana
        mana_cost = {"Fireball": 10, "Ice Shard": 7, "Healing Light": 15}.get(spell, 5)
        
        if caster.stats.mana < mana_cost:
            self.messages.append(f"{caster.name} doesn't have enough mana to cast {spell}!")
            return
        
        # Consume mana
        caster.stats.mana -= mana_cost
        
        # Process spell effects
        if spell == "Fireball":
            # Offensive fire spell
            base_damage = caster.stats.magical_attack * 1.2
            defense = target.stats.magical_defense
            
            # Add some randomness
            damage_multiplier = random.uniform(0.9, 1.3)
            
            # Calculate final damage
            damage = max(1, int((base_damage * damage_multiplier) - (defense * 0.3)))
            
            # Apply damage
            target.stats.health = max(0, target.stats.health - damage)
            
            message = f"{caster.name} casts Fireball at {target.name} for {damage} magical damage!"
            
            # Check if target is defeated
            if target.stats.health <= 0:
                message += f"\n{target.name} has been defeated!"
                
                # Remove defeated enemy from the combat
                if target in self.enemies:
                    self.enemies.remove(target)
                    
                    # Give player experience and rewards
                    if caster == self.player:
                        exp_gain = 10 * target.level
                        self.player.gain_exp(exp_gain)
                        message += f"\n{self.player.name} gained {exp_gain} experience!"
        
        elif spell == "Ice Shard":
            # Offensive ice spell with chance to slow
            base_damage = caster.stats.magical_attack * 0.9
            defense = target.stats.magical_defense
            
            # Add some randomness
            damage_multiplier = random.uniform(0.8, 1.2)
            
            # Calculate final damage
            damage = max(1, int((base_damage * damage_multiplier) - (defense * 0.3)))
            
            # Apply damage
            target.stats.health = max(0, target.stats.health - damage)
            
            message = f"{caster.name} casts Ice Shard at {target.name} for {damage} magical damage!"
            
            # Chance to reduce enemy speed
            if random.random() < 0.3:  # 30% chance
                target.stats.speed = max(1, int(target.stats.speed * 0.8))  # Reduce speed by 20%
                message += f"\n{target.name}'s speed is reduced!"
            
            # Check if target is defeated
            if target.stats.health <= 0:
                message += f"\n{target.name} has been defeated!"
                
                # Remove defeated enemy from the combat
                if target in self.enemies:
                    self.enemies.remove(target)
                    
                    # Give player experience and rewards
                    if caster == self.player:
                        exp_gain = 10 * target.level
                        self.player.gain_exp(exp_gain)
                        message += f"\n{self.player.name} gained {exp_gain} experience!"
        
        elif spell == "Healing Light":
            # Healing spell
            heal_amount = int(caster.stats.magical_attack * 0.8 + caster.stats.wisdom * 0.5)
            
            # Add some randomness
            heal_multiplier = random.uniform(0.8, 1.2)
            heal_amount = int(heal_amount * heal_multiplier)
            
            # Apply healing (not exceeding max health)
            old_health = target.stats.health
            target.stats.health = min(target.stats.max_health, target.stats.health + heal_amount)
            actual_healing = target.stats.health - old_health
            
            message = f"{caster.name} casts Healing Light on {target.name}, restoring {actual_healing} health!"
        
        self.messages.append(message)
    
    def end_combat(self):
        """Handle the end of combat."""
        clear_screen()
        print("=== Combat Ended ===\n")
        
        if not self.enemies:
            typewriter_effect("Victory! All enemies have been defeated.")
            
            # Calculate total rewards
            exp_total = sum(10 * enemy.level for enemy in self.enemies)
            gold_total = sum(random.randint(5, 10) * enemy.level for enemy in self.enemies)
            
            self.player.gold += gold_total
            
            print(f"\nRewards:")
            print(f"- Experience: {exp_total}")
            print(f"- Gold: {gold_total}")
            
        elif self.player.stats.health <= 0:
            typewriter_effect("Defeat! You have been defeated in combat.")
            print("\nYou wake up later, having lost some gold but thankfully still alive.")
            
            # Lose some gold as penalty
            gold_loss = int(self.player.gold * 0.2)  # Lose 20% of gold
            self.player.gold = max(0, self.player.gold - gold_loss)
            
            # Restore some health
            self.player.stats.health = max(1, int(self.player.stats.max_health * 0.3))
            
            print(f"\nPenalties:")
            print(f"- Lost {gold_loss} gold")
            print(f"- Health restored to {self.player.stats.health}")
            
        else:
            typewriter_effect("You fled from combat.")
            
        input("\nPress Enter to continue...")
