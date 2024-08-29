import tkinter as tk
from tkinter import ttk
from data_calculator import DataCalculator
import random

class DataClickerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Clicker")

        # Create a main frame to hold all content
        self.main_frame = tk.Frame(master, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill="both")

        # Configure main frame to center its contents
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Create a header frame
        self.header_frame = tk.Frame(self.main_frame, bg='#4a7abc', height=50)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.header_label = tk.Label(self.header_frame, text="Data Clicker", font=("Helvetica", 24, "bold"), bg='#4a7abc', fg='white')
        self.header_label.pack(pady=10)

        # Initialize values
        self.units = list(DataCalculator.UNIT_FACTORS.keys())[::-1]  # Reverse order
        self.resources = DataCalculator.calculate_and_distribute(0)  # Initialize resources as a dictionary
        self.generators = {}  # Initialize generators as an empty dictionary
        self.store_level = 1
        self.documents = 0  # Initialize document count
        self.inventory = {}  # Initialize inventory as an empty dictionary

        self.store_items = {
            2: [
                {"name": "Buy Bit Generator", "cost": "10 Bytes", "action": lambda: self.buy_generator("bit")},
                {"name": "Buy Level 1 Sword", "cost": "5 Bytes", "action": lambda: self.buy_item("Level 1 Sword", 5)},
                {"name": "Upgrade Store", "cost": "100 Bytes", "action": self.upgrade_store}
            ]
            # ... other store levels ...
        }

        # Create data section (left side)
        self.create_data_section()

        # Create inventory section (middle)
        self.create_inventory_section()

        # Create store section (right side)
        self.create_store_section()

        # Create button to go explore
        self.explore_button = tk.Button(self.main_frame, text="Go Explore", command=self.go_explore,
                                        bg='#FFA500', fg='white', font=("Helvetica", 14))
        self.explore_button.grid(row=2, column=0, columnspan=3, pady=(10, 5), padx=20, sticky="ew")

        # Create button to upload document (adds 1 bit)
        self.upload_button = tk.Button(self.main_frame, text="Upload Document", command=self.upload_document,
                                       bg='#008CBA', fg='white', font=("Helvetica", 14), state=tk.DISABLED)
        self.upload_button.grid(row=3, column=0, columnspan=3, pady=(5, 10), padx=20, sticky="ew")

        # Start automatic increment
        self.auto_increment()

    def create_data_section(self):
        # Create a frame for the data section
        self.data_frame = tk.Frame(self.main_frame, bg='white', bd=2, relief=tk.GROOVE)
        self.data_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Add a header to the data section
        self.data_header = tk.Label(self.data_frame, text="Data Storage", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.data_header.pack(fill="x", pady=(0, 10))

        # Create a canvas and scrollbar for the data section
        self.canvas = tk.Canvas(self.data_frame, bg='white')
        self.scrollbar = tk.Scrollbar(self.data_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create labels for each unit
        self.labels = []
        for i, name in enumerate(self.units):
            label = tk.Label(self.scrollable_frame, text=f"{name.capitalize()}: 0", font=("Helvetica", 12), bg='white')
            label.pack(pady=5, padx=10, anchor="w")
            self.labels.append(label)

    def create_inventory_section(self):
        # Create a frame for the inventory section
        self.inventory_frame = tk.Frame(self.main_frame, bg='#e6e6e6', bd=2, relief=tk.GROOVE)
        self.inventory_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        # Add a header to the inventory section
        self.inventory_header = tk.Label(self.inventory_frame, text="Inventory", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.inventory_header.pack(fill="x", pady=(0, 10))

        # Create a canvas and scrollbar for the inventory section
        self.inventory_canvas = tk.Canvas(self.inventory_frame, bg='#e6e6e6')
        self.inventory_scrollbar = tk.Scrollbar(self.inventory_frame, orient="vertical", command=self.inventory_canvas.yview)
        self.inventory_scrollable_frame = tk.Frame(self.inventory_canvas, bg='#e6e6e6')

        self.inventory_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.inventory_canvas.configure(
                scrollregion=self.inventory_canvas.bbox("all")
            )
        )

        self.inventory_canvas.create_window((0, 0), window=self.inventory_scrollable_frame, anchor="nw")
        self.inventory_canvas.configure(yscrollcommand=self.inventory_scrollbar.set)

        self.inventory_canvas.pack(side="left", fill="both", expand=True)
        self.inventory_scrollbar.pack(side="right", fill="y")

        # Create a label for empty inventory
        self.empty_inventory_label = tk.Label(self.inventory_scrollable_frame, font=("Helvetica", 12), bg='#e6e6e6')
        self.empty_inventory_label.pack(pady=5, padx=10, anchor="w")

        # Dictionary to store generator labels
        self.generator_labels = {}

    def create_store_section(self):
        # Create a frame for the store section
        self.store_frame = tk.Frame(self.main_frame, bg='#e6e6e6', bd=2, relief=tk.GROOVE)
        self.store_frame.grid(row=1, column=2, sticky="nsew", padx=20, pady=20)

        # Add a header to the store section
        self.store_header = tk.Label(self.store_frame, text=f"Store (Level {self.store_level})", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.store_header.pack(fill="x", pady=(0, 10))

        # Create a frame for store items
        self.store_items_frame = tk.Frame(self.store_frame, bg='#e6e6e6')
        self.store_items_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_store_items()

    def update_store_items(self):
        # Clear existing store items
        for widget in self.store_items_frame.winfo_children():
            widget.destroy()

        if self.store_level in self.store_items:
            for item in self.store_items[self.store_level]:
                if item["name"] != "Buy Level 1 Sword" or "Level 1 Sword" not in self.inventory:
                    self.create_store_item(item["name"], item["cost"], item["action"])

        # Always add the option to upgrade the store
        if self.store_level < 5:  # Assuming 5 is the maximum store level
            upgrade_cost = self.get_store_upgrade_cost()
            self.create_store_item("Upgrade Store", f"{upgrade_cost} Bytes", self.upgrade_store)

    def get_store_upgrade_cost(self):
        # Define the upgrade costs for each level
        upgrade_costs = {1: 10, 2: 100, 3: 1000, 4: 10000}
        return upgrade_costs.get(self.store_level, "N/A")

    def create_store_item(self, name, cost, command):
        frame = tk.Frame(self.store_items_frame, bg='#f0f0f0', bd=1, relief=tk.RAISED)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=name, font=("Helvetica", 12), bg='#f0f0f0')
        label.pack(side="left", padx=10, pady=5)

        button = tk.Button(frame, text=f"Buy ({cost})", command=command, bg='#4CAF50', fg='white')
        button.pack(side="right", padx=10, pady=5)

    def upgrade_store(self):
        cost_in_bits = DataCalculator.convert_to_bits(10 * (10 ** (self.store_level - 1)), 'byte')
        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)

        if total_bits >= cost_in_bits:
            self.resources = DataCalculator.calculate_and_distribute(cost_in_bits, 'subtract')
            self.store_level += 1
            self.store_header.config(text=f"Store (Level {self.store_level})")
            self.update_store_items()
            self.update_display()
        else:
            print("Not enough resources to upgrade the store.")

    def buy_generator(self, unit):
        cost_unit = self.units[self.units.index(unit) + 1]
        cost = 10
        cost_in_bits = DataCalculator.convert_to_bits(cost, cost_unit)

        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)

        if total_bits >= cost_in_bits:
            self.resources = DataCalculator.calculate_and_distribute(cost_in_bits, 'subtract')
            if unit not in self.generators:
                self.generators[unit] = 1
            else:
                self.generators[unit] += 1
            self.update_display()
            print(f"Successfully bought {unit.capitalize()} Generator.")
        else:
            print(f"Not enough resources to buy {unit.capitalize()} Generator.")

    def buy_item(self, item_name, cost):
        cost_in_bits = DataCalculator.convert_to_bits(cost, 'byte')
        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)

        if total_bits >= cost_in_bits:
            self.resources = DataCalculator.calculate_and_distribute(cost_in_bits, 'subtract')
            if item_name not in self.inventory:
                self.inventory[item_name] = 1
            else:
                self.inventory[item_name] += 1
            self.update_display()
            self.update_store_items()  # Update store items after purchase
            print(f"Successfully bought {item_name}.")
        else:
            print(f"Not enough resources to buy {item_name}.")

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
            print("Document uploaded successfully!")
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
        # Update data storage display
        for i, unit in enumerate(self.units):
            value = self.resources.get(unit, 0)
            self.labels[i].config(text=f"{unit.capitalize()}: {value}")

        # Update inventory display
        for widget in self.inventory_scrollable_frame.winfo_children():
            widget.destroy()

        self.generator_labels = {}  # Reset the generator_labels dictionary

        if not self.generators and self.documents == 0 and not self.inventory:
            self.empty_inventory_label = tk.Label(self.inventory_scrollable_frame, font=("Helvetica", 12), bg='#e6e6e6')
            self.empty_inventory_label.pack(pady=5, padx=10, anchor="w")
        else:
            if self.documents > 0:
                doc_label = tk.Label(self.inventory_scrollable_frame, text=f"Documents: {self.documents}", font=("Helvetica", 12), bg='#e6e6e6')
                doc_label.pack(pady=5, padx=10, anchor="w")
            
            for unit, count in self.generators.items():
                label = tk.Label(self.inventory_scrollable_frame, text=f"{unit.capitalize()} Generators: {count}", font=("Helvetica", 12), bg='#e6e6e6')
                label.pack(pady=5, padx=10, anchor="w")
                self.generator_labels[unit] = label

            for item, count in self.inventory.items():
                label = tk.Label(self.inventory_scrollable_frame, text=f"{item}: {count}", font=("Helvetica", 12), bg='#e6e6e6')
                label.pack(pady=5, padx=10, anchor="w")

        # Update upload button state
        self.upload_button.config(state=tk.NORMAL if self.documents > 0 else tk.DISABLED)

        # Update store items
        self.update_store_items()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x650")  # Increased height to accommodate the new button
    app = DataClickerGame(root)
    root.mainloop()
