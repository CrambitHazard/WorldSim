# Game Configuration Settings

# Display Settings
TYPEWRITER_DELAY = 0.03  # Delay for typewriter effect
CLEAR_SCREEN_ENABLED = True  # Whether to clear screen between menus

# Character Settings
STARTING_GOLD = 50
STARTING_LEVEL = 1
BASE_EXP_TO_NEXT_LEVEL = 100
EXP_MULTIPLIER = 1.5

# Combat Settings
BASE_DAMAGE_MULTIPLIER = 1.0
CRITICAL_HIT_CHANCE = 0.1  # 10% chance
CRITICAL_HIT_MULTIPLIER = 2.0

# Shop Settings
SHOP_ITEM_COUNT_MIN = 5
SHOP_ITEM_COUNT_MAX = 10
SELL_PRICE_MULTIPLIER = 0.5  # Items sell for 50% of their value

# Inn Settings
BASE_INN_COST = 10
INN_COST_PER_LEVEL = 2

# Quest Settings
QUEST_REWARD_BASE_EXP = 50
QUEST_REWARD_EXP_PER_LEVEL = 25
QUEST_REWARD_BASE_GOLD = 20
QUEST_REWARD_GOLD_PER_LEVEL = 10

# World Settings
AVAILABLE_LOCATIONS = [
    "Eldenvale", "Stormwatch", "Duskridge", "Ironhold", "Whispering Hollow"
]

# Simulation Settings
SIMULATION_TICK_RATE = 1.0  # Seconds between simulation updates
MAX_SIMULATION_TICKS = 1000  # Maximum simulation cycles

# Save Settings
SAVE_FILE_EXTENSION = "_save.json"
AUTO_SAVE_ENABLED = False
AUTO_SAVE_INTERVAL = 300  # Seconds

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = False