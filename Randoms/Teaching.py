from random import randint as rd # You can import files via these three keywords. You can drop the "from" if you want to import the entire package, or the "as" if you want to store it by its default name.

class ExampleClass(object):

    # BIG INFO: In pyhton, there are no {} and ; Python determines what belongs to what using indentation. 

    # This is how you create a class. An example of instantiating is is on line 42. It is currently inheriting the "object" superclass.
    def __init__(self) -> None: # This is the constructor for the ExampleClass class. It doesn't take in any parameters beside the standard "self" parameter that all class functions need.
        self.name = "Exemplar" # In python, variables are "dynamically typed" meaning that you don't have to declare their type. The "self" keyword acts exactly the same as the "this" keyword in Java.
        self.value = False # Booleans in python are always capitalized, and either True or False. You can multiply by booleans, with True counting as 1, and False counting as 0.
        self.list = [1, "2", 3, 4, 5, 6, 7] # Objects in python arrays can have any type. This can be a good and a bad thing.
        self.list.append(8) # By adding () to the end of a function, you can call it. Here, it calls the constructor of the superclass. Additionally, arrays in python have dynamic length, and can be appended to using the inbuilt .append() command
    
    def __repr__(self) -> str: # This is sort of a niche python thing, it is the __repr__() function of a class. It is called whenever the class gets printed. It should always return a string.

        return f"Name: {self.name}\nValue: {self.value}\nList: {self.list}" # These are what are called "f strings", with which you can input the values of variables into a string without using a bunch of + statements
    
    def get_value(self) -> bool: # You can declare the return type of a function to increase readability by using the "->" keyword.
        return self.value

    def set_value(self, value: bool) -> None: # you can also declare parameter types, however you can still input other types of parameters without it calling an error.
        self.value = value

    def get_name(self) -> str: # something I forgot to say is that in python, functions are defined using the "def" keyword.
        return self.name
    
    def _rename(self, name: str) -> None:
        self.name = name

    def print_list(self) -> None:

        for number in self.list: # This is what is called "list comprehension" in pyhton. Here, it stores numbers within "list" inside the "number" variable.
            print(number)
        
    def roll_dice(self, size: int) -> None:

        print(rd(1, size))
    
    def print_parts_of_name(self) -> None:

        print(f"First half: {self.name[:int(len(self.name) / 2)]}") # you can select the substring of a string by treating it like a list, and doing [start:end]. If you don't give a value, like [:end], python assumes you go to the extremes (start or end)
        print(f"Second half: {self.name[int(len(self.name) / 2):]}")
        print(f"last 3 letters: {self.name[-3:]}")

if __name__ == '__main__':

    example = ExampleClass() # This is how you instantiate classes in pyhton
    print(example.get_value()) # this is the print function in python
    example.set_value(True) # This is how you call functions
    print(example.get_value())

    example.print_list()

    example.print_parts_of_name()

    example.roll_dice(20)

    print(example.__dict__) # __dict__ gives the dictionary representation of a class, which can be easily stored into .json files using the json library and the .dump() command.
    print(example) # This is how the __repr__ becomes useful.