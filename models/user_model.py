class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.inventory = [
            ["", "", "","", "", "", "", "", ""]
        ]

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"
