class Slider():
    def __init__(self, name, range_min, range_max, value):
        self.name = name
        self.range_min = range_min
        self.range_max = range_max
        self.value = value

class Button():
    def __init__(self, full_name, short_name, id):
        self.full_name = full_name
        self.short_name = short_name
        self.id = id