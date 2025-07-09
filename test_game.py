#!/usr/bin/env python3
"""
Simple test script to verify the game systems work correctly.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from character import PlayerCharacter, create_character
        print("✓ Character system imported")
    except ImportError as e:
        print(f"✗ Character system import failed: {e}")
        return False
    
    try:
        from combat import Combat
        print("✓ Combat system imported")
    except ImportError as e:
        print(f"✗ Combat system import failed: {e}")
        return False
    
    try:
        from crafting import CraftingSystem
        print("✓ Crafting system imported")
    except ImportError as e:
        print(f"✗ Crafting system import failed: {e}")
        return False
    
    try:
        from housing import HousingSystem
        print("✓ Housing system imported")
    except ImportError as e:
        print(f"✗ Housing system import failed: {e}")
        return False
    
    try:
        from companions import CompanionSystem
        print("✓ Companion system imported")
    except ImportError as e:
        print(f"✗ Companion system import failed: {e}")
        return False
    
    try:
        from achievements import AchievementSystem
        print("✓ Achievement system imported")
    except ImportError as e:
        print(f"✗ Achievement system import failed: {e}")
        return False
    
    try:
        from magic_system import MagicSystem
        print("✓ Magic system imported")
    except ImportError as e:
        print(f"✗ Magic system import failed: {e}")
        return False
    
    try:
        from religion import ReligionSystem
        print("✓ Religion system imported")
    except ImportError as e:
        print(f"✗ Religion system import failed: {e}")
        return False
    
    try:
        from reputation import ReputationSystem
        print("✓ Reputation system imported")
    except ImportError as e:
        print(f"✗ Reputation system import failed: {e}")
        return False
    
    return True

def test_systems():
    """Test that the systems can be instantiated."""
    print("\nTesting system instantiation...")
    
    try:
        from magic_system import MagicSystem
        magic = MagicSystem()
        print(f"✓ Magic system: {len(magic.available_spells)} spells available")
    except Exception as e:
        print(f"✗ Magic system failed: {e}")
        return False
    
    try:
        from religion import ReligionSystem
        religion = ReligionSystem()
        print(f"✓ Religion system: {len(religion.gods)} gods, {len(religion.religions)} religions")
    except Exception as e:
        print(f"✗ Religion system failed: {e}")
        return False
    
    try:
        from reputation import ReputationSystem
        reputation = ReputationSystem()
        print(f"✓ Reputation system: {len(reputation.factions)} factions")
    except Exception as e:
        print(f"✗ Reputation system failed: {e}")
        return False
    
    try:
        from crafting import CraftingSystem
        crafting = CraftingSystem()
        print(f"✓ Crafting system: {len(crafting.recipes)} recipes available")
    except Exception as e:
        print(f"✗ Crafting system failed: {e}")
        return False
    
    try:
        from housing import HousingSystem
        housing = HousingSystem()
        print(f"✓ Housing system: {len(housing.available_rooms)} room types, {len(housing.available_furniture)} furniture types")
    except Exception as e:
        print(f"✗ Housing system failed: {e}")
        return False
    
    try:
        from companions import CompanionSystem
        companions = CompanionSystem()
        print(f"✓ Companion system: {len(companions.available_species)} companion types")
    except Exception as e:
        print(f"✗ Companion system failed: {e}")
        return False
    
    try:
        from achievements import AchievementSystem
        achievements = AchievementSystem()
        print(f"✓ Achievement system: {len(achievements.achievements)} achievements available")
    except Exception as e:
        print(f"✗ Achievement system failed: {e}")
        return False
    
    return True

def test_character_creation():
    """Test character creation and system integration."""
    print("\nTesting character creation...")
    
    try:
        from character import create_character
        from magic_system import MagicSystem
        from religion import ReligionSystem
        from reputation import ReputationSystem
        
        # Create a test character
        player = create_character()
        print(f"✓ Character created: {player.name} - Level {player.level} {player.race} {player.character_class}")
        
        # Initialize systems
        player.magic_system = MagicSystem()
        player.religion_system = ReligionSystem()
        player.reputation_system = ReputationSystem()
        print("✓ All systems initialized for character")
        
        # Test basic functionality
        print(f"  Health: {player.stats.health}/{player.stats.max_health}")
        print(f"  Mana: {player.stats.mana}/{player.stats.max_mana}")
        print(f"  Gold: {player.gold}")
        print(f"  Known spells: {len(getattr(player, 'known_spells', []))}")
        print(f"  Religion: {getattr(player, 'religion', 'None')}")
        print(f"  Faction reputation: {len(player.reputation_system.player_reputation)} factions")
        
        return True
        
    except Exception as e:
        print(f"✗ Character creation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Text RPG System Test ===\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return
    
    # Test system instantiation
    if not test_systems():
        print("\n❌ System instantiation tests failed!")
        return
    
    # Test character creation
    if not test_character_creation():
        print("\n❌ Character creation tests failed!")
        return
    
    print("\n✅ All tests passed! The game should work correctly.")
    print("\nTo start the game, run: python3 main.py")

if __name__ == "__main__":
    main()