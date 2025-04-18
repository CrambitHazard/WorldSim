import random
from character import Character, Stats

class NPC(Character):
    """
    NPC class for simulation mode, with additional attributes for 
    autonomous behavior in open-world simulation.
    """
    def __init__(self, name, race=None, character_class=None):
        super().__init__(name, race, character_class)
        
        # Simulation-specific attributes
        self.faction = None
        self.resources = random.randint(50, 200)
        self.territory = 1  # Starting territory size
        self.is_leader = False
        self.allegiance = None  # The faction this NPC is loyal to
        self.happiness = random.randint(40, 80)  # 0-100 scale
        
        # Relationships with other NPCs/factions
        self.allies = []
        self.enemies = []
        self.relationships = {}  # {npc_id: relationship_value}
        
        # Personality traits (0-100 scale)
        self.ambition = random.randint(10, 100)
        self.aggression = random.randint(10, 100)
        self.altruism = random.randint(10, 100)
        
        # Goals and current action
        self.goals = []
        self.current_action = "idle"
        self.action_progress = 0  # Progress toward completing current action
        
    def decide_action(self, world):
        """
        Determine what action the NPC should take based on their current state,
        personality, and world conditions.
        """
        # Emergency actions (take priority)
        if self.stats.health < self.stats.max_health * 0.3:
            return "seek_healing"
        
        if self.resources < 20:
            return "gather_resources"
        
        leadership = (self.stats.charisma + self.stats.wisdom) / 2
        
        # Consider forming/joining a faction
        if not self.faction and not self.allegiance:
            if self.stats.leadership > 15 and self.resources > 100 and self.ambition > 70:
                return "form_faction"
            elif random.random() < 0.3:  # 30% chance if no emergency
                return "seek_faction"
        
        # Leadership actions
        if self.is_leader:
            if self.territory < 3 and self.resources > 150:
                return "expand_territory"
            
            if len(self.allies) < 2 and random.random() < 0.4:
                return "seek_alliance"
                
            if self.aggression > 70 and self.resources > 200:
                return "plan_attack"
        
        # Regular NPC actions
        if self.happiness < 30 and self.stats.rebelliousness > 15:
            return "plot_rebellion"
        
        if random.random() < 0.2:  # 20% chance of looking for combat
            return "seek_combat"
        
        if self.resources < 50:
            return "gather_resources"
            
        if random.random() < 0.1:  # 10% chance of exploring
            return "explore"
        
        # Default actions
        options = ["train_skills", "socialize", "craft_item", "idle"]
        weights = [0.3, 0.3, 0.2, 0.2]  # 30% train, 30% socialize, 20% craft, 20% idle
        
        return random.choices(options, weights)[0]
    
    def execute_action(self, action, world):
        """
        Execute the given action and return the result.
        """
        self.current_action = action
        result = f"{self.name} is {action.replace('_', ' ')}ing"
        
        # Implement action logic
        if action == "gather_resources":
            gained = random.randint(10, 30)
            self.resources += gained
            result = f"{self.name} gathered {gained} resources. Total: {self.resources}"
            
        elif action == "train_skills":
            # Improve a random stat
            stat_options = ["strength", "intelligence", "wisdom", 
                          "constitution", "agility", "perception", "charisma"]
            stat = random.choice(stat_options)
            gain = random.uniform(0.1, 0.5)
            current = getattr(self.stats, stat)
            setattr(self.stats, stat, current + gain)
            result = f"{self.name} trained {stat}, gaining {gain:.1f} points"
            
        elif action == "form_faction":
            # Logic for creating a new faction
            faction_name = f"{self.name}'s {random.choice(['Kingdom', 'Clan', 'Guild', 'Order'])}"
            new_faction = Faction(faction_name, self)
            world.factions.append(new_faction)
            self.faction = new_faction
            self.is_leader = True
            self.allegiance = new_faction
            result = f"{self.name} formed a new faction: {faction_name}"
            
        elif action == "expand_territory":
            # Logic for territory expansion
            success_chance = (self.stats.strategy + self.resources/100) / 30
            if random.random() < success_chance:
                self.territory += 1
                self.resources -= 50
                result = f"{self.name} expanded territory to {self.territory} units"
            else:
                self.resources -= 20
                result = f"{self.name} failed to expand territory and lost 20 resources"
        
        # More action implementations would go here...
        
        return result
    
    def update(self, world):
        """Update the NPC's state for one simulation tick."""
        # Decide and execute action
        action = self.decide_action(world)
        result = self.execute_action(action, world)
        
        # Natural resource regeneration (small amount)
        if random.random() < 0.3:  # 30% chance
            self.resources += random.randint(1, 5)
        
        # Return the result of the NPC's action
        return result
    
    def get_relationship(self, other_npc):
        """Get relationship value with another NPC."""
        if other_npc.name in self.relationships:
            return self.relationships[other_npc.name]
        else:
            # Initialize new relationship with slight randomness
            base_value = 0
            
            # Racial affinities (optional)
            if self.race == other_npc.race:
                base_value += 10
                
            # Class affinities
            if self.character_class == other_npc.character_class:
                base_value += 5
                
            # Random factor (-10 to +10)
            random_factor = random.randint(-10, 10)
            
            value = base_value + random_factor
            self.relationships[other_npc.name] = value
            return value
    
    def modify_relationship(self, other_npc, amount):
        """Change relationship value with another NPC."""
        current = self.get_relationship(other_npc)
        new_value = max(-100, min(100, current + amount))  # Clamp between -100 and 100
        self.relationships[other_npc.name] = new_value
        
        # Update allies/enemies lists
        if new_value >= 50 and other_npc not in self.allies:
            self.allies.append(other_npc)
            if other_npc in self.enemies:
                self.enemies.remove(other_npc)
        elif new_value <= -50 and other_npc not in self.enemies:
            self.enemies.append(other_npc)
            if other_npc in self.allies:
                self.allies.remove(other_npc)
                
        return f"Relationship with {other_npc.name} changed by {amount} to {new_value}"
    
    def to_dict(self):
        """Convert NPC to dictionary for saving."""
        data = super().to_dict()
        data.update({
            "faction": self.faction.name if self.faction else None,
            "resources": self.resources,
            "territory": self.territory,
            "is_leader": self.is_leader,
            "allegiance": self.allegiance.name if self.allegiance else None,
            "happiness": self.happiness,
            "allies": [ally.name for ally in self.allies],
            "enemies": [enemy.name for enemy in self.enemies],
            "relationships": self.relationships,
            "ambition": self.ambition,
            "aggression": self.aggression,
            "altruism": self.altruism,
            "current_action": self.current_action
        })
        return data
    
    @classmethod
    def from_dict(cls, data, world=None):
        """Create an NPC from dictionary data."""
        npc = super().from_dict(data)
        
        npc.resources = data["resources"]
        npc.territory = data["territory"]
        npc.is_leader = data["is_leader"]
        npc.happiness = data["happiness"]
        npc.relationships = data["relationships"]
        npc.ambition = data["ambition"]
        npc.aggression = data["aggression"]
        npc.altruism = data["altruism"]
        npc.current_action = data["current_action"]
        
        # Faction and allegiance need to be resolved after all NPCs and factions are loaded
        # This would typically be handled by the world loading system
        
        return npc


