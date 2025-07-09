import random
from utils import typewriter_effect

class Quest:
    """Base quest class for the game."""
    
    def __init__(self, title, description, objective, reward_exp, reward_gold, quest_type="kill"):
        self.title = title
        self.description = description
        self.objective = objective
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.quest_type = quest_type
        self.completed = False
        self.progress = 0
        self.target = 1  # Default target for completion
        
    def get_progress_text(self):
        """Return progress text for the quest."""
        if self.quest_type == "kill":
            return f"Kill {self.progress}/{self.target} enemies"
        elif self.quest_type == "collect":
            return f"Collect {self.progress}/{self.target} items"
        elif self.quest_type == "visit":
            return f"Visit {self.progress}/{self.target} locations"
        else:
            return f"Progress: {self.progress}/{self.target}"
    
    def update_progress(self, amount=1):
        """Update quest progress."""
        self.progress += amount
        if self.progress >= self.target:
            self.completed = True
        return self.completed
    
    def to_dict(self):
        """Convert quest to dictionary for saving."""
        return {
            "title": self.title,
            "description": self.description,
            "objective": self.objective,
            "reward_exp": self.reward_exp,
            "reward_gold": self.reward_gold,
            "quest_type": self.quest_type,
            "completed": self.completed,
            "progress": self.progress,
            "target": self.target
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a quest from dictionary data."""
        quest = cls(
            data["title"],
            data["description"],
            data["objective"],
            data["reward_exp"],
            data["reward_gold"],
            data["quest_type"]
        )
        quest.completed = data["completed"]
        quest.progress = data["progress"]
        quest.target = data["target"]
        return quest

def generate_random_quest(player_level, location):
    """Generate a random quest appropriate for the player's level."""
    quest_types = [
        {
            "type": "kill",
            "titles": [
                f"Clear the {location} Bandits",
                f"Hunt the {location} Wolves",
                f"Defeat the {location} Goblins",
                f"Slay the {location} Trolls"
            ],
            "descriptions": [
                f"Local authorities need help dealing with threats in {location}.",
                f"Wild animals are causing problems for the residents of {location}.",
                f"Monstrous creatures have been spotted near {location}.",
                f"A dangerous creature has been terrorizing {location}."
            ]
        },
        {
            "type": "collect",
            "titles": [
                f"Gather {location} Herbs",
                f"Collect {location} Artifacts",
                f"Retrieve {location} Relics",
                f"Find {location} Crystals"
            ],
            "descriptions": [
                f"Local alchemists need rare herbs found in {location}.",
                f"Archaeologists are looking for ancient artifacts in {location}.",
                f"Religious orders seek sacred relics from {location}.",
                f"Magical crystals are needed from {location}."
            ]
        }
    ]
    
    quest_type = random.choice(quest_types)
    title = random.choice(quest_type["titles"])
    description = random.choice(quest_type["descriptions"])
    
    # Scale rewards with player level
    base_exp = 50 + (player_level * 25)
    base_gold = 20 + (player_level * 10)
    
    return Quest(
        title=title,
        description=description,
        objective=f"Complete the task in {location}",
        reward_exp=base_exp,
        reward_gold=base_gold,
        quest_type=quest_type["type"]
    )