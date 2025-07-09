# crafting.py
import random
from items import Item

class Recipe:
    """Represents a crafting recipe."""
    def __init__(self, name, ingredients, result_item, skill_required=None, difficulty=1):
        self.name = name
        self.ingredients = ingredients  # Dict of item_name: quantity
        self.result_item = result_item
        self.skill_required = skill_required  # e.g., "blacksmithing", "alchemy"
        self.difficulty = difficulty  # 1-10 scale
    
    def can_craft(self, player):
        """Check if player can craft this recipe."""
        # Check if player has required skill level
        if self.skill_required:
            skill_level = getattr(player, f"{self.skill_required}_skill", 0)
            if skill_level < self.difficulty:
                return False, f"Requires {self.skill_required} skill level {self.difficulty}"
        
        # Check if player has all ingredients
        for item_name, quantity in self.ingredients.items():
            player_quantity = sum(1 for item in player.inventory if item.name == item_name)
            if player_quantity < quantity:
                return False, f"Need {quantity} {item_name}"
        
        return True, "Can craft"
    
    def craft(self, player):
        """Attempt to craft the item."""
        can_craft, message = self.can_craft(player)
        if not can_craft:
            return False, message
        
        # Remove ingredients
        for item_name, quantity in self.ingredients.items():
            removed = 0
            items_to_remove = []
            for item in player.inventory:
                if item.name == item_name and removed < quantity:
                    items_to_remove.append(item)
                    removed += 1
            
            for item in items_to_remove:
                player.inventory.remove(item)
        
        # Calculate success chance based on skill
        if self.skill_required:
            skill_level = getattr(player, f"{self.skill_required}_skill", 0)
            success_chance = min(0.95, 0.5 + (skill_level - self.difficulty) * 0.1)
        else:
            success_chance = 0.8
        
        if random.random() < success_chance:
            # Success
            player.add_to_inventory(self.result_item)
            
            # Gain skill experience
            if self.skill_required:
                current_skill = getattr(player, f"{self.skill_required}_skill", 0)
                skill_gain = max(1, self.difficulty - current_skill + 1)
                setattr(player, f"{self.skill_required}_skill", current_skill + skill_gain)
            
            return True, f"Successfully crafted {self.result_item.name}!"
        else:
            # Failure
            return False, f"Crafting failed! Lost ingredients."

