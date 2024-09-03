import tkinter as tk
from config import STORE_ITEMS
from utils.item import Item

class StoreSection:
    def __init__(self, parent, store, inventory, units):
        self.parent = parent
        self.store = store
        self.inventory = inventory
        self.units = units
        self.store_items = {}
        self.create_store_frame()

    def create_store_frame(self):
        self.frame = tk.Frame(self.parent, bg='#2c2c2c', bd=2, relief=tk.GROOVE)
        self.frame.grid(row=1, column=2, sticky="nsew", padx=20, pady=20)

        self.create_header()
        self.create_items_frame()

    def create_header(self):
        self.header = tk.Label(self.frame, text=f"Store (Level {self.store.level})", font=("Helvetica", 16, "bold"), bg='#3a3a3a', fg='#ffffff')
        self.header.pack(fill="x", pady=(0, 10))

    def create_items_frame(self):
        self.items_frame = tk.Frame(self.frame, bg='#2c2c2c')
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_store_item(self, item):
        if isinstance(item, Item):
            item.button = None  # Initialize button attribute
            self.store_items[item.name] = item
        else:
            print(f"Invalid item: {item}")

    def update_store_items(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        for item in self.store.get_items():
            self.create_store_item(item)

    def create_store_item(self, item):
        frame = tk.Frame(self.items_frame, bg='#3a3a3a', bd=1, relief=tk.RAISED)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=item.name, bg='#3a3a3a', fg='#ffffff', font=("Helvetica", 12))
        label.pack(side="left", padx=10, pady=5)

        button = tk.Button(frame, text=f"Buy ({item.cost})", command=lambda: self.handle_purchase(item), bg='#4CAF50', fg='#ffffff', activebackground='#45a049', activeforeground='#ffffff')
        button.pack(side="right", padx=10, pady=5)
        item.button = button  # Store the button reference in the item object

    def handle_purchase(self, item):
        if item.action:
            if item.name == "Upgrade Store":
                self.store.upgrade()
            elif item.spammable:
                item.action(item.name.split()[-2].lower())
            elif item.action == self.store.buy_generator:
                item.action(item.name.split()[-2].lower())
            else:
                item.action(item.name, int(item.cost.split()[0]))
        else:
            print(f"No action defined for {item.name}")

        if item.add_to_inventory:
            self.store.buy_item(item.name, int(item.cost.split()[0]))

        if not item.spammable:
            self.store.remove_item(item.name)

        self.update_store_items()

    def update_store_level(self, new_level):
        self.header.config(text=f"Store (Level {new_level})")
        self.update_store_items()