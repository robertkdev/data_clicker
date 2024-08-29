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
    def convert_from_bits(bits):
        """Convert bits to the largest possible unit."""
        for unit, factor in reversed(DataCalculator.UNIT_FACTORS.items()):
            if bits >= factor:
                return bits / factor, unit
        return bits, 'bit'

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

    @staticmethod
    def calculate_and_distribute(value, operation='add'):
        """
        Perform the specified operation and distribute the result across all units.
        
        :param value: The value to add/subtract (in bits)
        :param operation: 'add' or 'subtract'
        :return: A dictionary with all units and their values
        """
        current_bits = getattr(DataCalculator, 'current_bits', 0)
        
        if operation == 'add':
            current_bits += value
        elif operation == 'subtract':
            current_bits = max(0, current_bits - value)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        DataCalculator.current_bits = current_bits
        
        result = {}
        remaining_bits = current_bits
        
        for unit, factor in DataCalculator.UNIT_FACTORS.items():
            unit_value = remaining_bits // factor
            remaining_bits %= factor
            result[unit] = unit_value
        
        return result

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Calculator")
        self.current_value = 0  # Initialize current value to 0
        self.create_widgets()

    def create_widgets(self):
        units = list(DataCalculator.UNIT_FACTORS.keys())

        # Input Value
        self.value_label = ttk.Label(self.root, text="Input Value:")
        self.value_label.grid(column=0, row=0, padx=10, pady=5)
        self.value_entry = ttk.Entry(self.root)
        self.value_entry.grid(column=1, row=0, padx=10, pady=5)
        self.unit_combo = ttk.Combobox(self.root, values=units)
        self.unit_combo.grid(column=2, row=0, padx=10, pady=5)
        self.unit_combo.set('bit')  # Set default unit to bit

        # Operation Buttons
        self.add_button = ttk.Button(self.root, text="Add", command=lambda: self.perform_operation(DataCalculator.add))
        self.add_button.grid(column=0, row=1, padx=10, pady=5)
        self.subtract_button = ttk.Button(self.root, text="Subtract", command=lambda: self.perform_operation(DataCalculator.subtract))
        self.subtract_button.grid(column=1, row=1, padx=10, pady=5)
        self.multiply_button = ttk.Button(self.root, text="Multiply", command=lambda: self.perform_operation(DataCalculator.multiply))
        self.multiply_button.grid(column=2, row=1, padx=10, pady=5)
        self.divide_button = ttk.Button(self.root, text="Divide", command=lambda: self.perform_operation(DataCalculator.divide))
        self.divide_button.grid(column=3, row=1, padx=10, pady=5)

        # Result
        self.result_label = ttk.Label(self.root, text="Result:")
        self.result_label.grid(column=0, row=2, padx=10, pady=5)
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(column=1, row=2, columnspan=3, padx=10, pady=5)

    def get_input_value(self):
        try:
            value = float(self.value_entry.get())
            unit = self.unit_combo.get()
            return value, unit
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the input value.")
            return None

    def perform_operation(self, operation):
        input_value = self.get_input_value()
        if input_value:
            value, unit = input_value
            try:
                self.current_value = operation(self.current_value, 'bit', value, unit)
                self.display_result(self.current_value)
            except ValueError as e:
                messagebox.showerror("Calculation Error", str(e))

    def display_result(self, result_bits):
        self.result_text.delete(1.0, tk.END)
        remaining_bits = result_bits
        
        for unit in DataCalculator.UNIT_FACTORS:
            factor = DataCalculator.UNIT_FACTORS[unit]
            value = remaining_bits // factor
            remaining_bits %= factor
            if value > 0:
                self.result_text.insert(tk.END, f"{unit}: {int(value)}\n")

# Example usage as an API
def calculate(operation, value1, unit1, value2, unit2):
    """Perform a calculation and return the result in the largest possible unit."""
    operations = {
        'add': DataCalculator.add,
        'subtract': DataCalculator.subtract,
        'multiply': DataCalculator.multiply,
        'divide': DataCalculator.divide
    }
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    
    result_bits = operations[operation](value1, unit1, value2, unit2)
    return DataCalculator.convert_from_bits(result_bits)

if __name__ == "__main__":
    # GUI usage
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()

    # API usage example
    print(calculate('add', 1, 'gigabyte', 500, 'megabyte'))
    print(calculate('multiply', 2, 'terabyte', 3, 'bit'))