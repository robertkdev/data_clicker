import tkinter as tk
from tkinter import ttk, messagebox

class DataCalculator:
    # Conversion factors
    UNIT_FACTORS = {
        'yottabyte': 8 * 1024**8,
        'zettabyte': 8 * 1024**7,
        'exabyte': 8 * 1024**6,
        'petabyte': 8 * 1024**5,
        'terabyte': 8 * 1024**4,
        'gigabyte': 8 * 1024**3,
        'megabyte': 8 * 1024**2,
        'kilobyte': 8 * 1024,
        'byte': 8,
        'bit': 1
    }

    @staticmethod
    def convert_to_bits(value, unit):
        """Convert a value from a given unit to bits."""
        if unit not in DataCalculator.UNIT_FACTORS:
            raise ValueError(f"Unknown unit: {unit}")
        return int(value * DataCalculator.UNIT_FACTORS[unit])

    @staticmethod
    def add(value1, unit1, value2, unit2):
        """Add two values with different units and return the result in bits."""
        bits1 = DataCalculator.convert_to_bits(value1, unit1)
        bits2 = DataCalculator.convert_to_bits(value2, unit2)
        return bits1 + bits2

    @staticmethod
    def subtract(value1, unit1, value2, unit2):
        """Subtract two values with different units and return the result in bits."""
        bits1 = DataCalculator.convert_to_bits(value1, unit1)
        bits2 = DataCalculator.convert_to_bits(value2, unit2)
        return max(0, bits1 - bits2)  # Ensure result is not negative

    @staticmethod
    def multiply(value1, unit1, value2, unit2):
        """Multiply two values with different units and return the result in bits."""
        bits1 = DataCalculator.convert_to_bits(value1, unit1)
        bits2 = DataCalculator.convert_to_bits(value2, unit2)
        return bits1 * bits2

    @staticmethod
    def divide(value1, unit1, value2, unit2):
        """Divide two values with different units and return the result in bits."""
        bits1 = DataCalculator.convert_to_bits(value1, unit1)
        bits2 = DataCalculator.convert_to_bits(value2, unit2)
        if bits2 == 0:
            raise ValueError("Division by zero is not allowed.")
        return bits1 // bits2

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Calculator")

        self.create_widgets()

    def create_widgets(self):
        units = list(DataCalculator.UNIT_FACTORS.keys())

        # Value 1
        self.value1_label = ttk.Label(self.root, text="Value 1:")
        self.value1_label.grid(column=0, row=0, padx=10, pady=5)
        self.value1_entry = ttk.Entry(self.root)
        self.value1_entry.grid(column=1, row=0, padx=10, pady=5)
        self.unit1_combo = ttk.Combobox(self.root, values=units)
        self.unit1_combo.grid(column=2, row=0, padx=10, pady=5)

        # Value 2
        self.value2_label = ttk.Label(self.root, text="Value 2:")
        self.value2_label.grid(column=0, row=1, padx=10, pady=5)
        self.value2_entry = ttk.Entry(self.root)
        self.value2_entry.grid(column=1, row=1, padx=10, pady=5)
        self.unit2_combo = ttk.Combobox(self.root, values=units)
        self.unit2_combo.grid(column=2, row=1, padx=10, pady=5)

        # Operation Buttons
        self.add_button = ttk.Button(self.root, text="Add", command=self.add)
        self.add_button.grid(column=0, row=2, padx=10, pady=5)
        self.subtract_button = ttk.Button(self.root, text="Subtract", command=self.subtract)
        self.subtract_button.grid(column=1, row=2, padx=10, pady=5)
        self.multiply_button = ttk.Button(self.root, text="Multiply", command=self.multiply)
        self.multiply_button.grid(column=2, row=2, padx=10, pady=5)
        self.divide_button = ttk.Button(self.root, text="Divide", command=self.divide)
        self.divide_button.grid(column=3, row=2, padx=10, pady=5)

        # Result
        self.result_label = ttk.Label(self.root, text="Result:")
        self.result_label.grid(column=0, row=3, padx=10, pady=5)
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(column=1, row=3, columnspan=3, padx=10, pady=5)

    def get_values(self):
        try:
            value1 = float(self.value1_entry.get())
            unit1 = self.unit1_combo.get()
            value2 = float(self.value2_entry.get())
            unit2 = self.unit2_combo.get()
            return value1, unit1, value2, unit2
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for values.")
            return None

    def display_result(self, result_bits):
        self.result_text.delete(1.0, tk.END)
        remaining_bits = result_bits
        
        for unit in DataCalculator.UNIT_FACTORS:
            factor = DataCalculator.UNIT_FACTORS[unit]
            value = remaining_bits // factor
            remaining_bits %= factor
            self.result_text.insert(tk.END, f"{unit}: {int(value)}\n")

    def add(self):
        values = self.get_values()
        if values:
            value1, unit1, value2, unit2 = values
            result_bits = DataCalculator.add(value1, unit1, value2, unit2)
            self.display_result(result_bits)

    def subtract(self):
        values = self.get_values()
        if values:
            value1, unit1, value2, unit2 = values
            result_bits = DataCalculator.subtract(value1, unit1, value2, unit2)
            self.display_result(result_bits)

    def multiply(self):
        values = self.get_values()
        if values:
            value1, unit1, value2, unit2 = values
            result_bits = DataCalculator.multiply(value1, unit1, value2, unit2)
            self.display_result(result_bits)

    def divide(self):
        values = self.get_values()
        if values:
            value1, unit1, value2, unit2 = values
            try:
                result_bits = DataCalculator.divide(value1, unit1, value2, unit2)
                self.display_result(result_bits)
            except ValueError as e:
                messagebox.showerror("Calculation Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()