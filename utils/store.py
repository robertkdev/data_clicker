from utils.item import Item
from config import STORE_ITEMS

class Store:
    def __init__(self, buy_generator, buy_item, upgrade_store):
        self.level = 1
        self.items = {}
        self.buy_generator = buy_generator
        self.buy_item = buy_item
        self.upgrade_store = upgrade_store
        self.initialize_store_items()

    def initialize_store_items(self):
        for item_data in STORE_ITEMS.get(self.level, []):
            item = Item(
                item_data["name"],
                item_data["cost"],
                item_data.get("description", ""),
                spammable=item_data.get("spammable", False),
                action=getattr(self, item_data["action"]),
                add_to_inventory=item_data.get("add_to_inventory", False)
            )
            self.add_item(item)

    def add_item(self, item):
        if isinstance(item, Item):
            item.button = None  # Initialize button attribute
            self.items[item.name] = item
        else:
            print(f"Invalid item: {item}")

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]

    def get_items(self):
        return self.items.values()

    def upgrade(self):
        if self.level >= len(STORE_ITEMS):
            print("Store is already at maximum level.")
            return False

        cost_in_bytes = self.get_upgrade_cost()
        if cost_in_bytes is None:
            print("Unable to determine upgrade cost.")
            return False

        if self.upgrade_store(cost_in_bytes):
            self.level += 1
            self.add_new_items()
            return True
        else:
            return False

    def add_new_items(self):
        for item_data in STORE_ITEMS.get(self.level, []):
            item = Item(
                item_data["name"],
                item_data["cost"],
                item_data.get("description", ""),
                spammable=item_data.get("spammable", False),
                action=getattr(self, item_data["action"]),
                add_to_inventory=item_data.get("add_to_inventory", False)
            )
            self.add_item(item)

    def get_upgrade_cost(self):
        for item_data in STORE_ITEMS.get(self.level, []):
            if item_data["name"] == "Upgrade Store":
                return int(item_data["cost"].split()[0])
        return None

    def handle_purchase(self, item):
        if item.action:
            if item.name == "Upgrade Store":
                success = self.upgrade()
            elif item.spammable:
                success = item.action(item.name.split()[-2].lower())
            elif item.action == self.buy_generator:
                success = item.action(item.name.split()[-2].lower())
            else:
                success = item.action(item.name, int(item.cost.split()[0]))
            
            if success:
                if item.add_to_inventory:
                    self.buy_item(item.name, int(item.cost.split()[0]))
                
                if not item.spammable:
                    self.remove_item(item.name)
            
            return success
        else:
            print(f"No action defined for {item.name}")
            return False
