import tkinter as tk

class InventorySection:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='#e6e6e6', bd=2, relief=tk.GROOVE)
        self.frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.create_header()
        self.create_scrollable_frame()

    def create_header(self):
        self.header = tk.Label(self.frame, text="Inventory", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.header.pack(fill="x", pady=(0, 10))

    def create_scrollable_frame(self):
        self.canvas = tk.Canvas(self.frame, bg='#e6e6e6')
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#e6e6e6')

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

    def update_display(self, generators, documents, inventory):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not generators and documents == 0 and not inventory:
            tk.Label(self.scrollable_frame, text="Inventory is empty", font=("Helvetica", 12), bg='#e6e6e6').pack(pady=5, padx=10, anchor="w")
        else:
            if documents > 0:
                tk.Label(self.scrollable_frame, text=f"Documents: {documents}", font=("Helvetica", 12), bg='#e6e6e6').pack(pady=5, padx=10, anchor="w")
            
            for unit, count in generators.items():
                tk.Label(self.scrollable_frame, text=f"{unit.capitalize()} Generators: {count}", font=("Helvetica", 12), bg='#e6e6e6').pack(pady=5, padx=10, anchor="w")

            for item, count in inventory.items():
                tk.Label(self.scrollable_frame, text=f"{item}: {count}", font=("Helvetica", 12), bg='#e6e6e6').pack(pady=5, padx=10, anchor="w")