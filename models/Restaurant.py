class Restaurant:
    def __init__(self, name, location, price, cuisine, timing):
        self.name = name
        self.location = location
        self.price = price
        self.cuisine = cuisine
        self.timing = timing

    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'price': self.price,
            'cuisine': self.cuisine,
            'timing': self.timing
        }