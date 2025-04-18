import random
import time
from utils import clear_screen, typewriter_effect
from npc import NPC, Faction
from narrative import generate_world_event

class WorldSimulation:
    """Main class for the open-world simulation mode."""
    
    def __init__(self):
        """Initialize the simulation world."""
        self.npcs = []
        self.factions = []
        self.locations = {}
        self.resources = {}
        self.current_year = 1
        self.current_season = "Spring"
        self.event_history = []
        self.simulation_speed = 1.0  # Modifier for simulation speed
        
    def create_world(self, size="medium", complexity="medium"):
        """Create a new simulation world with the specified parameters."""
        clear_screen()
        typewriter_effect("Creating new simulation world...\n")
        
        # Determine world parameters based on size and complexity
        if size == "small":
            npc_count = random.randint(10, 20)
            faction_count = random.randint(2, 4)
            location_count = random.randint(5, 10)
        elif size == "medium":
            npc_count = random.randint(20, 40)
            faction_count = random.randint(4, 8)
            location_count = random.randint(10, 20)
        else:  # large
            npc_count = random.randint(40, 80)
            faction_count = random.randint(8, 12)
            location_count = random.randint(20, 30)
        
        # Generate locations
        location_types = ["village", "city", "forest", "mountain", "ruins", "dungeon"]
        location_name_prefixes = ["North", "South", "East", "West", "Old", "New", "Great", "Small", "High", "Low"]
        location_name_roots = ["wood", "stone", "river", "lake", "hill", "field", "fort", "haven", "bridge", "cross"]
        location_name_suffixes = ["ton", "ville", "burg", "ford", "port", "holm", "dale", "gate", "keep", "point"]
        
        for i in range(location_count):
            if random.random() < 0.3:  # 30% chance of prefix
                prefix = random.choice(location_name_prefixes)
            else:
                prefix = ""
                
            root = random.choice(location_name_roots)
            
            if random.random() < 0.7:  # 70% chance of suffix
                suffix = random.choice(location_name_suffixes)
            else:
                suffix = ""
                
            name = f"{prefix}{root.capitalize()}{suffix}"
            loc_type = random.choice(location_types)
            
            # Ensure unique name
            while name in self.locations:
                name = f"{random.choice(location_name_prefixes)}{random.choice(location_name_roots).capitalize()}{random.choice(location_name_suffixes)}"
            
            self.locations[name] = {
                "type": loc_type,
                "resources": random.randint(50, 200),
                "population": random.randint(10, 100),
                "controller": None,  # Faction that controls this location
                "prosperity": random.randint(30, 70)  # Economic prosperity level
            }
            
        print(f"Generated {len(self.locations)} locations.")
        
        # Generate NPCs
        npc_name_first = ["Arn", "Bel", "Cor", "Dav", "Ela", "Fio", "Gar", "Hel", "Ivo", "Jor", 
                        "Kal", "Lor", "Mar", "Nor", "Ora", "Pax", "Quin", "Rav", "Syl", "Tyr", 
                        "Uma", "Val", "Wex", "Xan", "Yor", "Zed"]
        npc_name_last = ["Smith", "Rivers", "Stone", "Woods", "Hill", "Field", "Storm", "Bright", 
                        "Dark", "Fire", "Frost", "Wind", "Moon", "Star", "Iron", "Gold", "Swift", 
                        "Strong", "Wise", "Brave"]
        
        for i in range(npc_count):
            first_name = random.choice(npc_name_first)
            last_name = random.choice(npc_name_last)
            name = f"{first_name} {last_name}"
            
            # Ensure unique name
            while any(npc.name == name for npc in self.npcs):
                first_name = random.choice(npc_name_first)
                last_name = random.choice(npc_name_last)
                name = f"{first_name} {last_name}"
            
            new_npc = NPC(name)
            
            # Assign location
            new_npc.location = random.choice(list(self.locations.keys()))
            
            self.npcs.append(new_npc)
            
        print(f"Generated {len(self.npcs)} NPCs.")
        
        # Create initial factions (some NPCs start as independent faction leaders)
        potential_leaders = sorted(self.npcs, 
                                key=lambda x: x.stats.charisma + x.stats.strategy + x.ambition, 
                                reverse=True)
        
        faction_count = min(faction_count, len(potential_leaders))
        
        for i in range(faction_count):
            leader = potential_leaders[i]
            faction_types = ["Kingdom", "Empire", "Republic", "Clan", "Tribe", "Order", "Guild", "Alliance"]
            faction_name = f"The {leader.name.split()[0]}'s {random.choice(faction_types)}"
            
            # Ensure unique faction name
            while any(faction.name == faction_name for faction in self.factions):
                faction_name = f"The {leader.name.split()[0]}'s {random.choice(faction_types)}"
            
            new_faction = Faction(faction_name, leader)
            self.factions.append(new_faction)
            
            # Assign initial faction members (followers of the leader)
            nearby_npcs = [npc for npc in self.npcs if npc.location == leader.location and npc != leader]
            follower_count = min(random.randint(1, 5), len(nearby_npcs))
            
            for j in range(follower_count):
                follower = nearby_npcs[j]
                new_faction.add_member(follower)
            
            # Assign control of leader's location to this faction
            self.locations[leader.location]["controller"] = new_faction
            
        print(f"Generated {len(self.factions)} initial factions.")
        
        # Set initial relationships between factions
        for i, faction1 in enumerate(self.factions):
            for faction2 in self.factions[i+1:]:
                # Randomly determine initial relationship (allied, neutral, or hostile)
                relationship = random.choice(["allied", "neutral", "hostile"])
                
                if relationship == "allied":
                    faction1.form_alliance(faction2)
                    faction2.form_alliance(faction1)
                elif relationship == "hostile":
                    faction1.declare_war(faction2)
                    faction2.declare_war(faction1)
                # neutral requires no action
        
        print("World creation complete.")
        input("\nPress Enter to continue...")
        
    def run_simulation(self, ticks=1, display_results=True):
        """Run the simulation for the specified number of ticks."""
        results = []
        
        for tick in range(ticks):
            if display_results:
                clear_screen()
                print(f"=== Simulation Year {self.current_year}, {self.current_season} ===\n")
            
            # Update NPCs
            for npc in self.npcs:
                action_result = npc.update(self)
                if display_results:
                    results.append(action_result)
            
            # Update factions
            for faction in self.factions:
                faction_result = faction.update(self)
                if display_results:
                    results.append(faction_result)
            
            # Process conflicting factions
            self.process_conflicts()
            
            # Generate random world events
            if random.random() < 0.3:  # 30% chance per tick
                event = generate_world_event(self)
                self.event_history.append(event)
                if display_results:
                    results.append(f"WORLD EVENT: {event}")
            
            # Advance time
            self.advance_time()
            
            if display_results:
                # Display a sample of results to avoid flooding the screen
                sample_size = min(10, len(results))
                sampled_results = random.sample(results, sample_size)
                
                for result in sampled_results:
                    print(f"- {result}")
                    
                print(f"\nShowing {sample_size} of {len(results)} total events this tick.")
                print(f"\nCurrent Factions: {len(self.factions)}")
                for faction in self.factions:
                    print(f"- {faction.name}: {len(faction.members)} members, {faction.territory} territory")
                
                input("\nPress Enter for next simulation tick...")
                results = []
        
        if display_results:
            clear_screen()
            print("Simulation complete.")
    
    def advance_time(self):
        """Advance the simulation time by one season."""
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        current_index = seasons.index(self.current_season)
        next_index = (current_index + 1) % 4
        
        self.current_season = seasons[next_index]
        
        # If we've gone through all seasons, advance to the next year
        if next_index == 0:
            self.current_year += 1
    
    def process_conflicts(self):
        """Process conflicts between warring factions."""
        # Group factions by enemies
        for faction in self.factions:
            for enemy in faction.enemies:
                # Simple conflict resolution
                if random.random() < 0.2:  # 20% chance of battle per tick for enemies
                    self.resolve_battle(faction, enemy)
    
    def resolve_battle(self, faction1, faction2):
        """Simulate a battle between two factions and determine the outcome."""
        # Calculate battle strength based on members, resources, and territory
        strength1 = self.calculate_faction_strength(faction1)
        strength2 = self.calculate_faction_strength(faction2)
        
        # Add random factor to make battles less predictable
        strength1 *= random.uniform(0.8, 1.2)
        strength2 *= random.uniform(0.8, 1.2)
        
        # Determine winner
        if strength1 > strength2:
            winner, loser = faction1, faction2
            advantage = strength1 / strength2
        else:
            winner, loser = faction2, faction1
            advantage = strength2 / strength1
        
        # Determine battle impact based on advantage
        if advantage > 2.0:  # Overwhelming victory
            territory_gain = min(2, loser.territory)
            resource_gain = int(loser.resources * 0.3)
            casualty_rate_winner = 0.1
            casualty_rate_loser = 0.4
        elif advantage > 1.5:  # Significant victory
            territory_gain = 1
            resource_gain = int(loser.resources * 0.2)
            casualty_rate_winner = 0.15
            casualty_rate_loser = 0.3
        else:  # Marginal victory
            territory_gain = 0
            resource_gain = int(loser.resources * 0.1)
            casualty_rate_winner = 0.2
            casualty_rate_loser = 0.2
        
        # Apply battle results
        # Territory transfer
        if territory_gain > 0:
            loser.territory = max(1, loser.territory - territory_gain)
            winner.territory += territory_gain
        
        # Resource transfer
        loser.resources = max(10, loser.resources - resource_gain)
        winner.resources += resource_gain
        
        # Handle casualties and possible defections
        self.process_battle_casualties(winner, casualty_rate_winner)
        self.process_battle_casualties(loser, casualty_rate_loser)
        
        # Possible defections from loser to winner
        self.process_defections(loser, winner, advantage)
        
        # Record the event
        battle_result = f"Battle between {winner.name} and {loser.name} results in victory for {winner.name}."
        if territory_gain > 0:
            battle_result += f" {winner.name} gains {territory_gain} territory."
        
        self.event_history.append(battle_result)
        
        # Check if loser is eliminated
        if len(loser.members) == 0:
            self.factions.remove(loser)
            self.event_history.append(f"{loser.name} has been eliminated!")
    
    def calculate_faction_strength(self, faction):
        """Calculate the military strength of a faction."""
        base_strength = len(faction.members) * 10 + faction.resources / 10 + faction.territory * 20
        
        # Add bonuses from member stats
        for member in faction.members:
            # Military stats contribute to strength
            base_strength += member.stats.strength * 2
            base_strength += member.stats.agility
            base_strength += member.stats.constitution
            
            # Leadership stats provide bonuses
            if member == faction.leader:
                base_strength += member.stats.strategy * 5
                base_strength += member.stats.charisma * 2
        
        # Ethos modifiers
        if faction.ethos == "Militaristic":
            base_strength *= 1.3
        elif faction.ethos == "Diplomatic":
            base_strength *= 0.8
        
        return base_strength
    
    def process_battle_casualties(self, faction, casualty_rate):
        """Process casualties for a faction after a battle."""
        # Calculate number of casualties
        casualty_count = max(0, int(len(faction.members) * casualty_rate))
        
        # Ensure the leader is not a casualty unless they're the only member
        potential_casualties = [m for m in faction.members if m != faction.leader]
        
        if casualty_count > 0:
            # If we need more casualties than available non-leaders
            if casualty_count > len(potential_casualties):
                # Only make the leader a casualty if they're the only one left
                if len(faction.members) == 1:
                    faction.remove_member(faction.leader)
                else:
                    # Remove all non-leader members
                    for member in potential_casualties[:]:
                        faction.remove_member(member)
            else:
                # Select random casualties from non-leaders
                casualties = random.sample(potential_casualties, casualty_count)
                for member in casualties:
                    faction.remove_member(member)
    
    def process_defections(self, loser_faction, winner_faction, advantage):
        """Process possible defections after a battle."""
        defection_chance = min(0.5, (advantage - 1.0) * 0.5)  # Cap at 50%
        
        potential_defectors = [m for m in loser_faction.members if m != loser_faction.leader]
        
        for member in potential_defectors[:]:  # Use a copy to avoid modification issues
            member_loyalty = getattr(member, 'loyalty', 10) / 20.0  # Convert to 0-0.5 scale
            
            # Members with low loyalty are more likely to defect
            if random.random() < (defection_chance / member_loyalty):
                loser_faction.remove_member(member)
                winner_faction.add_member(member)
                
                self.event_history.append(f"{member.name} has defected from {loser_faction.name} to {winner_faction.name}!")
    
    def display_world_status(self):
        """Display the current status of the simulation world."""
        clear_screen()
        print(f"=== World Status - Year {self.current_year}, {self.current_season} ===\n")
        
        print("FACTIONS:")
        for i, faction in enumerate(self.factions, 1):
            print(f"{i}. {faction.name}")
            print(f"   Leader: {faction.leader.name}")
            print(f"   Members: {len(faction.members)}")
            print(f"   Territory: {faction.territory}")
            print(f"   Resources: {faction.resources}")
            print(f"   Stability: {faction.stability}")
            print(f"   Ethos: {faction.ethos}")
            print(f"   Allies: {', '.join([a.name for a in faction.allies]) if faction.allies else 'None'}")
            print(f"   Enemies: {', '.join([e.name for e in faction.enemies]) if faction.enemies else 'None'}")
            print()
        
        print("\nLOCATIONS:")
        location_sample = list(self.locations.items())[:10]  # Show first 10 to avoid clutter
        for name, data in location_sample:
            controller = data["controller"].name if data["controller"] else "Independent"
            print(f"- {name} ({data['type']}): Population {data['population']}, Controlled by {controller}")
        
        if len(self.locations) > 10:
            print(f"...and {len(self.locations) - 10} more locations")
        
        print("\nRECENT EVENTS:")
        recent_events = self.event_history[-10:] if len(self.event_history) > 10 else self.event_history
        for event in recent_events:
            print(f"- {event}")
            
        input("\nPress Enter to continue...")
    
    def get_faction_details(self, faction_index):
        """Display detailed information about a specific faction."""
        if 0 <= faction_index < len(self.factions):
            faction = self.factions[faction_index]
            
            clear_screen()
            print(f"=== Faction Details: {faction.name} ===\n")
            
            print(f"Leader: {faction.leader.name}")
            print(f"Founded: Year {faction.founded_year if hasattr(faction, 'founded_year') else 1}")
            print(f"Ethos: {faction.ethos}")
            print(f"Territory: {faction.territory}")
            print(f"Resources: {faction.resources}")
            print(f"Stability: {faction.stability}")
            
            print("\nALLIES:")
            if faction.allies:
                for ally in faction.allies:
                    print(f"- {ally.name}")
            else:
                print("None")
                
            print("\nENEMIES:")
            if faction.enemies:
                for enemy in faction.enemies:
                    print(f"- {enemy.name}")
            else:
                print("None")
            
            print("\nMEMBERS:")
            for i, member in enumerate(faction.members, 1):
                role = "Leader" if member == faction.leader else "Member"
                print(f"{i}. {member.name} ({role})")
                if i >= 10 and len(faction.members) > 10:
                    print(f"...and {len(faction.members) - 10} more members")
                    break
            
            print("\nCONTROLLED LOCATIONS:")
            controlled = [name for name, data in self.locations.items() if data["controller"] == faction]
            if controlled:
                for location in controlled:
                    print(f"- {location}")
            else:
                print("None")
                
            input("\nPress Enter to continue...")
        else:
            print("Invalid faction index.")
            input("\nPress Enter to continue...")
    
    def to_dict(self):
        """Convert world simulation to dictionary for saving."""
        return {
            "current_year": self.current_year,
            "current_season": self.current_season,
            "npcs": [npc.to_dict() for npc in self.npcs],
            "factions": [faction.to_dict() for faction in self.factions],
            "locations": self.locations,
            "event_history": self.event_history[-100:]  # Save only the most recent 100 events
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a world simulation from dictionary data."""
        world = cls()
        
        world.current_year = data["current_year"]
        world.current_season = data["current_season"]
        world.locations = data["locations"]
        world.event_history = data["event_history"]
        
        # Load NPCs first
        for npc_data in data["npcs"]:
            world.npcs.append(NPC.from_dict(npc_data, world))
        
        # Create a lookup dictionary for NPCs
        npc_lookup = {npc.name: npc for npc in world.npcs}
        
        # Then load factions
        for faction_data in data["factions"]:
            faction = Faction.from_dict(faction_data)
            
            # Associate leader
            leader_name = faction_data["leader"]
            if leader_name in npc_lookup:
                faction.leader = npc_lookup[leader_name]
                faction.leader.is_leader = True
                faction.leader.faction = faction
                faction.leader.allegiance = faction
            
            # Add members
            for member_name in faction_data["members"]:
                if member_name in npc_lookup:
                    member = npc_lookup[member_name]
                    if member not in faction.members:
                        faction.members.append(member)
                        member.faction = faction
                        member.allegiance = faction
            
            world.factions.append(faction)
        
        # Resolve faction relationships (allies and enemies)
        faction_lookup = {faction.name: faction for faction in world.factions}
        
        for i, faction_data in enumerate(data["factions"]):
            faction = world.factions[i]
            
            # Set allies
            for ally_name in faction_data["allies"]:
                if ally_name in faction_lookup:
                    ally = faction_lookup[ally_name]
                    if ally not in faction.allies:
                        faction.allies.append(ally)
            
            # Set enemies
            for enemy_name in faction_data["enemies"]:
                if enemy_name in faction_lookup:
                    enemy = faction_lookup[enemy_name]
                    if enemy not in faction.enemies:
                        faction.enemies.append(enemy)
        
        # Update location controllers
        for location_name, location_data in world.locations.items():
            controller_name = location_data["controller"]
            if controller_name in faction_lookup:
                location_data["controller"] = faction_lookup[controller_name]
            else:
                location_data["controller"] = None
        
        return world
