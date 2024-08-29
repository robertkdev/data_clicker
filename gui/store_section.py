import tkinter as tk
from config import STORE_ITEMS, STORE_UPGRADE_COSTS

class StoreSection:
    def __init__(self, parent, store_level, buy_generator, buy_item, upgrade_store, inventory, units):
        self.parent = parent
        self.store_level = store_level
        self.buy_generator = buy_generator
        self.original_buy_item = buy_item
        self.upgrade_store = upgrade_store
        self.inventory = inventory
        self.units = units
        self.create_store_frame()
        self.update_store_items()

    def create_store_frame(self):
        self.frame = tk.Frame(self.parent, bg='#e6e6e6', bd=2, relief=tk.GROOVE)
        self.frame.grid(row=1, column=2, sticky="nsew", padx=20, pady=20)

        self.create_header()
        self.create_items_frame()

    def create_header(self):
        self.header = tk.Label(self.frame, text=f"Store (Level {self.store_level})", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.header.pack(fill="x", pady=(0, 10))

    def create_items_frame(self):
        self.items_frame = tk.Frame(self.frame, bg='#e6e6e6')
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def update_store_level(self, new_level):
        self.store_level = new_level
        self.header.config(text=f"Store (Level {self.store_level})")
        self.update_store_items()

    def update_store_items(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        if self.store_level in STORE_ITEMS:
            for item in STORE_ITEMS[self.store_level]:
                if item["name"] == "Buy Level 1 Sword":
                    if "Level 1 Sword" not in self.inventory:
                        self.create_store_item(item["name"], item["cost"], self.buy_item_wrapper)
                else:
                    self.create_store_item(item["name"], item["cost"], getattr(self, item["action"]))

        if self.store_level < 5:  # Assuming 5 is the maximum store level
            upgrade_cost = STORE_UPGRADE_COSTS[self.store_level]
            self.create_store_item("Upgrade Store", f"{upgrade_cost} Bytes", self.upgrade_store)

    def create_store_item(self, name, cost, command):
        frame = tk.Frame(self.items_frame, bg='#f0f0f0', bd=1, relief=tk.RAISED)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=name, font=("Helvetica", 12), bg='#f0f0f0')
        label.pack(side="left", padx=10, pady=5)

        numeric_cost = int(cost.split()[0])  # Extract numeric part of the cost

        if command == self.upgrade_store:
            button = tk.Button(frame, text=f"Buy ({cost})", command=command, bg='#4CAF50', fg='white')
        elif command == self.buy_generator:
            unit = name.split()[1].lower()
            if unit in self.units:
                button = tk.Button(frame, text=f"Buy ({cost})", command=lambda: command(unit), bg='#4CAF50', fg='white')
            else:
                print(f"Invalid unit: {unit}")
                return
        else:
            button = tk.Button(frame, text=f"Buy ({cost})", command=lambda: command(name, numeric_cost), bg='#4CAF50', fg='white')
        
        button.pack(side="right", padx=10, pady=5)

    def buy_item_wrapper(self, name, cost):
        result = self.original_buy_item(name, cost)
        print(f"buy_item_wrapper: {name}, {cost}, result: {result}")  # Debug print statement
        if result and name == "Buy Level 1 Sword":
            self.inventory["Level 1 Sword"] = 1
            self.update_store_items()  # Refresh the store display
        return result