# testing max

class Thing():
    def __init__(self, value, name):
        self.value = value
        self.name = name
    def get_value(self):
        return self.value

things = [Thing(1, 'one'), Thing(2, 'two'), Thing(3, 'three')]
max_thing = max(things, key=lambda x: x.get_value())
print(max_thing.name)  # three