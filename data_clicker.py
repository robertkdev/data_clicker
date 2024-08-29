import tkinter as tk
from tkinter import ttk
import time
from data_calculator import DataCalculator, CalculatorGUI

class DataClickerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Clicker")

        # Create a main frame to hold all content
        self.main_frame = tk.Frame(master, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill="both")

        # Configure main frame to center its contents
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Create a header frame
        self.header_frame = tk.Frame(self.main_frame, bg='#4a7abc', height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_label = tk.Label(self.header_frame, text="Data Clicker", font=("Helvetica", 24, "bold"), bg='#4a7abc', fg='white')
        self.header_label.pack(pady=10)

        # Create a frame to hold the game content
        self.game_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.game_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Configure game frame columns
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=2)

        # Initialize values
        self.units = list(DataCalculator.UNIT_FACTORS.keys())[::-1]  # Reverse order
        self.resources = DataCalculator.calculate_and_distribute(0)  # Initialize resources as a dictionary
        self.generators = [0] * (len(self.units) - 1)  # Remove one generator for yottabytes

        # Create a frame for the data section
        self.data_frame = tk.Frame(self.game_frame, bg='white', bd=2, relief=tk.GROOVE)
        self.data_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

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

        # Create a frame for the generators and buttons
        self.control_frame = tk.Frame(self.game_frame, bg='#f0f0f0')
        self.control_frame.grid(row=0, column=1, sticky="nsew")

        # Create generator displays and buy buttons
        self.generator_labels = []
        self.buy_buttons = []
        for i, name in enumerate(self.units[:-1]):  # Exclude yottabytes
            frame = tk.Frame(self.control_frame, bg='#f0f0f0')
            frame.pack(fill="x", pady=5)

            generator_label = tk.Label(frame, text=f"{name.capitalize()} Generators: 0", font=("Helvetica", 12), bg='#f0f0f0')
            generator_label.pack(side="left", padx=(0, 10))
            self.generator_labels.append(generator_label)

            cost_unit = self.units[i+1]
            cost = 10
            button = tk.Button(frame, text=f"Buy (Cost: {cost} {cost_unit.capitalize()}s)",
                               command=lambda i=i: self.buy_generator(i),
                               bg='#4CAF50', fg='white')
            button.pack(side="right")
            self.buy_buttons.append(button)

        # Create button to upload document (adds 1 bit)
        self.upload_button = tk.Button(self.control_frame, text="Upload Document", command=self.upload_document,
                                       bg='#008CBA', fg='white', font=("Helvetica", 14))
        self.upload_button.pack(fill="x", pady=(20, 10))

        # Create button to sell all generators
        self.sell_all_button = tk.Button(self.control_frame, text="Sell All Generators", command=self.sell_all_generators,
                                         bg='#f44336', fg='white', font=("Helvetica", 14))
        self.sell_all_button.pack(fill="x", pady=10)

        # Start automatic increment
        self.auto_increment()

    def upload_document(self):
        self.resources = DataCalculator.calculate_and_distribute(1, 'add')  # Add 1 bit
        self.update_display()

    def buy_generator(self, i):
        if i >= len(self.generators):
            print(f"Cannot buy generator for {self.units[i]}.")
            return

        cost_unit = self.units[i+1]
        cost = 10
        cost_in_bits = DataCalculator.convert_to_bits(cost, cost_unit)

        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)

        if total_bits >= cost_in_bits:
            self.resources = DataCalculator.calculate_and_distribute(cost_in_bits, 'subtract')
            self.generators[i] += 1
            self.update_display()
            print(f"Successfully bought {self.units[i].capitalize()} Generator.")
        else:
            print(f"Not enough resources to buy {self.units[i].capitalize()} Generator.")
            
    def sell_all_generators(self):
        refund_bits = 0
        for i, count in enumerate(self.generators):
            if i < len(self.units) - 1:  # Exclude the highest tier (yottabytes)
                cost_unit = self.units[i+1]
                refund_bits += DataCalculator.convert_to_bits(count * 10, cost_unit)
                self.generators[i] = 0

        self.resources = DataCalculator.calculate_and_distribute(refund_bits, 'add')
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
            self.labels[i].config(text=f"{unit.capitalize()}: {value}")

        # Update generator labels
        for i, count in enumerate(self.generators):
            self.generator_labels[i].config(text=f"{self.units[i].capitalize()} Generators: {count}")

        # Update buy buttons
        total_bits = sum(DataCalculator.convert_to_bits(self.resources[unit], unit) for unit in self.units)
        for i, unit in enumerate(self.units[:-1]):  # Exclude yottabytes
            cost_unit = self.units[i+1]
            cost = 10
            cost_in_bits = DataCalculator.convert_to_bits(cost, cost_unit)
            affordable = total_bits >= cost_in_bits
            self.buy_buttons[i].config(
                text=f"Buy (Cost: {cost} {cost_unit.capitalize()}s)",
                state="normal" if affordable else "disabled"
            )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Data Clicker")
    
    # Set the window size
    window_width = 800
    window_height = 600
    
    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate the position for the window to be centered
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    # Set the window size and position
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = DataClickerGame(root)
    root.mainloop()
