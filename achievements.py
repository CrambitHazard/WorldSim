# achievements.py
import random
from items import Item

class Achievement:
    """Represents an achievement that can be unlocked."""
    def __init__(self, name, description, condition, reward_type, reward_value, category):
        self.name = name
        self.description = description
        self.condition = condition  # Function that checks if achieved
        self.reward_type = reward_type  # "gold", "exp", "item", "title", "stat_bonus"
        self.reward_value = reward_value
        self.category = category
        self.unlocked = False
        self.unlock_date = None
    
    def check_condition(self, player):
        """Check if the achievement condition is met."""
        if not self.unlocked:
            return self.condition(player)
        return False
    
    def unlock(self, player):
        """Unlock the achievement and give rewards."""
        if self.unlocked:
            return False
        
        self.unlocked = True
        import time
        self.unlock_date = time.time()
        
        # Give rewards
        if self.reward_type == "gold":
            player.gold += self.reward_value
            return f"Unlocked {self.name}! Gained {self.reward_value} gold!"
        elif self.reward_type == "exp":
            exp_gain = player.gain_exp(self.reward_value)
            return f"Unlocked {self.name}! {exp_gain}"
        elif self.reward_type == "item":
            item = self.reward_value
            player.add_to_inventory(item)
            return f"Unlocked {self.name}! Received {item.name}!"
        elif self.reward_type == "title":
            if not hasattr(player, 'titles'):
                player.titles = []
            player.titles.append(self.reward_value)
            return f"Unlocked {self.name}! Earned title: {self.reward_value}!"
        elif self.reward_type == "stat_bonus":
            stat, bonus = self.reward_value
            setattr(player.stats, stat, getattr(player.stats, stat) + bonus)
            return f"Unlocked {self.name}! +{bonus} to {stat}!"
        
        return f"Unlocked {self.name}!"
    
    def to_dict(self):
        """Convert achievement to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "reward_type": self.reward_type,
            "reward_value": self.reward_value,
            "category": self.category,
            "unlocked": self.unlocked,
            "unlock_date": self.unlock_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create achievement from dictionary."""
        # Note: We can't easily restore the condition function, so we'll need to recreate achievements
        return cls(data["name"], data["description"], lambda p: False, 
                  data["reward_type"], data["reward_value"], data["category"])