class CraftingSystem:
    """Manages the crafting system."""
    
    def __init__(self):
        self.recipes = self.initialize_recipes()
    
    def initialize_recipes(self):
        """Initialize all available recipes."""
        recipes = []
        
        # Basic weapon recipes
        iron_sword = Item("Iron Sword", "A basic iron sword", 50, "weapon", {"strength": 3})
        steel_sword = Item("Steel Sword", "A well-crafted steel sword", 100, "weapon", {"strength": 5})
        magic_staff = Item("Magic Staff", "A staff imbued with magical energy", 150, "weapon", {"intelligence": 4, "magical_attack": 10})
        
        recipes.extend([
            Recipe("Iron Sword", {"Iron Ore": 2, "Wood": 1}, iron_sword, "blacksmithing", 1),
            Recipe("Steel Sword", {"Steel": 3, "Iron Ore": 1}, steel_sword, "blacksmithing", 3),
            Recipe("Magic Staff", {"Wood": 2, "Magic Crystal": 1}, magic_staff, "enchanting", 2),
        ])
        
        # Armor recipes
        leather_armor = Item("Leather Armor", "Light leather armor", 40, "armor", {"agility": 2, "physical_defense": 5})
        chainmail = Item("Chainmail", "Flexible metal armor", 80, "armor", {"physical_defense": 10})
        plate_armor = Item("Plate Armor", "Heavy protective armor", 120, "armor", {"physical_defense": 15, "agility": -1})
        
        recipes.extend([
            Recipe("Leather Armor", {"Leather": 3, "Thread": 1}, leather_armor, "leatherworking", 1),
            Recipe("Chainmail", {"Iron Ore": 4, "Thread": 2}, chainmail, "blacksmithing", 2),
            Recipe("Plate Armor", {"Steel": 5, "Iron Ore": 2}, plate_armor, "blacksmithing", 4),
        ])
        
        # Potion recipes
        health_potion = Item("Health Potion", "Restores health", 20, "consumable", {"combat_effect": "heal", "healing_value": 30})
        mana_potion = Item("Mana Potion", "Restores mana", 25, "consumable", {"combat_effect": "mana", "mana_value": 30})
        antidote = Item("Antidote", "Cures poison", 30, "consumable", {"combat_effect": "cure_poison"})
        
        recipes.extend([
            Recipe("Health Potion", {"Herbs": 2, "Water": 1}, health_potion, "alchemy", 1),
            Recipe("Mana Potion", {"Magic Herbs": 2, "Water": 1}, mana_potion, "alchemy", 2),
            Recipe("Antidote", {"Antidote Herb": 1, "Water": 1}, antidote, "alchemy", 2),
        ])
        
        # Accessory recipes
        strength_ring = Item("Ring of Strength", "Increases strength", 60, "accessory", {"strength": 3})
        wisdom_amulet = Item("Amulet of Wisdom", "Increases wisdom", 70, "accessory", {"wisdom": 3})
        speed_boots = Item("Boots of Speed", "Increases agility", 50, "accessory", {"agility": 3})
        
        recipes.extend([
            Recipe("Ring of Strength", {"Gold": 1, "Iron Ore": 1}, strength_ring, "jewelcrafting", 2),
            Recipe("Amulet of Wisdom", {"Silver": 1, "Magic Crystal": 1}, wisdom_amulet, "jewelcrafting", 3),
            Recipe("Boots of Speed", {"Leather": 2, "Magic Crystal": 1}, speed_boots, "leatherworking", 2),
        ])
        
        return recipes
    
    def get_available_recipes(self, player):
        """Get recipes the player can craft."""
        available = []
        for recipe in self.recipes:
            can_craft, message = recipe.can_craft(player)
            if can_craft:
                available.append((recipe, "Available"))
            else:
                available.append((recipe, f"Missing: {message}"))
        
        return available
    
    def craft_item(self, player, recipe_index):
        """Attempt to craft an item."""
        if 0 <= recipe_index < len(self.recipes):
            recipe = self.recipes[recipe_index]
            success, message = recipe.craft(player)
            return success, message
        else:
            return False, "Invalid recipe selection"
    
    def show_crafting_menu(self, player):
        """Display the crafting menu."""
        print("\n=== CRAFTING MENU ===")
        print(f"Blacksmithing: {getattr(player, 'blacksmithing_skill', 0)}")
        print(f"Alchemy: {getattr(player, 'alchemy_skill', 0)}")
        print(f"Enchanting: {getattr(player, 'enchanting_skill', 0)}")
        print(f"Leatherworking: {getattr(player, 'leatherworking_skill', 0)}")
        print(f"Jewelcrafting: {getattr(player, 'jewelcrafting_skill', 0)}")
        
        available_recipes = self.get_available_recipes(player)
        
        print("\nAvailable Recipes:")
        for i, (recipe, status) in enumerate(available_recipes):
            print(f"{i+1}. {recipe.name} - {status}")
        
        print(f"{len(available_recipes)+1}. Back")
        
        try:
            choice = int(input("\nChoose recipe to craft: ")) - 1
            if choice == len(available_recipes):
                return
            elif 0 <= choice < len(available_recipes):
                success, message = self.craft_item(player, choice)
                print(f"\n{message}")
                if success:
                    print(f"Added {available_recipes[choice][0].result_item.name} to inventory!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

def generate_crafting_materials(player_level):
    """Generate random crafting materials based on player level."""
    materials = [
        "Iron Ore", "Steel", "Wood", "Leather", "Thread", "Herbs", 
        "Magic Herbs", "Antidote Herb", "Water", "Magic Crystal", 
        "Gold", "Silver"
    ]
    
    # Higher level players get better materials
    if player_level < 5:
        material_pool = materials[:6]  # Basic materials
    elif player_level < 10:
        material_pool = materials[:9]  # Include magic herbs
    else:
        material_pool = materials  # All materials
    
    material = random.choice(material_pool)
    quantity = random.randint(1, 3)
    
    return Item(material, f"A crafting material", 5, "material", {"quantity": quantity})