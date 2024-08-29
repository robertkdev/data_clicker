import tkinter as tk

class DataSection:
    def __init__(self, parent, units):
        self.frame = tk.Frame(parent, bg='white', bd=2, relief=tk.GROOVE)
        self.frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.create_header()
        self.create_scrollable_frame()
        self.create_labels(units)

    def create_header(self):
        self.header = tk.Label(self.frame, text="Data Storage", font=("Helvetica", 16, "bold"), bg='#4a7abc', fg='white')
        self.header.pack(fill="x", pady=(0, 10))

    def create_scrollable_frame(self):
        self.canvas = tk.Canvas(self.frame, bg='white')
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
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

    def create_labels(self, units):
        self.labels = []
        for name in units:
            label = tk.Label(self.scrollable_frame, text=f"{name.capitalize()}: 0", font=("Helvetica", 12), bg='white')
            label.pack(pady=5, padx=10, anchor="w")
            self.labels.append(label)

    def update_display(self, resources):
        for label, (unit, value) in zip(self.labels, resources.items()):
            label.config(text=f"{unit.capitalize()}: {value}")