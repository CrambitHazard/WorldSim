# main.py
import sys
import random
import tkinter as tk
from tkinter import messagebox, filedialog
from utils import clear_screen, typewriter_effect, save_game, load_game, get_save_files
from character import PlayerCharacter, create_character
from npc import NPC
from combat import Combat
from narrative import generate_quest, generate_location_description
from simulation import WorldSimulation
from items import generate_random_item
from game_state import GameState

root = tk.Tk()
root.withdraw()

def main_menu():
    """Display the main menu and handle user selection."""
    while True:
        try:
            clear_screen()
            title = """
  _____                _    _____  _____   _____
 |_   _|              | |  |  __ \\|  __ \\ / ____|
   | |    ___  __  __ | |_ | |__) | |__) | |  __
   | |   / _ \\ \\ \\/ / | __||  ___/|  ___/| | |_ |
  _| |_ |  __/  >  <  | |_ | |    | |    | |__| |
 |_____| \\___| /_/\\_\\  \\__||_|    |_|     \\_____|
                                                  
    """
            print(title)
            typewriter_effect("\nWelcome to Text RPG: Character & Simulation Mode!")
            print("\nMain Menu:")
            print("1. New Character Mode Game")
            print("2. New Simulation Mode")
            print("3. Load Game")
            print("4. About")
            print("5. Quit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                character_mode()
            elif choice == "2":
                simulation_mode()
            elif choice == "3":
                load_game_menu()
            elif choice == "4":
                about_screen()
            elif choice == "5":
                print("\nThank you for playing! Goodbye.")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please enter a number between 1-5.")
                input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("\nPress Enter to continue...")

def load_game_menu():
    """Display a menu for loading a saved game."""
    clear_screen()
    print("=== Load Game ===\n")
    save_files = get_save_files()
    if not save_files:
        print("No save files found.")
        input("\nPress Enter to return to the main menu...")
        main_menu()
    else:
        for i, file in enumerate(save_files, 1):
            print(f"{i}. {file}")
        choice = input("\nEnter the number of the file to load, or 'b' to go back: ")
        if choice.lower() == 'b':
            main_menu()
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(save_files):
                    player, world, msg = load_game(save_files[index])
                    print(msg)
                    input("\nPress Enter to continue...")
                    global game_state
                    game_state = GameState(player=player, world=world)
                    # If world exists, assume Simulation Mode; otherwise, Character Mode
                    if world:
                        simulation_mode_loaded(world)
                    else:
                        game_loop(player)
                else:
                    print("Invalid selection.")
                    input("\nPress Enter to continue...")
                    load_game_menu()
            except ValueError:
                print("Invalid input.")
                input("\nPress Enter to continue...")
                load_game_menu()

def simulation_mode_loaded(world):
    """Start simulation mode from a loaded game state."""
    simulation_loop(world)

def character_mode():
    """Start a new character-driven mode game."""
    clear_screen()
    typewriter_effect("=== Character Mode ===\n")
    typewriter_effect("In this mode, you'll create and play as a character in a fantastical world.\n")
    
    # Character creation
    player = create_character()
    global game_state
    game_state = GameState(player=player, world=None)
    game_loop(player)

def simulation_mode():
    """Start a new simulation mode game."""
    clear_screen()
    typewriter_effect("=== Simulation Mode ===\n")
    typewriter_effect("In this mode, you'll observe an autonomous world where NPCs form factions, wage wars, and create their own stories.\n")
    
    # Create simulation world
    world = WorldSimulation()
    print("\nSelect world size:")
    print("1. Small")
    print("2. Medium")
    print("3. Large")
    size_choice = input("\nEnter choice (1-3): ")
    if size_choice == "1":
        world_size = "small"
    elif size_choice == "3":
        world_size = "large"
    else:
        world_size = "medium"
    
    print("\nSelect world complexity:")
    print("1. Simple")
    print("2. Standard")
    print("3. Complex")
    complexity_choice = input("\nEnter choice (1-3): ")
    if complexity_choice == "1":
        complexity = "simple"
    elif complexity_choice == "3":
        complexity = "complex"
    else:
        complexity = "medium"
    
    # Create world with specified parameters
    world.create_world(world_size, complexity)
    global game_state
    game_state = GameState(player=None, world=world)
    
    simulation_loop(world)

def game_loop(player):
    """Main game loop for character mode."""
    current_location = player.location
    quit_game = False
    
    while not quit_game:
        clear_screen()
        print(f"=== {current_location} ===")
        print(f"Player: {player.name} - Level {player.level} {player.race} {player.character_class}")
        print(f"Health: {player.stats.health}/{player.stats.max_health} | Mana: {player.stats.mana}/{player.stats.max_mana} | Gold: {player.gold}")
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Visit Shop")
        print("3. Rest at Inn")
        print("4. Character Sheet")
        print("5. Quests")
        print("6. Travel")
        print("7. Save Game")
        print("8. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-8): ")
        if choice == "1":
            explore(player)
        elif choice == "2":
            visit_shop(player)
        elif choice == "3":
            rest_at_inn(player)
        elif choice == "4":
            player.display_character_sheet()
        elif choice == "5":
            manage_quests(player)
        elif choice == "6":
            new_location = travel(player)
            if new_location:
                current_location = new_location
                player.change_location(new_location)
        elif choice == "7":
            result = save_game(player)
            print(result)
            input("\nPress Enter to continue...")
        elif choice == "8":
            if confirm_action("Are you sure you want to return to the main menu? Unsaved progress will be lost."):
                quit_game = True
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def simulation_loop(world):
    """Main simulation loop for simulation mode."""
    quit_simulation = False
    
    while not quit_simulation:
        clear_screen()
        print(f"=== Simulation: Year {world.current_year}, {world.current_season} ===")
        print(f"Factions: {len(world.factions)} | NPCs: {len(world.npcs)} | Locations: {len(world.locations)}")
        
        print("\nWhat would you like to do?")
        print("1. Run Simulation (1 Season)")
        print("2. Run Simulation (1 Year)")
        print("3. Run Simulation (5 Years)")
        print("4. View World Status")
        print("5. View Faction Details")
        print("6. View Top 5 Characters for Each Stat")
        print("7. Save Simulation")
        print("8. Return to Main Menu")
        
        choice = input("\nEnter your choice (1-8): ")
        if choice == "1":
            world.run_simulation(ticks=1, display_results=False)
        elif choice == "2":
            world.run_simulation(ticks=4, display_results=False)
        elif choice == "3":
            world.run_simulation(ticks=20, display_results=False)
        elif choice == "4":
            world.display_world_status()
        elif choice == "5":
            view_faction_details(world)
        elif choice == "6":
            view_top_stats(world)
        elif choice == "7":
            # Create a dummy player for simulation save purposes
            dummy_player = PlayerCharacter("Simulation_Observer")
            result = save_game(dummy_player, world, f"Simulation_Y{world.current_year}_save.json")
            print(result)
            input("\nPress Enter to continue...")
        elif choice == "8":
            if confirm_action("Are you sure you want to return to the main menu? Unsaved progress will be lost."):
                quit_simulation = True
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def view_faction_details(world):
    """Display detailed information for a chosen faction."""
    clear_screen()
    print("=== Faction Details ===\n")
    if not world.factions:
        print("No factions available in this simulation.")
        input("\nPress Enter to continue...")
        return
    print("Select a faction to view:")
    for i, faction in enumerate(world.factions, 1):
        print(f"{i}. {faction.name} (Members: {len(faction.members)}, Leader: {faction.leader.name})")
    print(f"{len(world.factions)+1}. Back")
    
    choice = input(f"\nEnter choice (1-{len(world.factions)+1}): ")
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(world.factions):
            world.get_faction_details(choice_num - 1)
        elif choice_num == len(world.factions) + 1:
            return
        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")

def view_top_stats(world):
    """Display the top 5 characters for each stat in a new window."""
    # Define which stats to show:
    stat_names = ["strength", "intelligence", "wisdom", "constitution", "agility", "perception", "charisma"]
    results = ""
    npcs = world.npcs
    for stat in stat_names:
        sorted_npcs = sorted(npcs, key=lambda npc: getattr(npc.stats, stat), reverse=True)
        results += f"Top 5 for {stat.title()}:\n"
        for idx, npc in enumerate(sorted_npcs[:5]):
            value = getattr(npc.stats, stat)
            results += f"  {idx+1}. {npc.name}: {value}\n"
        results += "\n"
    
    # Create a pop-up window to show the results
    top_window = tk.Toplevel()
    top_window.title("Top 5 Characters for Each Stat")
    text_widget = tk.Text(top_window, wrap="word", width=80, height=30)
    text_widget.pack(fill="both", expand=True)
    text_widget.insert("end", results)
    text_widget.configure(state="disabled")

def explore(player):
    """Handle exploration in the current location."""
    clear_screen()
    print(f"=== Exploring {player.location} ===\n")
    location_type = "village"  # This could be dynamic based on player's location data
    description = generate_location_description(player.location, location_type)
    typewriter_effect(description)
    
    print("\nWhat would you like to do?")
    print("1. Look for adventure")
    print("2. Search for items")
    print("3. Talk to locals")
    print("4. Return")
    
    choice = input("\nEnter your choice (1-4): ")
    if choice == "1":
        if random.random() < 0.7:
            handle_encounter(player)
        else:
            print("\nYou search for adventure but nothing unusual happens.")
            input("\nPress Enter to continue...")
    elif choice == "2":
        if random.random() < 0.4:
            item = generate_random_item(player.level)
            player.add_to_inventory(item)
            print(f"\nYou found a {item.name}!")
            print(f"Description: {item.description}")
            print(f"Value: {item.value} gold")
            input("\nPress Enter to continue...")
        else:
            print("\nYou search the area but find nothing of value.")
            input("\nPress Enter to continue...")
    elif choice == "3":
        talk_to_locals(player)
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")

def handle_encounter(player):
    """Process a random encounter during exploration."""
    encounter_types = ["combat", "quest", "special"]
    weights = [0.6, 0.3, 0.1]
    encounter_type = random.choices(encounter_types, weights)[0]
    
    if encounter_type == "combat":
        enemy_count = random.randint(1, min(3, player.level))
        enemies = []
        for i in range(enemy_count):
            enemy_types = ["Goblin", "Bandit", "Wolf", "Skeleton", "Spider"]
            enemy_name = f"{random.choice(enemy_types)} {i+1}"
            enemy = NPC(enemy_name)
            enemy.level = max(1, player.level - 1 + random.randint(-1, 1))
            enemy.stats.update_derived_stats()
            enemies.append(enemy)
        combat = Combat(player, enemies)
        combat.start()
    elif encounter_type == "quest":
        new_quest = generate_quest(player.level, player.location)
        clear_screen()
        print("=== New Quest ===\n")
        print(f"Title: {new_quest.title}")
        typewriter_effect(f"\n{new_quest.description}")
        print(f"\nObjective: {new_quest.get_progress_text()}")
        print(f"Rewards: {new_quest.reward_exp} XP, {new_quest.reward_gold} Gold")
        print("\nDo you accept this quest?")
        print("1. Yes")
        print("2. No")
        choice = input("\nEnter choice (1-2): ")
        if choice == "1":
            player.quests.append(new_quest)
            print("\nQuest accepted!")
            input("\nPress Enter to continue...")
        else:
            print("\nYou declined the quest.")
            input("\nPress Enter to continue...")
    elif encounter_type == "special":
        special_events = [
            "You stumble upon a mysterious shrine that emanates a calming aura.",
            "A wandering merchant offers you rare items at discounted prices.",
            "A sudden celestial event momentarily fills you with inspiration.",
            "You discover a hidden cache of supplies left by an earlier adventurer."
        ]
        event = random.choice(special_events)
        clear_screen()
        print("=== Special Encounter ===\n")
        typewriter_effect(event)
        input("\nPress Enter to continue...")

def talk_to_locals(player):
    """Interact with locals in the current area."""
    clear_screen()
    print("=== Talking to Locals ===\n")
    npc_types = ["Merchant", "Guard", "Farmer", "Scholar", "Adventurer", "Elder"]
    npc_type = random.choice(npc_types)
    npc_names_first = ["Arn", "Bel", "Cor", "Dav", "Ela", "Fio", "Gar", "Hel", "Ivo", "Jor"]
    npc_names_last = ["Smith", "Rivers", "Stone", "Woods", "Hill", "Field", "Storm", "Bright"]
    npc_name = f"{random.choice(npc_names_first)} {random.choice(npc_names_last)}"
    npc = NPC(npc_name)
    npc.location = player.location
    print(f"You encounter a {npc_type} named {npc.name}.")
    conversation_active = True
    while conversation_active:
        print("\nWhat would you like to talk about?")
        print("1. Ask about the area")
        print("2. Ask for rumors")
        print("3. Ask for work")
        print("4. End conversation")
        choice = input("\nEnter your choice (1-4): ")
        if choice == "1":
            print(f"\n{npc.name}: \"{player.location} is known for its beautiful landscapes and hidden dangers.\"")
            input("\nPress Enter to continue...")
        elif choice == "2":
            print(f"\n{npc.name} whispers: \"I've heard that strange creatures roam near the old ruins...\"")
            input("\nPress Enter to continue...")
        elif choice == "3":
            print(f"\n{npc.name} says: \"I might have a task for you if you're willing to take a risk.\"")
            input("\nPress Enter to continue...")
        elif choice == "4":
            print(f"\nYou end the conversation with {npc.name}.")
            conversation_active = False
        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")

def visit_shop(player):
    """Visit a shop to buy or sell items."""
    clear_screen()
    print("=== Shop ===\n")
    shop_inventory = [generate_random_item(player.level) for _ in range(random.randint(5, 10))]
    shopping = True
    while shopping:
        clear_screen()
        print("=== Shop ===\n")
        print(f"Your Gold: {player.gold}")
        print("\nWhat would you like to do?")
        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Leave Shop")
        choice = input("\nEnter your choice (1-3): ")
        if choice == "1":
            print("\nItems available for purchase:")
            for i, item in enumerate(shop_inventory, 1):
                print(f"{i}. {item.name} - {item.value} Gold")
            selection = input(f"\nSelect item to buy (1-{len(shop_inventory)}), or 'b' to go back: ")
            if selection.lower() == 'b':
                continue
            try:
                index = int(selection) - 1
                if 0 <= index < len(shop_inventory):
                    item = shop_inventory[index]
                    if player.gold >= item.value:
                        player.gold -= item.value
                        player.add_to_inventory(item)
                        print(f"\nYou purchased {item.name}!")
                        shop_inventory.pop(index)
                    else:
                        print("\nNot enough gold!")
                else:
                    print("\nInvalid selection!")
            except ValueError:
                print("\nInvalid input!")
            input("\nPress Enter to continue...")
        elif choice == "2":
            if not player.inventory:
                print("\nYour inventory is empty.")
                input("\nPress Enter to continue...")
                continue
            print("\nYour Inventory:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.name} - Sell Price: {int(item.value * 0.5)} Gold")
            selection = input(f"\nSelect item to sell (1-{len(player.inventory)}), or 'b' to go back: ")
            if selection.lower() == 'b':
                continue
            try:
                index = int(selection) - 1
                if 0 <= index < len(player.inventory):
                    item = player.inventory.pop(index)
                    sell_price = int(item.value * 0.5)
                    player.gold += sell_price
                    print(f"\nYou sold {item.name} for {sell_price} Gold!")
                else:
                    print("\nInvalid selection!")
            except ValueError:
                print("\nInvalid input!")
            input("\nPress Enter to continue...")
        elif choice == "3":
            shopping = False
        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")

def rest_at_inn(player):
    """Rest and recover at an inn."""
    clear_screen()
    print("=== Rest at the Inn ===\n")
    cost = 10 + player.level * 2
    print(f"The inn costs {cost} gold for a night's rest.")
    if player.gold >= cost:
        choice = input("Do you want to rest? (y/n): ").lower()
        if choice == "y":
            player.gold -= cost
            print(player.rest())
        else:
            print("You decide not to rest.")
    else:
        print("Not enough gold to rest.")
    input("\nPress Enter to continue...")

def travel(player):
    """Allow the player to travel to a new location."""
    clear_screen()
    print("=== Travel ===\n")
    destinations = ["Eldenvale", "Stormwatch", "Duskridge", "Ironhold", "Whispering Hollow"]
    destinations = [d for d in destinations if d != player.location]
    for i, dest in enumerate(destinations, 1):
        print(f"{i}. {dest}")
    print(f"{len(destinations)+1}. Cancel")
    choice = input(f"\nChoose a destination (1-{len(destinations)+1}): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(destinations):
            new_location = destinations[index]
            print(f"\nTraveling to {new_location}...")
            input("\nPress Enter to continue...")
            return new_location
        else:
            return None
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")
        return None

def manage_quests(player):
    """Display and manage the player's active quests."""
    clear_screen()
    print("=== Quest Log ===\n")
    if not player.quests:
        print("No active quests.")
    else:
        for i, quest in enumerate(player.quests, 1):
            print(f"{i}. {quest.title} - {quest.get_progress_text()}")
            print(f"   Rewards: {quest.reward_exp} XP, {quest.reward_gold} Gold")
    input("\nPress Enter to continue...")

def about_screen():
    """Display information about the game."""
    clear_screen()
    print("=== About This Game ===\n")
    print("Text RPG is a Python-based adventure game featuring both character-driven gameplay")
    print("and an open-world simulation mode.")
    print("\nCreated with passion by your friendly neighborhood developer.")
    input("\nPress Enter to return to the main menu...")

def confirm_action(prompt):
    """Ask the user to confirm an action."""
    print(f"\n{prompt}")
    choice = input("Confirm (y/n): ").lower()
    return choice == "y"

if __name__ == '__main__':
    main_menu()
