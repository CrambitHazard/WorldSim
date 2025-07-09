# Text RPG - Enhanced Edition

A sophisticated text-based RPG with character-driven gameplay and autonomous world simulation.

## 🎮 Game Modes

### Character Mode
Traditional RPG where you create and play as a character in a fantastical world.

### Simulation Mode
Autonomous world simulation where NPCs form factions, wage wars, and create their own stories.

## 🆕 New Features Added

### ⚔️ Enhanced Combat System
- **Special Abilities**: Class-specific spells and abilities
  - Mages: Fireball, Ice Shield, Lightning Bolt
  - Warriors: Power Strike, Battle Cry, Shield Wall
  - Paladins: Divine Smite, Lay on Hands, Divine Shield
  - Rogues: Backstab, Poison Dart, Stealth
  - Clerics: Heal, Turn Undead, Bless
- **Status Effects**: Poison, stun, buffs/debuffs
- **Tactical Combat**: Positioning, cover, flanking bonuses
- **Multi-enemy Battles**: Fight multiple opponents simultaneously
- **Critical Hits**: Enhanced damage system with critical strikes

### 🛠️ Crafting System
- **Multiple Skills**: Blacksmithing, Alchemy, Enchanting, Leatherworking, Jewelcrafting
- **Recipes**: Weapons, armor, potions, accessories
- **Skill Progression**: Improve crafting success rates with practice
- **Materials**: Gather resources to craft items

**Available Recipes:**
- Weapons: Iron Sword, Steel Sword, Magic Staff
- Armor: Leather Armor, Chainmail, Plate Armor
- Potions: Health Potion, Mana Potion, Antidote
- Accessories: Ring of Strength, Amulet of Wisdom, Boots of Speed

### 🏠 Housing System
- **Build Rooms**: Bedroom, Kitchen, Living Room, Workshop, Storage Room, Study, Forge, Laboratory, Library, Garden
- **Furniture**: Beds, workbenches, bookshelves, forges, alchemy tables, armchairs, storage chests, mirrors, fireplaces, training dummies
- **Decorations**: Paintings, rugs, plants, candles, tapestries, crystals, fountains, statues
- **Bonuses**: Rest bonuses, crafting bonuses, storage capacity

### 🐾 Companion System
- **6 Species**: Wolf, Eagle, Bear, Fox, Horse, Cat
- **Training**: Combat, obedience, agility, intelligence training
- **Feeding**: Poor, good, and excellent food options
- **Special Abilities**: Species-specific abilities like Pack Tactics, Aerial Attack, Thick Hide, Stealth, Swift Movement, Agile Movement
- **Loyalty & Happiness**: Manage your companion's well-being

### 🏆 Achievement System
- **6 Categories**: Combat, Exploration, Crafting, Social, Collection, Story
- **Rewards**: Gold, experience, items, titles, stat bonuses
- **Progress Tracking**: Monitor your achievements across all categories

**Sample Achievements:**
- **Combat**: First Blood, Warrior, Veteran, Legend, Critical Hit
- **Exploration**: Explorer, Wanderer, Adventurer
- **Crafting**: Apprentice, Craftsman, Master
- **Social**: Friend, Socialite, Diplomat
- **Collection**: Collector, Hoarder, Curator
- **Story**: Novice, Experienced, Veteran, Master, Wealthy, Rich, Millionaire

## 🎯 How to Play

### Starting the Game
```bash
python main.py
```

### Character Creation
1. Enter your character's name
2. Choose your race (Human, Dwarf, Elf, Demon, Angel, Demigod, Messiah, Dragon, Beastman, Kaosborne)
3. Choose your class (Warrior, Mage, Ranger, Cleric, Rogue, Paladin, Warlock, Bard, Monk, Berserker)

### Main Game Loop
1. **Explore**: Find encounters, items, and opportunities
2. **Visit Shop**: Buy and sell items
3. **Rest at Inn**: Recover health and mana
4. **Character Sheet**: View your stats and equipment
5. **Quests**: Accept and complete quests
6. **Travel**: Move between locations
7. **Crafting**: Create items and improve skills
8. **Housing**: Build and customize your home
9. **Companions**: Find and train animal companions
10. **Achievements**: Track your progress and rewards
11. **Save Game**: Save your progress
12. **Return to Main Menu**: Exit to main menu

## 🎨 Features Overview

### Core Systems
- **Character Progression**: Level up, gain experience, improve stats
- **Combat**: Turn-based combat with tactical elements
- **Inventory**: Collect and manage items
- **Equipment**: Weapons, armor, and accessories with stat bonuses
- **Quests**: Dynamic quest generation and completion
- **World Travel**: Multiple locations to explore

### Advanced Systems
- **Crafting**: Create items with different skills and materials
- **Housing**: Build and customize your own home
- **Companions**: Recruit and train animal companions
- **Achievements**: Track accomplishments and earn rewards
- **Simulation**: Autonomous NPCs and faction dynamics

### Quality of Life
- **Save/Load**: JSON-based save system
- **GUI Option**: Tkinter-based interface (alternative to console)
- **Cross-platform**: Works on Windows, Mac, and Linux

## 📁 File Structure

```
text-rpg/
├── main.py              # Main game loop and menu system
├── character.py         # Character classes and stats
├── npc.py              # NPC and faction systems
├── combat.py           # Enhanced combat system
├── simulation.py       # World simulation engine
├── narrative.py        # Quest generation and story
├── items.py           # Item system
├── crafting.py        # Crafting system
├── housing.py         # Housing system
├── companions.py      # Companion system
├── achievements.py    # Achievement system
├── game_state.py      # Game state management
├── utils.py          # Utility functions
├── gui.py            # GUI interface
└── README.md         # This file
```

## 🎮 Controls

### Main Menu
- `1`: New Character Mode Game
- `2`: New Simulation Mode
- `3`: Load Game
- `4`: About
- `5`: Quit

### Character Mode Menu
- `1`: Explore
- `2`: Visit Shop
- `3`: Rest at Inn
- `4`: Character Sheet
- `5`: Quests
- `6`: Travel
- `7`: Crafting
- `8`: Housing
- `9`: Companions
- `10`: Achievements
- `11`: Save Game
- `12`: Return to Main Menu

## 🛠️ Technical Details

### Requirements
- Python 3.6+
- No external dependencies (pure Python)

### Save Files
- JSON format
- Includes all character data, world state, and system progress
- Compatible with both Character and Simulation modes

### Performance
- Optimized for text-based gameplay
- Efficient simulation engine for large worlds
- Memory-conscious design for long play sessions

## 🎯 Tips for New Players

1. **Start with Character Mode** to learn the basics
2. **Explore frequently** to find items and opportunities
3. **Craft items** to improve your equipment
4. **Build a house** for better rest and crafting bonuses
5. **Find a companion** for combat assistance
6. **Track achievements** for additional rewards
7. **Save regularly** to preserve your progress

## 🚀 Future Enhancements

The game is designed to be easily extensible. Potential future features include:
- Multiplayer elements
- More complex AI behaviors
- Additional crafting recipes
- Expanded world simulation
- Modding support
- Cloud saves
- Mobile version

## 📝 License

This project is open source and available under the MIT License.

---

**Enjoy your adventure in the Text RPG world!** 🎮✨