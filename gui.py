# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# Import game modules (make sure these are in your project)
from game_state import GameState
from character import PlayerCharacter, create_character
from simulation import WorldSimulation
from utils import clear_screen, typewriter_effect

# Global variable for the game state
game_state = None

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Text RPG - Main Menu")
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Text RPG", font=("Helvetica", 24)).pack(pady=20)
        
        btn_char_mode = tk.Button(self, text="New Character Mode Game", font=("Helvetica", 14),
                                   command=self.start_character_mode)
        btn_char_mode.pack(pady=5)
        
        btn_sim_mode = tk.Button(self, text="New Simulation Mode", font=("Helvetica", 14),
                                  command=self.start_simulation_mode)
        btn_sim_mode.pack(pady=5)
        
        btn_load = tk.Button(self, text="Load Game", font=("Helvetica", 14),
                             command=self.load_game_menu)
        btn_load.pack(pady=5)
        
        btn_about = tk.Button(self, text="About", font=("Helvetica", 14),
                              command=self.show_about)
        btn_about.pack(pady=5)
        
        btn_quit = tk.Button(self, text="Quit", font=("Helvetica", 14),
                             command=self.master.quit)
        btn_quit.pack(pady=5)

    def start_character_mode(self):
        # For now, we’ll launch character mode by creating a new player and launching
        # a simulation window that shows that character’s details (or you can create your own window)
        global game_state
        player = create_character()
        game_state = GameState(player=player, world=None)
        self.destroy()
        CharacterMode(self.master, game_state)

    def start_simulation_mode(self):
        global game_state
        # Create a new simulation world using your existing logic.
        world = WorldSimulation()
        # For simplicity, we prompt in a simple dialog or select defaults:
        # Here we use default parameters; in a full implementation, you can add more dialogs.
        world.create_world(size="medium", complexity="medium")
        game_state = GameState(world=world)
        self.destroy()
        SimulationMode(self.master, game_state)

    def load_game_menu(self):
        # Let the user select a save file
        filename = filedialog.askopenfilename(title="Select Save File",
                                              filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        if filename:
            from utils import load_game  # our load_game function returns player, world, message
            player, world, msg = load_game(filename)
            messagebox.showinfo("Load Game", msg)
            global game_state
            game_state = GameState(player=player, world=world)
            if world:
                self.destroy()
                SimulationMode(self.master, game_state)
            else:
                self.destroy()
                CharacterMode(self.master, game_state)

    def show_about(self):
        about_text = (
            "Text RPG is a Python-based adventure game featuring both\n"
            "character-driven gameplay and an open-world simulation mode.\n"
            "\nCreated with passion by your friendly neighborhood developer."
        )
        messagebox.showinfo("About Text RPG", about_text)

class CharacterMode(tk.Frame):
    """
    A simple window that displays the player's character info.
    (You can expand this to include exploration, combat, and more.)
    """
    def __init__(self, master, state: GameState):
        super().__init__(master)
        self.state = state
        self.master.title("Text RPG - Character Mode")
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Display a simple character sheet
        header = tk.Label(self, text="Character Mode", font=("Helvetica", 20))
        header.pack(pady=10)
        
        char_sheet = tk.Text(self, width=80, height=20)
        char_sheet.pack(pady=10)
        # Display the player's character dictionary data nicely formatted.
        player_data = json.dumps(self.state.player.to_dict(), indent=2)
        char_sheet.insert("end", player_data)
        char_sheet.configure(state="disabled")
        
        btn_back = tk.Button(self, text="Back to Main Menu", command=self.back_to_menu)
        btn_back.pack(pady=10)

    def back_to_menu(self):
        self.destroy()
        MainMenu(self.master)

class SimulationMode(tk.Frame):
    """
    The Simulation Mode window displays simulation world data.
    You can run simulation ticks, view world status, and inspect individual NPCs.
    """
    def __init__(self, master, state: GameState):
        super().__init__(master)
        self.state = state
        self.master.title("Text RPG - Simulation Mode")
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.update_npc_list()

    def create_widgets(self):
        # Top frame for simulation controls
        controls_frame = tk.Frame(self)
        controls_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        btn_tick = tk.Button(controls_frame, text="Run 1 Tick", command=self.run_tick)
        btn_tick.pack(side="left", padx=5)
        
        btn_run_year = tk.Button(controls_frame, text="Run 1 Year", command=lambda: self.run_ticks(4))
        btn_run_year.pack(side="left", padx=5)
        
        btn_save = tk.Button(controls_frame, text="Save Simulation", command=self.save_simulation)
        btn_save.pack(side="left", padx=5)
        
        btn_world_status = tk.Button(controls_frame, text="World Status", command=self.show_world_status)
        btn_world_status.pack(side="left", padx=5)
        
        btn_back = tk.Button(controls_frame, text="Main Menu", command=self.back_to_menu)
        btn_back.pack(side="right", padx=5)
        
        # Left frame for NPC list
        npc_frame = tk.Frame(self)
        npc_frame.pack(side="left", fill="y", padx=10, pady=5)
        tk.Label(npc_frame, text="NPC List", font=("Helvetica", 14)).pack()
        self.npc_listbox = tk.Listbox(npc_frame, width=30)
        self.npc_listbox.pack(padx=5, pady=5, fill="y")
        self.npc_listbox.bind("<<ListboxSelect>>", self.show_npc_details)
        
        # Right frame for NPC details
        details_frame = tk.Frame(self)
        details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        tk.Label(details_frame, text="NPC Details", font=("Helvetica", 14)).pack()
        self.npc_details_text = tk.Text(details_frame, width=60, height=20)
        self.npc_details_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.npc_details_text.configure(state="disabled")
        
        # Bottom frame for simulation events
        events_frame = tk.Frame(self)
        events_frame.pack(side="bottom", fill="both", padx=10, pady=5)
        tk.Label(events_frame, text="Recent Events", font=("Helvetica", 14)).pack()
        self.events_text = tk.Text(events_frame, width=80, height=8)
        self.events_text.pack(fill="both", padx=5, pady=5)
        self.events_text.configure(state="disabled")

    def update_npc_list(self):
        """Refresh the NPC list from the simulation world."""
        self.npc_listbox.delete(0, tk.END)
        world = self.state.world
        for npc in world.npcs:
            self.npc_listbox.insert(tk.END, npc.name)

    def show_npc_details(self, event):
        """Display detailed info for the selected NPC."""
        selection = self.npc_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        npc = self.state.world.npcs[index]
        details = f"Name: {npc.name}\n"
        details += f"Race: {npc.race}\n"
        details += f"Class: {npc.character_class}\n"
        details += f"Level: {npc.level}\n"
        details += f"HP: {npc.stats.health}/{npc.stats.max_health}\n"
        details += f"Mana: {npc.stats.mana}/{npc.stats.max_mana}\n"
        details += f"Resources: {npc.resources}\n"
        details += f"Territory: {npc.territory}\n"
        details += f"Ambition: {npc.ambition}\n"
        details += f"Aggression: {npc.aggression}\n"
        details += f"Altruism: {npc.altruism}\n"
        details += f"Current Action: {npc.current_action}\n"
        details += "\nRelationships:\n"
        for other, val in npc.relationships.items():
            details += f"  {other}: {val}\n"
        self.npc_details_text.configure(state="normal")
        self.npc_details_text.delete(1.0, tk.END)
        self.npc_details_text.insert(tk.END, details)
        self.npc_details_text.configure(state="disabled")

    def run_tick(self):
        """Run one simulation tick and update the display."""
        self.state.world.run_simulation(ticks=1, display_results=False)
        self.update_events_display()
        self.update_npc_list()

    def run_ticks(self, n):
        """Run multiple simulation ticks."""
        self.state.world.run_simulation(ticks=n, display_results=False)
        self.update_events_display()
        self.update_npc_list()

    def update_events_display(self):
        """Display the last few events from the simulation."""
        events = self.state.world.event_history[-10:]
        self.events_text.configure(state="normal")
        self.events_text.delete(1.0, tk.END)
        for event in events:
            self.events_text.insert(tk.END, f"{event}\n")
        self.events_text.configure(state="disabled")

    def save_simulation(self):
        """Save the current simulation using the GameState save method."""
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            msg = self.state.save(filename)
            messagebox.showinfo("Save Simulation", msg)

    def show_world_status(self):
        """Show world status in a new popup."""
        status = f"Year: {self.state.world.current_year}\nSeason: {self.state.world.current_season}\n"
        status += f"Factions: {len(self.state.world.factions)}\nNPCs: {len(self.state.world.npcs)}\nLocations: {len(self.state.world.locations)}\n"
        messagebox.showinfo("World Status", status)

    def back_to_menu(self):
        self.destroy()
        MainMenu(self.master)

def main():
    root = tk.Tk()
    root.geometry("900x600")
    app = MainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
