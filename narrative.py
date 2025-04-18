import random
from utils import typewriter_effect, clear_screen

# This module provides text generation functions for the game
# In a production environment, this could interface with a language model API

class Quest:
    """Represents a quest that can be assigned to and completed by the player."""
    
    def __init__(self, title, description, objective_type, objective_count, reward_exp, reward_gold):
        self.title = title
        self.description = description
        self.objective_type = objective_type  # e.g., "kill", "collect", "explore"
        self.objective_count = objective_count  # How many to kill/collect/etc.
        self.current_progress = 0
        self.completed = False
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.reward_items = []
    
    def update_progress(self, amount=1):
        """Update progress toward the quest objective."""
        if self.completed:
            return False
            
        self.current_progress += amount
        if self.current_progress >= self.objective_count:
            self.completed = True
            return True
        return False
    
    def get_progress_text(self):
        """Get a text description of current quest progress."""
        return f"{self.current_progress}/{self.objective_count} {self.objective_type}"
    
    def to_dict(self):
        """Convert quest to dictionary for saving."""
        return {
            "title": self.title,
            "description": self.description,
            "objective_type": self.objective_type,
            "objective_count": self.objective_count,
            "current_progress": self.current_progress,
            "completed": self.completed,
            "reward_exp": self.reward_exp,
            "reward_gold": self.reward_gold,
            "reward_items": [item.to_dict() for item in self.reward_items]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a quest from dictionary data."""
        from items import Item  # Import here to avoid circular imports
        
        quest = cls(
            data["title"],
            data["description"],
            data["objective_type"],
            data["objective_count"],
            data["reward_exp"],
            data["reward_gold"]
        )
        
        quest.current_progress = data["current_progress"]
        quest.completed = data["completed"]
        
        # Load reward items
        quest.reward_items = [Item.from_dict(item_data) for item_data in data["reward_items"]]
        
        return quest


def generate_quest_description(location, theme=None):
    """
    Generate a quest description based on location and optional theme.
    This simulates what an ML model might generate.
    """
    themes = theme or random.choice([
        "exploration", "combat", "rescue", "collection", 
        "mystery", "diplomacy", "corruption", "ancient power"
    ])
    
    descriptions = {
        "exploration": [
            f"Rumors speak of an ancient ruin near {location} that holds treasures beyond imagination.",
            f"The elders of {location} say that a hidden cave system could lead to a forgotten civilization.",
            f"A mysterious forest outside {location} has been changing, revealing paths that weren't there before."
        ],
        "combat": [
            f"{location} has been plagued by bandits attacking trade caravans. The merchants need help.",
            f"A powerful creature has made its lair near {location}, threatening the local population.",
            f"The garrison at {location} is undermanned and needs assistance repelling an imminent attack."
        ],
        "rescue": [
            f"A child from {location} wandered into the wilderness and hasn't returned. Time is of the essence.",
            f"Slavers have kidnapped several residents of {location}. Their hideout is said to be nearby.",
            f"An important diplomat has gone missing on their way to {location}. Foul play is suspected."
        ],
        "collection": [
            f"An alchemist in {location} needs rare herbs that only grow in dangerous areas nearby.",
            f"The blacksmith of {location} has received a special commission but needs rare ore.",
            f"A collector in {location} will pay handsomely for ancient artifacts from the region."
        ],
        "mystery": [
            f"Strange occurrences have been reported in {location}. Residents speak of lights in the sky.",
            f"People in {location} have been acting oddly, as if under some kind of influence.",
            f"A series of unexplained deaths has {location} on edge. Some whisper of a curse."
        ],
        "diplomacy": [
            f"Two factions in {location} are at each other's throats. Conflict seems inevitable without intervention.",
            f"An important treaty is at risk of failing without a neutral mediator in {location}.",
            f"The leadership of {location} is in dispute, with multiple claimants threatening civil unrest."
        ],
        "corruption": [
            f"Evidence suggests officials in {location} are involved in a smuggling operation.",
            f"The well-respected leader of {location} may be hiding a dark secret.",
            f"Tax money in {location} is disappearing, and the poor are suffering for it."
        ],
        "ancient power": [
            f"Locals of {location} speak of ancient magic awakening in the ruins nearby.",
            f"A scholar in {location} has discovered references to a powerful artifact buried in the region.",
            f"Strange energy emanates from beneath {location}, causing magical anomalies."
        ]
    }
    
    return random.choice(descriptions[themes])


def generate_quest(player_level, location):
    """Generate a complete random quest appropriate for the player's level."""
    quest_types = {
        "kill": ["Extermination", "Pest Control", "Cleansing", "Hunt"],
        "collect": ["Gathering", "Collection", "Harvesting", "Scavenging"],
        "explore": ["Exploration", "Scouting", "Mapping", "Survey"],
        "deliver": ["Delivery", "Courier", "Transport", "Shipment"],
        "escort": ["Protection", "Escort", "Safeguard", "Convoy"]
    }
    
    objective_type = random.choice(list(quest_types.keys()))
    title_prefix = random.choice(quest_types[objective_type])
    
    # Generate targets based on quest type
    targets = {
        "kill": ["Wolves", "Bandits", "Skeletons", "Goblins", "Cultists", "Spiders", "Zombies", "Giants"],
        "collect": ["Herbs", "Ore", "Pelts", "Crystals", "Essences", "Books", "Relics", "Ingredients"],
        "explore": ["Ruins", "Caves", "Forest", "Tombs", "Towers", "Tunnels", "Shipwrecks", "Temples"],
        "deliver": ["Package", "Letter", "Artifact", "Supplies", "Medicine", "Documents", "Weapon", "Relic"],
        "escort": ["Merchant", "Noble", "Scholar", "Diplomat", "Pilgrim", "Refugee", "Child", "Prisoner"]
    }
    
    target = random.choice(targets[objective_type])
    
    # Generate titles and descriptions
    if objective_type == "kill":
        title = f"{title_prefix}: The {target} Menace"
        description = generate_quest_description(location, "combat")
    elif objective_type == "collect":
        title = f"{title_prefix}: Precious {target}"
        description = generate_quest_description(location, "collection")
    elif objective_type == "explore":
        title = f"{title_prefix}: Forgotten {target}"
        description = generate_quest_description(location, "exploration")
    elif objective_type == "deliver":
        title = f"{title_prefix}: Urgent {target}"
        description = generate_quest_description(location, "mystery")
    elif objective_type == "escort":
        title = f"{title_prefix}: Vulnerable {target}"
        description = generate_quest_description(location, "rescue")
    
    # Scale objective count with quest type
    if objective_type == "kill":
        objective_count = random.randint(3, 8) + player_level
    elif objective_type == "collect":
        objective_count = random.randint(2, 6) + int(player_level/2)
    elif objective_type == "explore":
        objective_count = random.randint(1, 3)
    elif objective_type == "deliver":
        objective_count = 1
    elif objective_type == "escort":
        objective_count = 1
    
    # Scale rewards with player level and quest difficulty
    reward_exp = (objective_count * 10) * (1 + player_level * 0.1)
    reward_gold = (objective_count * 5) * (1 + player_level * 0.1)
    
    return Quest(title, description, objective_type, objective_count, int(reward_exp), int(reward_gold))


def generate_location_description(location_name, location_type):
    """
    Generate a rich description of a location.
    This simulates what an ML model might generate.
    """
    descriptions = {
        "village": [
            f"{location_name} is a quaint village nestled between rolling hills. Thatched roof cottages line the dirt roads, and the smell of fresh bread wafts from the local bakery. Farmers tend to their crops in nearby fields, while children play with wooden toys in the central square.",
            
            f"The small village of {location_name} features wooden houses with smoke curling from stone chimneys. Villagers nod respectfully as you pass, though some eye you with suspicion. A modest inn stands at the crossroads, offering shelter to the few travelers who venture this way.",
            
            f"{location_name} appears to be a peaceful farming community. Livestock graze in pens, and simple stone markers indicate the boundaries of family plots. The village elder's home is distinguishable by its slightly larger size and the ornate carvings around its doorway."
        ],
        "city": [
            f"The city of {location_name} rises impressively against the horizon, its stone walls standing tall and proud. The main thoroughfare is paved with cobblestones, bustling with merchants, nobles, and commoners alike. Guards in polished armor patrol the streets, maintaining order in this hub of commerce and culture.",
            
            f"{location_name} sprawls before you, a maze of narrow alleys and grand avenues. Market stalls crowd the main square, selling goods from distant lands. The wealthy district is marked by elaborate architecture and gardens, while poorer neighborhoods consist of tightly packed tenements. The contrasts of city life are on full display.",
            
            f"Within the protective walls of {location_name}, diversity thrives. Humans, elves, dwarves, and other races go about their business, creating a tapestry of cultures and traditions. Guildhalls display their banners proudly, and temples to various deities offer spiritual guidance to their followers. The city never truly sleeps."
        ],
        "forest": [
            f"The {location_name} is a dense woodland where sunlight filters through the canopy in dappled patterns. Ancient trees tower overhead, their massive roots creating natural pathways and obstacles. The air is rich with the scent of moss and earth, and distant bird calls echo through the verdant expanse.",
            
            f"Entering the {location_name}, you're enveloped by a green world that seems untouched by civilization. Massive ferns unfurl at the bases of trees, and mushrooms of various colors dot the forest floor. There's a weight to the silence here, broken only by the occasional rustle of unseen creatures moving through the underbrush.",
            
            f"The {location_name} changes character with each step. In some areas, trees grow so densely that they block out the sky entirely. In others, small clearings offer respite and a chance to see the heavens. Strange glowing fungi provide illumination in the darker regions, creating an almost mystical atmosphere."
        ],
        "dungeon": [
            f"The entrance to {location_name} is an ominous stone archway, worn by time and partially covered with creeping vines. Cold air flows outward from the darkness beyond. Torch sconces line the initial corridor, some still bearing the remnants of previous explorers' attempts to illuminate these treacherous halls.",
            
            f"{location_name} descends into the earth, its twisting passages hewn from solid rock. Water drips steadily from the ceiling in places, forming small puddles on the uneven floor. The distant sounds of scratching and skittering suggest you are not alone in this ancient place of forgotten secrets.",
            
            f"The walls of {location_name} bear carved symbols and faded murals depicting scenes from a lost civilization. As you venture deeper, the air grows stale and dust motes dance in any light you bring. Skeletal remains of the less fortunate serve as grim warnings of the dangers that lurk within these labyrinthine chambers."
        ],
        "mountain": [
            f"The {location_name} pierce the clouds, their snow-capped peaks glistening in the sunlight. Jagged cliffs and treacherous paths challenge any who attempt to scale these majestic heights. The air grows thinner as you ascend, rewarding the effort with increasingly spectacular views of the lands below.",
            
            f"Wind howls through the passes of the {location_name}, carrying the cold bite of winter regardless of the season. Hardy mountain goats navigate seemingly impossible slopes with ease, while eagles soar on thermal currents high above. Cave openings dot the mountainsides, some natural and others clearly carved by intelligent hands.",
            
            f"The {location_name} range stands as a natural barrier between realms, its lower slopes covered in pine forests that give way to bare rock and permanent ice. Avalanches have been known to bury unwary travelers, their paths marked by swaths of destruction cut through the vegetation. Rumors speak of ancient dwarf kingdoms hidden within the mountains' heart."
        ],
        "ruins": [
            f"The {location_name} stand as a crumbling testament to a forgotten era. Columns lie toppled across overgrown plazas, and statues stare eyelessly at visitors. Nature reclaims what was once a center of civilization, with vines strangling stone and roots breaking apart foundations.",
            
            f"Time has not been kind to the {location_name}. Once-grand structures now lie exposed to the elements, their roofs long collapsed and their treasures mostly plundered. Yet hints of former glory remain in fragments of colorful mosaics and the imposing scale of what still stands.",
            
            f"An eerie silence permeates the {location_name}, broken only by the wind whistling through empty windows and doorways. Scholars debate which civilization built this place, as the architectural style incorporates elements unfamiliar to modern eyes. Those with magical sensitivity report strange energies lingering here, dormant but not dissipated."
        ]
    }
    
    if location_type in descriptions:
        return random.choice(descriptions[location_type])
    else:
        return f"You've arrived at {location_name}. The area has a distinct character worth exploring."


def generate_npc_dialogue(npc, conversation_type):
    """
    Generate contextual dialogue for NPCs based on their characteristics and conversation context.
    This simulates what an ML model might generate.
    """
    greetings = {
        "friendly": [
            f"Ah, a traveler! Welcome to our humble {npc.location}. I'm {npc.name}.",
            f"Well met, stranger! The name's {npc.name}. What brings you to these parts?",
            f"*smiles warmly* Good day to you! I'm {npc.name}. You look like you've come a long way."
        ],
        "neutral": [
            f"*nods* I'm {npc.name}. What do you need?",
            f"*looks up from work* {npc.name}'s the name. You're not from around here, are you?",
            f"*studies you carefully* I'm called {npc.name}. State your business."
        ],
        "hostile": [
            f"*scowls* What do you want? I'm {npc.name}, and I don't have time for outsiders.",
            f"*narrows eyes* {npc.name}. That's me. Now why are you bothering me?",
            f"*hand moves subtly toward weapon* They call me {npc.name}. You'd best have a good reason for approaching me."
        ]
    }
    
    # Determine NPC's disposition based on their stats and other factors
    if hasattr(npc, 'disposition'):
        disposition = npc.disposition
    else:
        # Calculate disposition if not already set
        disposition = "neutral"
        if npc.stats.charisma > 15:
            disposition = "friendly"
        elif npc.stats.aggression > 70:
            disposition = "hostile"
    
    # Generate greeting
    if conversation_type == "greeting":
        return random.choice(greetings[disposition])
    
    # Generate quest-related dialogue
    elif conversation_type == "quest_offer":
        if disposition == "friendly":
            return f"I could really use someone like you! {generate_quest_description(npc.location)}. Would you be willing to help us out?"
        elif disposition == "neutral":
            return f"I've got a problem that needs solving. {generate_quest_description(npc.location)}. Payment is available if you're interested."
        else:  # hostile
            return f"Look, I don't like asking for help, but I'm desperate. {generate_quest_description(npc.location)}. There's something in it for you, of course."
    
    # Generate merchant dialogue
    elif conversation_type == "merchant":
        if disposition == "friendly":
            return f"Welcome to my humble shop! I've got the finest goods in all of {npc.location}. Take your time browsing - quality merchandise like this deserves appreciation!"
        elif disposition == "neutral":
            return f"Welcome. I buy and sell goods. Fair prices, no haggling. What do you need today?"
        else:  # hostile
            return f"*sigh* Another customer. Look but don't touch unless you're buying. My prices are firm - take it or leave it."
    
    # Generate tavern dialogue
    elif conversation_type == "tavern_rumor":
        rumors = [
            f"They say there's a hidden treasure in the {random.choice(['cave', 'forest', 'ruins', 'temple'])} nearby.",
            f"Strange lights have been seen in the sky over {npc.location} recently. Some say it's a sign of things to come.",
            f"The old {random.choice(['mine', 'tower', 'mansion', 'crypt'])} is supposedly haunted. No one who goes in comes out the same.",
            f"Word is that bandits have set up camp along the road to the next town. Travelers beware.",
            f"Have you heard about the {random.choice(['wizard', 'witch', 'warlock', 'sorcerer'])} who moved into the abandoned tower? Keeps to themselves, but strange noises come from there at night."
        ]
        
        if disposition == "friendly":
            return f"*leans in closely* Hey friend, between you and me... {random.choice(rumors)} Just thought you should know."
        elif disposition == "neutral":
            return f"*takes a sip of ale* If you're interested in local news... {random.choice(rumors)} Take that for what it's worth."
        else:  # hostile
            return f"*grudgingly* Fine, I'll tell you something useful. {random.choice(rumors)} Now leave me to my drink."
    
    # Default response
    return f"{npc.name} looks at you but says nothing of interest."


def generate_combat_description(attacker, defender, damage, is_critical):
    """Generate dynamic combat descriptions based on participants and outcomes."""
    weapon_types = {
        "sword": [
            "slashes at", "cuts toward", "swings at", "thrusts at", 
            "lunges at", "strikes at", "brings their blade down on"
        ],
        "axe": [
            "swings at", "cleaves toward", "brings their axe down on", 
            "chops at", "hacks at", "strikes at"
        ],
        "mace": [
            "swings at", "brings their mace down on", "bashes", 
            "slams into", "strikes at", "crushes toward"
        ],
        "dagger": [
            "stabs at", "slices toward", "lunges at", "thrusts at", 
            "jabs at", "cuts at", "slashes at"
        ],
        "staff": [
            "swings at", "jabs at", "strikes at", "thrusts at", 
            "sweeps at", "brings their staff down on"
        ],
        "fist": [
            "punches", "strikes at", "jabs at", "swings at", 
            "lunges at", "throws a fist toward"
        ],
        "claw": [
            "claws at", "rakes at", "slashes at", "swipes at", 
            "tears at", "lunges at", "rends"
        ],
        "bite": [
            "bites at", "snaps at", "lunges teeth toward", 
            "chomps at", "sinks teeth into", "bares fangs at"
        ]
    }
    
    # Determine weapon type (default to sword if unknown)
    weapon_type = "sword"  # Default
    if hasattr(attacker, 'weapon_type'):
        weapon_type = attacker.weapon_type
    
    # For monsters/creatures without weapons
    if hasattr(attacker, 'attack_type'):
        weapon_type = attacker.attack_type
    
    # Get appropriate verbs
    if weapon_type in weapon_types:
        verb = random.choice(weapon_types[weapon_type])
    else:
        verb = random.choice(weapon_types["sword"])
    
    # Generate hit description
    if damage > 0:
        # Critical hit descriptions
        if is_critical:
            critical_descriptions = [
                f"{attacker.name} finds a perfect opening and {verb} {defender.name} with devastating accuracy, dealing {damage} critical damage!",
                f"In a brilliant display of skill, {attacker.name} {verb} {defender.name}'s vulnerable spot for {damage} critical damage!",
                f"{attacker.name} {verb} {defender.name} with incredible force, landing a critical hit for {damage} damage!"
            ]
            return random.choice(critical_descriptions)
        
        # Normal hit descriptions
        hit_severity = "light"
        if damage > defender.stats.max_health * 0.3:
            hit_severity = "heavy"
        elif damage > defender.stats.max_health * 0.15:
            hit_severity = "moderate"
        
        if hit_severity == "light":
            descriptions = [
                f"{attacker.name} {verb} {defender.name}, inflicting a glancing blow for {damage} damage.",
                f"A quick strike from {attacker.name} catches {defender.name}, dealing {damage} damage.",
                f"{attacker.name} {verb} {defender.name} with a swift motion, dealing {damage} damage."
            ]
        elif hit_severity == "moderate":
            descriptions = [
                f"{attacker.name} {verb} {defender.name} with considerable force, dealing {damage} damage.",
                f"A solid hit from {attacker.name} strikes {defender.name} for {damage} damage.",
                f"{attacker.name} {verb} {defender.name} effectively, causing {damage} damage."
            ]
        else:  # heavy
            descriptions = [
                f"{attacker.name} {verb} {defender.name} with tremendous power, dealing a devastating {damage} damage!",
                f"A mighty blow from {attacker.name} crashes into {defender.name} for {damage} damage!",
                f"{attacker.name} {verb} {defender.name} with brutal efficiency, inflicting {damage} severe damage!"
            ]
        
        return random.choice(descriptions)
    
    # Miss descriptions
    miss_descriptions = [
        f"{attacker.name} {verb} {defender.name}, but the attack misses its mark.",
        f"{defender.name} deftly avoids as {attacker.name} {verb} them.",
        f"The attack from {attacker.name} fails to connect with {defender.name}.",
        f"{attacker.name} {verb} {defender.name}, but {defender.name} blocks the attack."
    ]
    
    return random.choice(miss_descriptions)


def generate_world_event(world):
    """Generate a significant world event for the simulation mode."""
    event_types = [
        "natural_disaster", "political", "economic", 
        "conflict", "discovery", "migration"
    ]
    
    event_type = random.choice(event_types)
    event = ""
    
    if event_type == "natural_disaster":
        disasters = [
            "earthquake", "flood", "wildfire", 
            "drought", "plague", "volcanic eruption", "blizzard"
        ]
        disaster = random.choice(disasters)
        
        # Affected area
        if world.factions:
            affected_faction = random.choice(world.factions)
            faction_name = affected_faction.name
        else:
            faction_name = f"the {random.choice(['northern', 'southern', 'eastern', 'western'])} regions"
        
        severity = random.choice(["mild", "significant", "devastating", "catastrophic"])
        
        impacts = {
            "mild": [
                f"causing minor damage to infrastructure",
                f"resulting in temporary discomfort for residents",
                f"leading to some resource shortages"
            ],
            "significant": [
                f"destroying several important structures",
                f"causing notable casualties and displacement",
                f"significantly depleting food reserves"
            ],
            "devastating": [
                f"decimating large portions of settlements",
                f"resulting in many deaths and a refugee crisis",
                f"destroying critical infrastructure and resources"
            ],
            "catastrophic": [
                f"obliterating entire settlements",
                f"causing massive loss of life and complete displacement",
                f"eliminating most resources and infrastructure"
            ]
        }
        
        impact = random.choice(impacts[severity])
        event = f"A {severity} {disaster} has struck {faction_name}, {impact}."
        
        # Add response information
        responses = [
            f"Local leaders are organizing relief efforts.",
            f"Surrounding factions have offered aid and support.",
            f"The affected population struggles to recover without assistance.",
            f"Opportunistic bandits are targeting weakened settlements."
        ]
        
        event += f" {random.choice(responses)}"
        
    elif event_type == "political":
        if not world.factions or len(world.factions) < 1:
            event = "Political tensions are brewing in various regions as power structures begin to take shape."
        else:
            event_subtypes = [
                "coup", "election", "scandal", "assassination", 
                "new_leader", "policy_change", "alliance"
            ]
            subtype = random.choice(event_subtypes)
            
            faction = random.choice(world.factions)
            
            if subtype == "coup":
                event = f"A coup has occurred in {faction.name}, with power violently changing hands."
            elif subtype == "election":
                event = f"A peaceful transition of power through election has taken place in {faction.name}."
            elif subtype == "scandal":
                scandal_types = ["corruption", "betrayal", "secret alliance", "forbidden magic use"]
                event = f"A {random.choice(scandal_types)} scandal has rocked the leadership of {faction.name}."
            elif subtype == "assassination":
                event = f"An important figure in {faction.name} has been assassinated, causing political turmoil."
            elif subtype == "new_leader":
                event = f"{faction.name} has a new leader who is introducing significant changes to their policies."
            elif subtype == "policy_change":
                policies = ["isolationism", "expansionism", "free trade", "military buildup", "religious reform"]
                event = f"{faction.name} has adopted a policy of {random.choice(policies)}."
            elif subtype == "alliance":
                if len(world.factions) > 1:
                    other_factions = [f for f in world.factions if f != faction]
                    ally = random.choice(other_factions)
                    event = f"{faction.name} and {ally.name} have formed a formal alliance."
                else:
                    event = f"{faction.name} is seeking allies to strengthen their position."
    
    elif event_type == "conflict":
        if len(world.factions) < 2:
            event = "Tensions are rising as different groups compete for resources and territory."
        else:
            conflict_types = ["full_war", "border_skirmish", "trade_dispute", "proxy_war", "civil_war"]
            conflict_type = random.choice(conflict_types)
            
            # Select participants
            if conflict_type == "civil_war":
                faction = random.choice(world.factions)
                event = f"Civil war has broken out within {faction.name}, dividing their territory and people."
            else:
                factions = random.sample(world.factions, 2)
                faction1, faction2 = factions[0], factions[1]
                
                if conflict_type == "full_war":
                    event = f"Full-scale war has erupted between {faction1.name} and {faction2.name}."
                elif conflict_type == "border_skirmish":
                    event = f"Border skirmishes have been reported between {faction1.name} and {faction2.name}."
                elif conflict_type == "trade_dispute":
                    event = f"A serious trade dispute threatens relations between {faction1.name} and {faction2.name}."
                elif conflict_type == "proxy_war":
                    event = f"{faction1.name} and {faction2.name} are fighting through proxies, avoiding direct confrontation."
    
    elif event_type == "discovery":
        discovery_types = [
            "resource", "ruins", "magic", "technology", 
            "creature", "land", "historical_artifact"
        ]
        discovery_type = random.choice(discovery_types)
        
        if world.factions:
            discovering_faction = random.choice(world.factions)
            faction_name = discovering_faction.name
        else:
            faction_name = "Explorers"
        
        if discovery_type == "resource":
            resources = ["gold", "iron", "crystal", "magical ore", "oil", "fertile land"]
            event = f"{faction_name} has discovered a rich deposit of {random.choice(resources)}."
        elif discovery_type == "ruins":
            ruin_types = ["ancient temple", "underground city", "forgotten fortress", "alien structure"]
            event = f"{faction_name} has uncovered a {random.choice(ruin_types)} of unknown origin."
        elif discovery_type == "magic":
            event = f"A new form of magic has been discovered by scholars from {faction_name}."
        elif discovery_type == "technology":
            techs = ["metallurgy", "alchemy", "architecture", "navigation", "siege weapons"]
            event = f"{faction_name} has developed advanced {random.choice(techs)} technology."
        elif discovery_type == "creature":
            event = f"A previously unknown species has been documented in territory controlled by {faction_name}."
        elif discovery_type == "land":
            event = f"{faction_name} explorers have mapped previously uncharted lands beyond the known world."
        elif discovery_type == "historical_artifact":
            event = f"An artifact of immense historical significance has been unearthed in {faction_name} territory."
    
    elif event_type == "economic":
        econ_events = [
            "trade_boom", "recession", "new_trade_route", 
            "resource_depletion", "market_crash", "innovation"
        ]
        econ_event = random.choice(econ_events)
        
        if world.factions:
            affected_faction = random.choice(world.factions)
            faction_name = affected_faction.name
        else:
            faction_name = "The region"
        
        if econ_event == "trade_boom":
            event = f"{faction_name} is experiencing unprecedented economic growth due to increased trade."
        elif econ_event == "recession":
            event = f"Economic hardship has befallen {faction_name}, with resources becoming scarce."
        elif econ_event == "new_trade_route":
            event = f"A new trade route has been established, significantly benefiting {faction_name}."
        elif econ_event == "resource_depletion":
            resources = ["mining", "lumber", "fishing", "farming"]
            event = f"{random.choice(resources).capitalize()} resources in {faction_name} territory are becoming depleted."
        elif econ_event == "market_crash":
            event = f"A sudden market crash has severely impacted the economy of {faction_name}."
        elif econ_event == "innovation":
            industries = ["agriculture", "construction", "military", "transportation", "communication"]
            event = f"Innovation in {random.choice(industries)} has revolutionized industry in {faction_name}."
    
    elif event_type == "migration":
        if not world.factions or len(world.factions) < 2:
            event = "Population movements are occurring as people seek better living conditions."
        else:
            cause = random.choice(["war", "famine", "opportunity", "persecution", "natural disaster"])
            
            factions = random.sample(world.factions, 2)
            source, destination = factions[0], factions[1]
            
            scale = random.choice(["small group", "significant population", "mass exodus"])
            
            event = f"A {scale} is migrating from {source.name} to {destination.name} due to {cause}."
            
            effects = [
                f"This is straining resources in {destination.name}.",
                f"This is bringing valuable skills to {destination.name}.",
                f"This is creating cultural tensions in the destination region.",
                f"This is depleting the workforce of {source.name}."
            ]
            
            event += f" {random.choice(effects)}"
    
    return event
