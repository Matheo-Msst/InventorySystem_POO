from models.item import Item

class InventoryService:

    def get_slot(self, user, row, col):
        return user.inventory[row][col]

    def move_item(self, user, r1, c1, r2, c2):
        if user.inventory[r2][c2] != "":
            return False
        user.inventory[r2][c2] = user.inventory[r1][c1]
        user.inventory[r1][c1] = ""
        return True
    
    def set_item(self, user, row, col, item):
        if user.inventory[row][col] == "":
            user.inventory[row][col] = item
            item.user = user  
            return True
        return False
    
    def remove_item(self, user, row, col):
        item = user.inventory[row][col]
        if item != "":
            item.user = None  # plus de propriétaire
        user.inventory[row][col] = ""