class Faction:
    """
    Represents a group of NPCs under a leadership structure.
    Factions can control territory, wage war, and form alliances.
    """
    def __init__(self, name, leader=None):
        self.name = name
        self.leader = leader
        self.members = []
        if leader:
            self.members.append(leader)
        
        self.territory = 0
        self.resources = 0
        self.allies = []
        self.enemies = []
        self.reputation = 0  # General world reputation
        
        # Faction characteristics
        self.ethos = random.choice(["Militaristic", "Diplomatic", "Isolationist", 
                                  "Expansionist", "Religious", "Trade-focused"])
        self.stability = random.randint(50, 100)  # Internal stability
        
        # Update the leader's status
        if leader:
            leader.faction = self
            leader.is_leader = True
            leader.allegiance = self
            self.territory = leader.territory
            self.resources = int(leader.resources * 0.5)  # Leader contributes half their resources
            leader.resources = int(leader.resources * 0.5)  # Leader keeps half
    
    def add_member(self, npc):
        """Add an NPC to the faction."""
        if npc not in self.members:
            self.members.append(npc)
            npc.allegiance = self
            npc.faction = self
            
            # Contribute some resources to the faction
            contribution = int(npc.resources * 0.3)  # 30% tax
            npc.resources -= contribution
            self.resources += contribution
            
            return f"{npc.name} has joined {self.name}"
        return f"{npc.name} is already a member of {self.name}"
    
    def remove_member(self, npc):
        """Remove an NPC from the faction."""
        if npc in self.members:
            self.members.remove(npc)
            
            # Handle leadership change if the leader is leaving
            if npc == self.leader:
                if self.members:
                    # Find the most suitable new leader
                    new_leader = max(self.members, 
                                    key=lambda m: m.stats.charisma + m.stats.strategy)
                    self.leader = new_leader
                    new_leader.is_leader = True
                    return f"{npc.name} has left {self.name}. {new_leader.name} is the new leader."
                else:
                    # Faction is dissolved
                    return f"{self.name} has been dissolved as all members have left."
            
            npc.allegiance = None
            npc.faction = None
            return f"{npc.name} has left {self.name}"
        return f"{npc.name} is not a member of {self.name}"
    
    def declare_war(self, other_faction):
        """Declare war on another faction."""
        if other_faction in self.allies:
            self.allies.remove(other_faction)
        
        if other_faction not in self.enemies:
            self.enemies.append(other_faction)
            
            # Update relationships between members
            for member in self.members:
                for enemy in other_faction.members:
                    member.modify_relationship(enemy, -30)
            
            return f"{self.name} has declared war on {other_faction.name}!"
        return f"{self.name} is already at war with {other_faction.name}"
    
    def form_alliance(self, other_faction):
        """Form an alliance with another faction."""
        if other_faction in self.enemies:
            self.enemies.remove(other_faction)
        
        if other_faction not in self.allies:
            self.allies.append(other_faction)
            
            # Update relationships between members
            for member in self.members:
                for ally in other_faction.members:
                    member.modify_relationship(ally, 20)
            
            return f"{self.name} has formed an alliance with {other_faction.name}!"
        return f"{self.name} is already allied with {other_faction.name}"
    
    def collect_taxes(self):
        """Collect taxes from faction members."""
        total_collected = 0
        for member in self.members:
            if member != self.leader:  # Leader doesn't pay taxes
                tax_amount = int(member.resources * 0.1)  # 10% tax rate
                if tax_amount > 0:
                    member.resources -= tax_amount
                    total_collected += tax_amount
                    
                    # Happiness impact
                    member.happiness -= 5  # Taxes reduce happiness
        
        self.resources += total_collected
        return f"{self.name} collected {total_collected} resources in taxes"
    
    def distribute_resources(self, amount_per_member):
        """Distribute resources to faction members."""
        if amount_per_member * len(self.members) > self.resources:
            return f"Not enough resources to distribute {amount_per_member} to each member"
        
        total_distributed = 0
        for member in self.members:
            member.resources += amount_per_member
            total_distributed += amount_per_member
            
            # Happiness impact
            member.happiness += 10  # Resource distribution increases happiness
        
        self.resources -= total_distributed
        return f"{self.name} distributed {total_distributed} resources to members"
    
    def update(self, world):
        """Update the faction for one simulation tick."""
        results = []
        
        # Check for internal instability
        if self.stability < 30:
            # Possible rebellion or dissolution
            if random.random() < 0.2:  # 20% chance of rebellion
                rebel_chance = lambda m: (m.stats.rebelliousness / 20) * (100 - m.happiness) / 100
                potential_rebels = [m for m in self.members if rebel_chance(m) > 0.3]
                
                if potential_rebels:
                    rebel = random.choice(potential_rebels)
                    results.append(f"{rebel.name} is rebelling against {self.name}!")
                    
                    # Rebellion mechanics would go here
                    if random.random() < 0.5:  # 50% chance of successful rebellion
                        if rebel.stats.charisma > self.leader.stats.charisma:
                            # Leadership overthrow
                            old_leader = self.leader
                            old_leader.is_leader = False
                            self.leader = rebel
                            rebel.is_leader = True
                            results.append(f"{rebel.name} has overthrown {old_leader.name} and is now leader of {self.name}!")
                        else:
                            # Failed overthrow - rebel leaves
                            self.remove_member(rebel)
                            results.append(f"{rebel.name}'s rebellion failed and they have been exiled from {self.name}")
        
        # Tax collection (not every tick)
        if random.random() < 0.3:  # 30% chance
            results.append(self.collect_taxes())
        
        # Resource distribution (occasional)
        if self.resources > len(self.members) * 20 and random.random() < 0.2:
            amount = min(20, int(self.resources / (len(self.members) * 2)))
            results.append(self.distribute_resources(amount))
        
        # Faction strategy based on ethos
        if self.ethos == "Expansionist" and self.resources > 100:
            self.territory += 1
            self.resources -= 50
            results.append(f"{self.name} expanded its territory to {self.territory} units")
            
        elif self.ethos == "Militaristic" and self.resources > 150:
            # Potential for starting conflicts
            if not self.enemies and random.random() < 0.2:
                potential_targets = [f for f in world.factions if f != self and f not in self.allies]
                if potential_targets:
                    target = random.choice(potential_targets)
                    results.append(self.declare_war(target))
            
        elif self.ethos == "Diplomatic" and random.random() < 0.3:
            # Look for alliances
            potential_allies = [f for f in world.factions if f != self and f not in self.allies and f not in self.enemies]
            if potential_allies:
                ally = random.choice(potential_allies)
                results.append(self.form_alliance(ally))
        
        # Natural resource generation based on territory
        resource_gain = self.territory * random.randint(5, 10)
        self.resources += resource_gain
        
        # Stability adjustments
        if len(self.members) > 10:
            self.stability -= 1  # Larger factions are harder to control
        
        if len(self.enemies) > 0:
            self.stability -= 2  # War decreases stability
            
        if self.resources < len(self.members) * 10:
            self.stability -= 3  # Resource shortages decrease stability
        
        # Natural stability recovery
        if random.random() < 0.5:  # 50% chance
            self.stability = min(100, self.stability + 1)
        
        return "\n".join(results) if results else f"{self.name} continues normal operations"
    
    def to_dict(self):
        """Convert faction to dictionary for saving."""
        return {
            "name": self.name,
            "leader": self.leader.name if self.leader else None,
            "members": [member.name for member in self.members],
            "territory": self.territory,
            "resources": self.resources,
            "allies": [ally.name for ally in self.allies],
            "enemies": [enemy.name for enemy in self.enemies],
            "reputation": self.reputation,
            "ethos": self.ethos,
            "stability": self.stability
        }
    
    @classmethod
    def from_dict(cls, data, npcs=None):
        """
        Create a faction from dictionary data.
        Requires a dictionary of NPCs to resolve references.
        """
        faction = cls(data["name"])
        faction.territory = data["territory"]
        faction.resources = data["resources"]
        faction.reputation = data["reputation"]
        faction.ethos = data["ethos"]
        faction.stability = data["stability"]
        
        # Leader and members need to be resolved after all NPCs are loaded
        # This would typically be handled by the world loading system
        
        return faction