class AchievementSystem:
    """Manages the achievement system."""
    
    def __init__(self):
        self.achievements = self.initialize_achievements()
        self.categories = ["Combat", "Exploration", "Crafting", "Social", "Collection", "Story"]
    
    def initialize_achievements(self):
        """Initialize all available achievements."""
        achievements = []
        
        # Combat achievements
        achievements.extend([
            Achievement(
                "First Blood",
                "Win your first combat encounter",
                lambda p: hasattr(p, 'combat_wins') and p.combat_wins >= 1,
                "gold", 50, "Combat"
            ),
            Achievement(
                "Warrior",
                "Win 10 combat encounters",
                lambda p: hasattr(p, 'combat_wins') and p.combat_wins >= 10,
                "title", "The Warrior", "Combat"
            ),
            Achievement(
                "Veteran",
                "Win 50 combat encounters",
                lambda p: hasattr(p, 'combat_wins') and p.combat_wins >= 50,
                "exp", 200, "Combat"
            ),
            Achievement(
                "Legend",
                "Win 100 combat encounters",
                lambda p: hasattr(p, 'combat_wins') and p.combat_wins >= 100,
                "title", "The Legend", "Combat"
            ),
            Achievement(
                "Critical Hit",
                "Score a critical hit in combat",
                lambda p: hasattr(p, 'critical_hits') and p.critical_hits >= 1,
                "gold", 25, "Combat"
            ),
        ])
        
        # Exploration achievements
        achievements.extend([
            Achievement(
                "Explorer",
                "Visit 5 different locations",
                lambda p: hasattr(p, 'locations_visited') and len(p.locations_visited) >= 5,
                "gold", 100, "Exploration"
            ),
            Achievement(
                "Wanderer",
                "Visit 10 different locations",
                lambda p: hasattr(p, 'locations_visited') and len(p.locations_visited) >= 10,
                "title", "The Wanderer", "Exploration"
            ),
            Achievement(
                "Adventurer",
                "Visit 20 different locations",
                lambda p: hasattr(p, 'locations_visited') and len(p.locations_visited) >= 20,
                "exp", 300, "Exploration"
            ),
        ])
        
        # Crafting achievements
        achievements.extend([
            Achievement(
                "Apprentice",
                "Craft your first item",
                lambda p: hasattr(p, 'items_crafted') and p.items_crafted >= 1,
                "gold", 75, "Crafting"
            ),
            Achievement(
                "Craftsman",
                "Craft 10 items",
                lambda p: hasattr(p, 'items_crafted') and p.items_crafted >= 10,
                "title", "The Craftsman", "Crafting"
            ),
            Achievement(
                "Master",
                "Craft 50 items",
                lambda p: hasattr(p, 'items_crafted') and p.items_crafted >= 50,
                "exp", 400, "Crafting"
            ),
        ])
        
        # Social achievements
        achievements.extend([
            Achievement(
                "Friend",
                "Make your first friend",
                lambda p: hasattr(p, 'friends_made') and p.friends_made >= 1,
                "gold", 50, "Social"
            ),
            Achievement(
                "Socialite",
                "Make 5 friends",
                lambda p: hasattr(p, 'friends_made') and p.friends_made >= 5,
                "title", "The Socialite", "Social"
            ),
            Achievement(
                "Diplomat",
                "Make 10 friends",
                lambda p: hasattr(p, 'friends_made') and p.friends_made >= 10,
                "exp", 250, "Social"
            ),
        ])
        
        # Collection achievements
        achievements.extend([
            Achievement(
                "Collector",
                "Collect 10 different items",
                lambda p: hasattr(p, 'unique_items_collected') and p.unique_items_collected >= 10,
                "gold", 100, "Collection"
            ),
            Achievement(
                "Hoarder",
                "Collect 25 different items",
                lambda p: hasattr(p, 'unique_items_collected') and p.unique_items_collected >= 25,
                "title", "The Hoarder", "Collection"
            ),
            Achievement(
                "Curator",
                "Collect 50 different items",
                lambda p: hasattr(p, 'unique_items_collected') and p.unique_items_collected >= 50,
                "exp", 500, "Collection"
            ),
        ])
        
        # Level achievements
        achievements.extend([
            Achievement(
                "Novice",
                "Reach level 5",
                lambda p: p.level >= 5,
                "gold", 100, "Story"
            ),
            Achievement(
                "Experienced",
                "Reach level 10",
                lambda p: p.level >= 10,
                "title", "The Experienced", "Story"
            ),
            Achievement(
                "Veteran",
                "Reach level 20",
                lambda p: p.level >= 20,
                "exp", 1000, "Story"
            ),
            Achievement(
                "Master",
                "Reach level 30",
                lambda p: p.level >= 30,
                "title", "The Master", "Story"
            ),
        ])
        
        # Gold achievements
        achievements.extend([
            Achievement(
                "Wealthy",
                "Accumulate 1000 gold",
                lambda p: p.gold >= 1000,
                "title", "The Wealthy", "Story"
            ),
            Achievement(
                "Rich",
                "Accumulate 5000 gold",
                lambda p: p.gold >= 5000,
                "exp", 800, "Story"
            ),
            Achievement(
                "Millionaire",
                "Accumulate 10000 gold",
                lambda p: p.gold >= 10000,
                "title", "The Millionaire", "Story"
            ),
        ])
        
        return achievements
    
    def check_achievements(self, player):
        """Check all achievements and unlock any that are met."""
        unlocked_achievements = []
        
        for achievement in self.achievements:
            if achievement.check_condition(player):
                message = achievement.unlock(player)
                unlocked_achievements.append(message)
        
        return unlocked_achievements
    
    def get_achievement_progress(self, player):
        """Get progress information for all achievements."""
        progress = {}
        
        for achievement in self.achievements:
            if achievement.category not in progress:
                progress[achievement.category] = {"total": 0, "unlocked": 0}
            
            progress[achievement.category]["total"] += 1
            if achievement.unlocked:
                progress[achievement.category]["unlocked"] += 1
        
        return progress
    
    def show_achievements_menu(self, player):
        """Display the achievements menu."""
        while True:
            print("\n=== ACHIEVEMENTS ===")
            
            # Show overall progress
            progress = self.get_achievement_progress(player)
            total_unlocked = sum(cat["unlocked"] for cat in progress.values())
            total_achievements = sum(cat["total"] for cat in progress.values())
            print(f"Progress: {total_unlocked}/{total_achievements} achievements unlocked")
            
            print("\nCategories:")
            for i, category in enumerate(self.categories):
                if category in progress:
                    unlocked = progress[category]["unlocked"]
                    total = progress[category]["total"]
                    print(f"{i+1}. {category} ({unlocked}/{total})")
            
            print(f"{len(self.categories)+1}. View All Achievements")
            print(f"{len(self.categories)+2}. Back")
            
            try:
                choice = int(input("\nChoose option: "))
                
                if 1 <= choice <= len(self.categories):
                    category = self.categories[choice - 1]
                    self.show_category_achievements(player, category)
                elif choice == len(self.categories) + 1:
                    self.show_all_achievements(player)
                elif choice == len(self.categories) + 2:
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input!")
    
    def show_category_achievements(self, player, category):
        """Show achievements for a specific category."""
        print(f"\n=== {category.upper()} ACHIEVEMENTS ===")
        
        category_achievements = [a for a in self.achievements if a.category == category]
        
        for i, achievement in enumerate(category_achievements):
            status = "✓" if achievement.unlocked else "□"
            print(f"{i+1}. [{status}] {achievement.name}")
            print(f"   {achievement.description}")
            if achievement.unlocked:
                print(f"   Reward: {achievement.reward_type} - {achievement.reward_value}")
            else:
                print(f"   Reward: {achievement.reward_type} - {achievement.reward_value}")
            print()
        
        input("Press Enter to continue...")
    
    def show_all_achievements(self, player):
        """Show all achievements."""
        print("\n=== ALL ACHIEVEMENTS ===")
        
        for category in self.categories:
            print(f"\n{category.upper()}:")
            category_achievements = [a for a in self.achievements if a.category == category]
            
            for achievement in category_achievements:
                status = "✓" if achievement.unlocked else "□"
                print(f"  [{status}] {achievement.name} - {achievement.description}")
        
        input("\nPress Enter to continue...")
    
    def get_recent_achievements(self, player, count=5):
        """Get recently unlocked achievements."""
        unlocked_achievements = [a for a in self.achievements if a.unlocked]
        unlocked_achievements.sort(key=lambda x: x.unlock_date or 0, reverse=True)
        return unlocked_achievements[:count]
    
    def to_dict(self):
        """Convert achievement system to dictionary."""
        return {
            "achievements": [achievement.to_dict() for achievement in self.achievements]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create achievement system from dictionary."""
        system = cls()
        
        # Restore achievement states
        for achievement_data in data.get("achievements", []):
            for achievement in system.achievements:
                if achievement.name == achievement_data["name"]:
                    achievement.unlocked = achievement_data.get("unlocked", False)
                    achievement.unlock_date = achievement_data.get("unlock_date")
                    break
        
        return system

def track_player_stats(player, action_type, value=1):
    """Track player statistics for achievements."""
    if not hasattr(player, 'achievement_stats'):
        player.achievement_stats = {}
    
    if action_type not in player.achievement_stats:
        player.achievement_stats[action_type] = 0
    
    player.achievement_stats[action_type] += value
    
    # Set specific attributes for achievement checking
    if action_type == "combat_wins":
        player.combat_wins = player.achievement_stats.get("combat_wins", 0)
    elif action_type == "critical_hits":
        player.critical_hits = player.achievement_stats.get("critical_hits", 0)
    elif action_type == "items_crafted":
        player.items_crafted = player.achievement_stats.get("items_crafted", 0)
    elif action_type == "friends_made":
        player.friends_made = player.achievement_stats.get("friends_made", 0)
    elif action_type == "unique_items_collected":
        # Count unique items in inventory
        unique_items = set(item.name for item in player.inventory)
        player.unique_items_collected = len(unique_items)
    elif action_type == "locations_visited":
        if not hasattr(player, 'locations_visited'):
            player.locations_visited = set()
        player.locations_visited.add(player.location)