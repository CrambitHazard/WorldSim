# Text RPG: Character & Simulation Mode

A Python-based text adventure game featuring both character-driven gameplay and an autonomous world simulation mode.

## Features

### Character Mode
- Create and customize your character with different races and classes
- Explore various locations and encounter NPCs
- Combat system with turn-based battles
- Quest system with dynamic objectives
- Inventory and equipment management
- Shop system for buying and selling items
- Save/load game functionality

### Simulation Mode
- Autonomous world where NPCs form factions
- Dynamic political systems and warfare
- Procedurally generated events and stories
- Multiple world sizes and complexity levels
- Real-time world observation

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. No external dependencies required (uses only standard library)

```bash
# Optional: Install enhanced terminal libraries
pip install colorama rich
```

## How to Play

### Starting the Game
```bash
python main.py
```

### Game Modes

#### Character Mode
- Create your character with custom name, race, and class
- Explore locations, fight enemies, complete quests
- Manage inventory and equipment
- Save your progress and continue later

#### Simulation Mode
- Watch an autonomous world develop
- Observe NPCs forming factions and engaging in politics
- Choose world size and complexity
- View detailed statistics and faction information

### Controls
- Use number keys (1, 2, 3, etc.) to make selections
- Press Enter to continue
- Type 'b' or 'back' to return to previous menus

## File Structure

```
├── main.py           # Main game entry point
├── character.py      # Character classes and stats
├── combat.py         # Combat system
├── items.py          # Item system
├── npc.py           # NPC and faction system
├── narrative.py      # Story generation
├── simulation.py     # World simulation
├── game_state.py     # Game state management
├── gui.py           # GUI components (optional)
├── utils.py         # Utility functions
├── quests.py        # Quest system
└── README.md        # This file
```

## Game Mechanics

### Character Classes
- **Warrior**: High strength and constitution
- **Mage**: High intelligence and magical abilities
- **Ranger**: High agility and perception
- **Cleric**: Balanced wisdom and healing
- **Rogue**: High agility and stealth
- **Paladin**: Holy warrior with protection abilities
- **Warlock**: Dark magic user
- **Bard**: Charismatic support character
- **Monk**: Agile martial artist
- **Berserker**: Fierce warrior with rage abilities

### Races
- **Human**: Balanced stats
- **Dwarf**: High constitution and strength
- **Elf**: High intelligence and agility
- **Demon**: High strength and magical abilities
- **Angel**: High wisdom and magical defense
- **Demigod**: Superior stats across the board
- **Messiah**: Divine abilities and high charisma
- **Dragon**: Exceptional strength and magical power
- **Beastman**: High agility and physical abilities
- **Kaosborne**: Unpredictable chaotic abilities

## Contributing

Feel free to contribute by:
- Adding new character classes or races
- Improving the combat system
- Enhancing the simulation mode
- Adding new quest types
- Improving the UI/UX

## License

This project is open source and available under the MIT License.

## Credits

Created with passion by your friendly neighborhood developer.