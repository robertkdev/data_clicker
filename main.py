import tkinter as tk
from game_logic import DataClickerGame

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x650")  # Increased height to accommodate the new button
    app = DataClickerGame(root, enable_commands=True)  # Set to False to disable commands
    root.mainloop()