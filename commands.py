import tkinter as tk

class CommandBox:
    def __init__(self, parent, execute_command):
        self.frame = tk.Frame(parent, bg='#2c2c2c', bd=2, relief=tk.GROOVE)
        self.frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        
        self.entry = tk.Entry(self.frame, font=("Helvetica", 14), bg='#3a3a3a', fg='#ffffff', insertbackground='#ffffff')
        self.entry.pack(fill="x", padx=10, pady=5)
        self.entry.bind("<Return>", self.on_enter)
        
        self.execute_command = execute_command

    def on_enter(self, event):
        command = self.entry.get()
        self.execute_command(command)
        self.entry.delete(0, tk.END)

    def hide(self):
        self.frame.grid_remove()

    def show(self):
        self.frame.grid()

    def execute_command(self, command):
        print(f"Executing command: {command}")
        parts = command.split()
        if len(parts) == 3 and parts[0] == "/give":
            data_type = parts[1]
            try:
                quantity = float(parts[2])
                self.give_data(data_type, quantity)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        else:
            print("Unknown command or incorrect format.")