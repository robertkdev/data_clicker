import tkinter as tk
from tkinter import ttk
from utils.data_calculator import DataCalculator
import random
from gui.data_section import DataSection
from gui.inventory_section import InventorySection
from gui.store_section import StoreSection
from config import STORE_ITEMS
from commands import CommandBox
from utils.item import Item
from utils.store import Store

class DataClickerGame:
    def __init__(self, master, enable_commands=False):
        self.master = master
        self.master.title("Data Clicker")
        self.master.configure(bg='#1e1e1e')

        # Create a main frame to hold all content
        self.main_frame = tk.Frame(master, bg='#1e1e1e')
        self.main_frame.pack(expand=True, fill="both")

        # Configure main frame to center its contents
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Create a header frame
        self.create_header()

        # Initialize values
        self.units = list(DataCalculator.UNIT_FACTORS.keys())  # Reverse order
        self.resources = DataCalculator.calculate_and_distribute(0)  # Initialize resources as a dictionary
        self.generators = {}  # Initialize generators as an empty dictionary
        self.store = Store(self.buy_generator, self.buy_item, self.upgrade_store)
        self.documents = 0  # Initialize document count
        self.inventory = {}  # Initialize inventory as an empty dictionary

        # Create sections
        self.data_section = DataSection(self.main_frame, self.units)
        self.inventory_section = InventorySection(self.main_frame)
        self.store_section = StoreSection(self.main_frame, self.store, self.inventory, self.units)
        self.store_section.update_store_items()  # Add this line

        # Create buttons
        self.create_buttons()

        # Create command box if enabled
        self.command_box = None
        if enable_commands:
            self.command_box = CommandBox(self.main_frame, self.execute_command)

        # Start automatic increment
        self.auto_increment()

    def create_header(self):
        self.header_frame = tk.Frame(self.main_frame, bg='#2c2c2c', height=50)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.header_label = tk.Label(self.header_frame, text="Data Clicker", font=("Helvetica", 24, "bold"), bg='#2c2c2c', fg='#ffffff')
        self.header_label.pack(pady=10)

    def create_buttons(self):
        self.explore_button = tk.Button(self.main_frame, text="Go Explore", command=self.go_explore,
                                        bg='#3a3a3a', fg='#ffffff', font=("Helvetica", 14), activebackground='#4a4a4a', activeforeground='#ffffff')
        self.explore_button.grid(row=2, column=0, columnspan=3, pady=(10, 5), padx=20, sticky="ew")

        self.upload_button = tk.Button(self.main_frame, text="Upload Document", command=self.upload_document,
                                    bg='#3a3a3a', fg='#ffffff', font=("Helvetica", 14), state=tk.DISABLED, activebackground='#4a4a4a', activeforeground='#ffffff')
        self.upload_button.grid(row=3, column=0, columnspan=3, pady=(5, 10), padx=20, sticky="ew")

    def upgrade_store(self, cost_in_bytes):
        if self.buy(cost_in_bytes, 'byte'):
            self.store.upgrade()
            self.store_section.update_store_level(self.store.level)
            return True
        return False

    def buy(self, cost, cost_unit, item_name=None, unit=None):
        cost_in_bits = DataCalculator.convert_to_bits(cost, cost_unit)
        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)

        if total_bits >= cost_in_bits:
            self.resources = DataCalculator.calculate_and_distribute(cost_in_bits, 'subtract')
            if item_name:
                if item_name not in self.inventory:
                    self.inventory[item_name] = 1
                else:
                    self.inventory[item_name] += 1
                print(f"Successfully bought {item_name}.")
            elif unit:
                if unit not in self.generators:
                    self.generators[unit] = 1
                else:
                    self.generators[unit] += 1
            self.update_display()
            self.store_section.update_store_items()
            return True
        else:
            if item_name:
                print(f"Not enough resources to buy {item_name}.")
            elif unit:
                print(f"Not enough resources to buy {unit.capitalize()} Generator.")
            return False

    def buy_generator(self, unit):
        if unit == 'bit':
            cost_unit = 'byte'
            cost = 10  # Define the cost for a bit generator
        elif self.units.index(unit) + 1 < len(self.units):
            cost_unit = self.units[self.units.index(unit) + 1]
            cost = 10
        else:
            print(f"Cannot buy generator for {unit}. No higher unit available.")
            return

        self.buy(cost, cost_unit, unit=unit)

    def buy_item(self, item_name, cost):
        return self.buy(cost, 'byte', item_name=item_name)

    def go_explore(self):
        if random.random() < 0.9:  # 90% chance to find a document
            self.documents += 1
            print("You found a document!")
            
            # Check for zombie brain
            if "Level 1 Sword" in self.inventory and random.random() < 0.02:  # 2% chance with sword
                if "Zombie Brain" not in self.inventory:
                    self.inventory["Zombie Brain"] = 1
                else:
                    self.inventory["Zombie Brain"] += 1
                print("You found a zombie brain!")
        else:
            print("You didn't find anything this time.")
        self.update_display()

    def upload_document(self):
        if self.documents > 0:
            self.documents -= 1
            self.resources = DataCalculator.calculate_and_distribute(1, 'add')  # Add 1 bit
        else:
            print("No documents to upload!")
        self.update_display()

    def auto_increment(self):
        increment = 0
        for unit, count in self.generators.items():
            increment += DataCalculator.convert_to_bits(count, unit)
        self.resources = DataCalculator.calculate_and_distribute(increment, 'add')
        self.update_display()
        self.master.after(1000, self.auto_increment)  # Repeat every second

    def update_display(self):
        # Update only the necessary parts of the UI
        self.data_section.update_display({unit: self.resources[unit] for unit in reversed(self.units)})
        self.inventory_section.update_display(self.generators, self.documents, self.inventory)
        self.upload_button.config(state=tk.NORMAL if self.documents > 0 else tk.DISABLED)
        if self.should_update_store():
            self.store_section.update_store_items()
        self.master.update_idletasks()  # Use update_idletasks instead of update

    def should_update_store(self):
        for item in self.store_section.store_items.values():
            if item.action == self.buy_generator:
                unit = item.name.split()[-2].lower()
                if self.can_afford(item.cost) != (item.button and item.button['state'] == tk.NORMAL):
                    return True
            elif item.action == self.buy_item:
                if self.can_afford(item.cost) != (item.button and item.button['state'] == tk.NORMAL):
                    return True
        return False

    def can_afford(self, cost):
        cost_value, cost_unit = cost.split()
        cost_unit = cost_unit.lower()
        if cost_unit.endswith('s'):  # Handle plural forms
            cost_unit = cost_unit[:-1]
        if cost_unit not in DataCalculator.UNIT_FACTORS:
            print(f"Unknown unit: {cost_unit}")
            return False
        cost_in_bits = DataCalculator.convert_to_bits(float(cost_value), cost_unit)
        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)
        return total_bits >= cost_in_bits

    def execute_command(self, command):
        parts = command.split()
        if len(parts) == 3 and parts[0] == "give":
            try:
                amount = int(parts[1])
                unit = parts[2].lower()
                if unit in self.units:
                    bits_to_add = DataCalculator.convert_to_bits(amount, unit)
                    self.resources = DataCalculator.calculate_and_distribute(bits_to_add, 'add')
                    self.update_display()
                    print(f"Added {amount} {unit} to your resources.")
                else:
                    print(f"Invalid unit: {unit}")
            except ValueError:
                print("Invalid amount. Please enter a number.")
        else:
            print("Invalid command. Use format: give <amount> <unit>")

    def give_data(self, data_type, quantity):
        if data_type not in DataCalculator.UNIT_FACTORS:
            print(f"Unknown data type: {data_type}")
            return

        bits = DataCalculator.convert_to_bits(quantity, data_type)
        self.resources = DataCalculator.calculate_and_distribute(bits, 'add')
        self.update_display()
        print(f"Gave {quantity} {data_type}(s) to the player.")

    def add_to_inventory(self, item_name):
        if item_name not in self.inventory:
            self.inventory[item_name] = 1
        else:
            self.inventory[item_name] += 1
        print(f"Added {item_name} to inventory.")





