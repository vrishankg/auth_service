class User:
    def __init__(self, name, location, budget, top_cuisines, fav_activities):
        self.name = name
        self.location = location
        self.budget = budget
        self.top_cuisines = top_cuisines
        self.fav_activities = fav_activities

    def __str__(self):
        return f"User(name={self.name}, location={self.location}, budget={self.budget}, top_cuisines={self.top_cuisines}, fav_activities={self.fav_activities})"

