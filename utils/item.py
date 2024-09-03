class Item:
    def __init__(self, name, cost, description, spammable=False, action=None, add_to_inventory=False):
        self.name = name
        self.cost = cost
        self.description = description
        self.spammable = spammable
        self.action = action
        self.add_to_inventory = add_to_inventory

    def __str__(self):
        return f"{self.name} (Cost: {self.cost})"
