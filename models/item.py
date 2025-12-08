class Item:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}')"
