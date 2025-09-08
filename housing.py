# housing.py
import random
from items import Item

class Room:
    """Represents a room in a house."""
    def __init__(self, name, size, cost, description):
        self.name = name
        self.size = size  # Small, Medium, Large
        self.cost = cost
        self.description = description
        self.furniture = []
        self.decorations = []
        self.functionality = {}
    
    def add_furniture(self, furniture):
        """Add furniture to the room."""
        self.furniture.append(furniture)
    
    def add_decoration(self, decoration):
        """Add decoration to the room."""
        self.decorations.append(decoration)
    
    def get_bonus(self, bonus_type):
        """Get bonus provided by this room."""
        total_bonus = 0
        for furniture in self.furniture:
            if hasattr(furniture, 'bonuses') and bonus_type in furniture.bonuses:
                total_bonus += furniture.bonuses[bonus_type]
        return total_bonus
    
    def to_dict(self):
        """Convert room to dictionary."""
        return {
            "name": self.name,
            "size": self.size,
            "cost": self.cost,
            "description": self.description,
            "furniture": [f.to_dict() for f in self.furniture],
            "decorations": [d.to_dict() for d in self.decorations],
            "functionality": self.functionality
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create room from dictionary."""
        room = cls(data["name"], data["size"], data["cost"], data["description"])
        room.furniture = [Item.from_dict(f) for f in data.get("furniture", [])]
        room.decorations = [Item.from_dict(d) for d in data.get("decorations", [])]
        room.functionality = data.get("functionality", {})
        return room

class House:
    """Represents a player's house."""
    def __init__(self, name="My House", location="Starting Village"):
        self.name = name
        self.location = location
        self.rooms = []
        self.storage_capacity = 50
        self.rest_bonus = 0
        self.crafting_bonus = 0
        self.total_value = 0
    
    def add_room(self, room):
        """Add a room to the house."""
        self.rooms.append(room)
        self.total_value += room.cost
        self.update_bonuses()
    
    def remove_room(self, room_name):
        """Remove a room from the house."""
        for room in self.rooms:
            if room.name == room_name:
                self.rooms.remove(room)
                self.total_value -= room.cost
                self.update_bonuses()
                return True
        return False
    
    def update_bonuses(self):
        """Update house-wide bonuses based on rooms and furniture."""
        self.rest_bonus = 0
        self.crafting_bonus = 0
        self.storage_capacity = 50
        
        for room in self.rooms:
            # Storage bonus from storage rooms
            if "storage" in room.name.lower():
                self.storage_capacity += 20
            
            # Rest bonus from bedrooms and living areas
            if any(keyword in room.name.lower() for keyword in ["bedroom", "bed", "living", "lounge"]):
                self.rest_bonus += room.get_bonus("rest_bonus")
            
            # Crafting bonus from workshops
            if any(keyword in room.name.lower() for keyword in ["workshop", "forge", "laboratory", "study"]):
                self.crafting_bonus += room.get_bonus("crafting_bonus")
    
    def get_room_by_name(self, name):
        """Get a room by name."""
        for room in self.rooms:
            if room.name == name:
                return room
        return None
    
    def display_house_info(self):
        """Display information about the house."""
        print(f"\n=== {self.name} ===")
        print(f"Location: {self.location}")
        print(f"Total Value: {self.total_value} gold")
        print(f"Storage Capacity: {self.storage_capacity}")
        print(f"Rest Bonus: +{self.rest_bonus} health/mana recovery")
        print(f"Crafting Bonus: +{self.crafting_bonus} success chance")
        
        print(f"\nRooms ({len(self.rooms)}):")
        for room in self.rooms:
            print(f"- {room.name} ({room.size})")
            if room.furniture:
                print(f"  Furniture: {', '.join([f.name for f in room.furniture])}")
            if room.decorations:
                print(f"  Decorations: {', '.join([d.name for d in room.decorations])}")
    
    def to_dict(self):
        """Convert house to dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "rooms": [room.to_dict() for room in self.rooms],
            "storage_capacity": self.storage_capacity,
            "rest_bonus": self.rest_bonus,
            "crafting_bonus": self.crafting_bonus,
            "total_value": self.total_value
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create house from dictionary."""
        house = cls(data["name"], data["location"])
        house.rooms = [Room.from_dict(room_data) for room_data in data.get("rooms", [])]
        house.storage_capacity = data.get("storage_capacity", 50)
        house.rest_bonus = data.get("rest_bonus", 0)
        house.crafting_bonus = data.get("crafting_bonus", 0)
        house.total_value = data.get("total_value", 0)
        return house

class HousingSystem:
    """Manages the housing system."""
    
    def __init__(self):
        self.available_rooms = self.initialize_rooms()
        self.available_furniture = self.initialize_furniture()
        self.available_decorations = self.initialize_decorations()
    
    def initialize_rooms(self):
        """Initialize available room types."""
        rooms = [
            Room("Bedroom", "Medium", 100, "A comfortable bedroom for rest and recovery"),
            Room("Kitchen", "Small", 80, "A kitchen for cooking and food preparation"),
            Room("Living Room", "Large", 150, "A spacious living area for relaxation"),
            Room("Workshop", "Medium", 200, "A workshop for crafting and repairs"),
            Room("Storage Room", "Small", 60, "A room for storing items and materials"),
            Room("Study", "Small", 120, "A quiet study for magical research and learning"),
            Room("Forge", "Medium", 250, "A blacksmith's forge for metalworking"),
            Room("Laboratory", "Medium", 300, "An alchemy laboratory for potion making"),
            Room("Library", "Large", 400, "A library filled with books and knowledge"),
            Room("Garden", "Large", 180, "A peaceful garden for meditation and growth"),
        ]
        return rooms
    
    def initialize_furniture(self):
        """Initialize available furniture."""
        furniture = [
            Item("Bed", "A comfortable bed for rest", 50, "furniture", {"rest_bonus": 10}),
            Item("Workbench", "A sturdy workbench for crafting", 80, "furniture", {"crafting_bonus": 5}),
            Item("Bookshelf", "A shelf filled with books", 60, "furniture", {"intelligence": 2}),
            Item("Forge", "A blacksmith's forge", 150, "furniture", {"crafting_bonus": 10}),
            Item("Alchemy Table", "A table for alchemical experiments", 120, "furniture", {"crafting_bonus": 8}),
            Item("Armchair", "A comfortable chair for relaxation", 40, "furniture", {"rest_bonus": 5}),
            Item("Storage Chest", "A large chest for storing items", 70, "furniture", {"storage_bonus": 20}),
            Item("Mirror", "A decorative mirror", 30, "furniture", {"charisma": 1}),
            Item("Fireplace", "A warm fireplace", 100, "furniture", {"rest_bonus": 8}),
            Item("Training Dummy", "A dummy for combat practice", 90, "furniture", {"strength": 2}),
        ]
        return furniture
    
    def initialize_decorations(self):
        """Initialize available decorations."""
        decorations = [
            Item("Painting", "A beautiful painting", 40, "decoration", {"charisma": 1}),
            Item("Rug", "A soft rug", 25, "decoration", {"rest_bonus": 2}),
            Item("Plant", "A potted plant", 20, "decoration", {"wisdom": 1}),
            Item("Candle", "A scented candle", 15, "decoration", {"rest_bonus": 1}),
            Item("Tapestry", "A decorative tapestry", 50, "decoration", {"charisma": 2}),
            Item("Crystal", "A magical crystal", 80, "decoration", {"intelligence": 1}),
            Item("Fountain", "A small indoor fountain", 120, "decoration", {"wisdom": 2}),
            Item("Statue", "A decorative statue", 100, "decoration", {"charisma": 3}),
        ]
        return decorations
    
    def show_housing_menu(self, player):
        """Display the housing menu."""
        if not hasattr(player, 'house'):
            player.house = House()
        
        while True:
            print("\n=== HOUSING MENU ===")
            print("1. View House")
            print("2. Build Room")
            print("3. Add Furniture")
            print("4. Add Decoration")
            print("5. Rest at Home")
            print("6. Back")
            
            choice = input("\nChoose option: ")
            
            if choice == "1":
                player.house.display_house_info()
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.build_room(player)
            elif choice == "3":
                self.add_furniture(player)
            elif choice == "4":
                self.add_decoration(player)
            elif choice == "5":
                self.rest_at_home(player)
            elif choice == "6":
                break
            else:
                print("Invalid choice!")
    
    def build_room(self, player):
        """Build a new room."""
        print("\n=== BUILD ROOM ===")
        print("Available rooms:")
        
        for i, room in enumerate(self.available_rooms):
            print(f"{i+1}. {room.name} - {room.size} - {room.cost} gold")
            print(f"   {room.description}")
        
        print(f"{len(self.available_rooms)+1}. Back")
        
        try:
            choice = int(input("\nChoose room to build: ")) - 1
            if choice == len(self.available_rooms):
                return
            elif 0 <= choice < len(self.available_rooms):
                room = self.available_rooms[choice]
                
                if player.gold >= room.cost:
                    # Create a copy of the room
                    new_room = Room(room.name, room.size, room.cost, room.description)
                    player.house.add_room(new_room)
                    player.gold -= room.cost
                    print(f"\nBuilt {room.name} for {room.cost} gold!")
                else:
                    print(f"\nNot enough gold! Need {room.cost} gold.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def add_furniture(self, player):
        """Add furniture to a room."""
        if not player.house.rooms:
            print("You need to build a room first!")
            return
        
        print("\n=== ADD FURNITURE ===")
        print("Available furniture:")
        
        for i, furniture in enumerate(self.available_furniture):
            print(f"{i+1}. {furniture.name} - {furniture.value} gold")
            print(f"   {furniture.description}")
        
        print(f"{len(self.available_furniture)+1}. Back")
        
        try:
            choice = int(input("\nChoose furniture: ")) - 1
            if choice == len(self.available_furniture):
                return
            elif 0 <= choice < len(self.available_furniture):
                furniture = self.available_furniture[choice]
                
                if player.gold >= furniture.value:
                    # Choose room to add furniture to
                    print("\nChoose room:")
                    for i, room in enumerate(player.house.rooms):
                        print(f"{i+1}. {room.name}")
                    
                    room_choice = int(input("Enter room number: ")) - 1
                    if 0 <= room_choice < len(player.house.rooms):
                        room = player.house.rooms[room_choice]
                        room.add_furniture(furniture)
                        player.gold -= furniture.value
                        player.house.update_bonuses()
                        print(f"\nAdded {furniture.name} to {room.name}!")
                    else:
                        print("Invalid room choice!")
                else:
                    print(f"\nNot enough gold! Need {furniture.value} gold.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def add_decoration(self, player):
        """Add decoration to a room."""
        if not player.house.rooms:
            print("You need to build a room first!")
            return
        
        print("\n=== ADD DECORATION ===")
        print("Available decorations:")
        
        for i, decoration in enumerate(self.available_decorations):
            print(f"{i+1}. {decoration.name} - {decoration.value} gold")
            print(f"   {decoration.description}")
        
        print(f"{len(self.available_decorations)+1}. Back")
        
        try:
            choice = int(input("\nChoose decoration: ")) - 1
            if choice == len(self.available_decorations):
                return
            elif 0 <= choice < len(self.available_decorations):
                decoration = self.available_decorations[choice]
                
                if player.gold >= decoration.value:
                    # Choose room to add decoration to
                    print("\nChoose room:")
                    for i, room in enumerate(player.house.rooms):
                        print(f"{i+1}. {room.name}")
                    
                    room_choice = int(input("Enter room number: ")) - 1
                    if 0 <= room_choice < len(player.house.rooms):
                        room = player.house.rooms[room_choice]
                        room.add_decoration(decoration)
                        player.gold -= decoration.value
                        print(f"\nAdded {decoration.name} to {room.name}!")
                    else:
                        print("Invalid room choice!")
                else:
                    print(f"\nNot enough gold! Need {decoration.value} gold.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def rest_at_home(self, player):
        """Rest at home with bonus recovery."""
        if not player.house.rooms:
            print("You need to build a room first!")
            return
        
        rest_cost = 5  # Cost to rest at home
        if player.gold >= rest_cost:
            player.gold -= rest_cost
            
            # Calculate recovery with house bonus
            health_recovery = 20 + player.house.rest_bonus
            mana_recovery = 15 + player.house.rest_bonus
            
            old_health = player.stats.health
            old_mana = player.stats.mana
            
            player.stats.health = min(player.stats.max_health, player.stats.health + health_recovery)
            player.stats.mana = min(player.stats.max_mana, player.stats.mana + mana_recovery)
            
            actual_health_gain = player.stats.health - old_health
            actual_mana_gain = player.stats.mana - old_mana
            
            print(f"\nYou rest at home for {rest_cost} gold.")
            print(f"Recovered {actual_health_gain} health and {actual_mana_gain} mana.")
            print(f"House rest bonus: +{player.house.rest_bonus}")
        else:
            print(f"Not enough gold! Need {rest_cost} gold to rest at home.")