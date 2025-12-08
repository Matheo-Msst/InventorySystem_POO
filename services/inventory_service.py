class InventoryManager:

    def __init__(self, inventory):
        self.inventory = inventory

    def get_slot(self, row, col):
        return self.inventory[row][col]

    def set_item(self, row, col, item: Item):
        if self.inventory[row][col] == "":
            self.inventory[row][col] = item
            return True
        return False

    def remove_item(self, row, col):
        self.inventory[row][col] = ""

    def move_item(self, from_row, from_col, to_row, to_col):
        if self.inventory[to_row][to_col] != "":
            return False 

        self.inventory[to_row][to_col] = self.inventory[from_row][from_col]
        self.inventory[from_row][from_col] = ""
        return True

    def find_item_by_id(self, item_id):
        for r in range(3):
            for c in range(3):
                item = self.inventory[r][c]
                if isinstance(item, Item) and item.id == item_id:
                    return r, c, item
        return None
