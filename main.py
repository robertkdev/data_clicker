import tkinter as tk
from dataclickergame import DataClickerGame

if __name__ == "__main__":
    root = tk.Tk()
    
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size
    window_width = 1200
    window_height = 650

    # Calculate position coordinates
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = DataClickerGame(root, enable_commands=True)  # Set to False to disable commands
    root.mainloop()