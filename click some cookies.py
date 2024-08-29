import tkinter as tk
from tkinter import ttk
import time
from data_calculator import DataCalculator, CalculatorGUI

class RolloverClickerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Clicker")

        # Initialize values
        self.units = list(DataCalculator.UNIT_FACTORS.keys())[::-1]  # Reverse order
        self.resources = DataCalculator.calculate_and_distribute(0)  # Initialize resources as a dictionary
        self.generators = [0] * len(self.units)

        # Create labels, buttons, and generator displays for each unit
        self.labels = []
        self.generator_labels = []
        self.buy_buttons = []
        for i, name in enumerate(self.units):
            label = tk.Label(master, text=f"{name.capitalize()}: 0")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.labels.append(label)

            generator_label = tk.Label(master, text=f"Generators: {self.generators[i]}")
            generator_label.grid(row=i, column=1, padx=5, pady=5)
            self.generator_labels.append(generator_label)

            cost_unit = self.units[i-1] if i > 0 else "N/A"
            button = tk.Button(master, text=f"Buy {name.capitalize()} Generator (Cost: 10 {cost_unit.capitalize()})",
                               command=lambda i=i: self.buy_generator(i))
            button.grid(row=i, column=2, padx=5, pady=5)
            self.buy_buttons.append(button)

        # Create dropdown for selecting data type
        self.selected_data_type = tk.StringVar()
        self.data_type_dropdown = ttk.Combobox(master, textvariable=self.selected_data_type)
        self.data_type_dropdown['values'] = self.units
        self.data_type_dropdown.current(len(self.units) - 1)  # Set default value to "Bit"
        self.data_type_dropdown.grid(row=len(self.units), column=0, pady=10)

        # Create button to add one unit of selected data type
        self.add_button = tk.Button(master, text="Add 1", command=self.add_selected_data_type)
        self.add_button.grid(row=len(self.units), column=1, pady=10)

        # Create button to sell all generators
        self.sell_all_button = tk.Button(master, text="Sell All Generators", command=self.sell_all_generators)
        self.sell_all_button.grid(row=len(self.units), column=2, pady=10)

        # Start automatic increment
        self.auto_increment()

    def add_selected_data_type(self):
        selected_type = self.selected_data_type.get()
        bits_to_add = DataCalculator.convert_to_bits(1, selected_type)
        self.resources = DataCalculator.calculate_and_distribute(bits_to_add, 'add')
        self.update_display()

    def buy_generator(self, i):
        if i == 0:
            print(f"Cannot buy generator for highest tier.")
            return

        cost_unit = self.units[i-1]
        cost = DataCalculator.convert_to_bits(10, cost_unit)

        if self.resources['bit'] >= cost:
            self.resources = DataCalculator.calculate_and_distribute(cost, 'subtract')
            self.generators[i] += 1
            self.update_display()
            print(f"Successfully bought {self.units[i].capitalize()} Generator.")
        else:
            print(f"Not enough resources to buy {self.units[i].capitalize()} Generator.")

    def sell_all_generators(self):
        refund = 0
        for i in range(1, len(self.units)):  # Exclude the highest tier
            refund += DataCalculator.convert_to_bits(self.generators[i] * 10, self.units[i-1])
            self.generators[i] = 0

        self.resources = DataCalculator.calculate_and_distribute(refund, 'add')
        self.update_display()
        print("All generators sold and resources refunded.")

    def auto_increment(self):
        increment = 0
        for i, count in enumerate(self.generators):
            increment += DataCalculator.convert_to_bits(count, self.units[i])
        self.resources = DataCalculator.calculate_and_distribute(increment, 'add')
        self.update_display()
        self.master.after(1000, self.auto_increment)  # Repeat every second

    def update_display(self):
        for i, unit in enumerate(self.units):
            value = self.resources.get(unit, 0)
            if value > 0:
                self.labels[i].config(text=f"{unit.capitalize()}: {value}")
            else:
                self.labels[i].config(text="")

        # Update generator labels
        for i, count in enumerate(self.generators):
            self.generator_labels[i].config(text=f"Generators: {count}")




if __name__ == "__main__":
    root = tk.Tk()
    app = RolloverClickerGame(root)
    root.mainloop()
