class Item:
    def __init__(self, id: int, name: str, user=None, col=None):
        self.id = id
        self.name = name
        self.user = user    
        self.col = col      

    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}', user_id={self.user.id if self.user else None}, col={self.col})"
