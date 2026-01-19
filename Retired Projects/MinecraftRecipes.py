import copy

class Recipe():
    def __init__(self, ingredients: list[tuple['Recipe|str', 'int']], result: int):
        self.ingredients = ingredients
        self.result = result
    
    def __add__(self, other: 'Recipe'):
        # if not isinstance(other, Recipe):
        #     print("Warning: Non-recipe added to recipe!")
        #     return False
        new = self.ingredients
        for ingredient, amount in other.ingredients:
            found = False
            for i, (ing, amt) in enumerate(new):
                if ing == ingredient:
                    new[i] = (ing, amt + amount)
                    found = True
                    break
            if not found:
                new.append((ingredient, amount))

        # self.ingredients = new
        return Recipe(new, self.result)
    
    def __mul__(self, other: int):
        new = self.ingredients
        new = [(ingredient, amount * other) for ingredient, amount in new]
        newobj = Recipe(new, self.result)
        return newobj
    
    def __repr__(self):
        return self.ingredients.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.ingredients == other.ingredients and self.result == other.result
    
    def get_degree(self):
        # How many recipe-in-a-recipe's there are.
        # if this contains no recipes, it's degree 0, if it has a recipe with degree 0 then it's degree 1, etc.
        degree = 0
        for ingredient in self.ingredients:
            if isinstance(ingredient[0], Recipe):
                degree = max(degree, ingredient[0].get_degree() + 1)
        return degree
    
    def craft(self, amount: int = 1):
        # Unpack the recipe into all base costs: if it contains a recipe, unpack it, etc.
        # Some recipes produce more than one item, and some require more than one: this is why I have the degree system.
        # Let's say a recipe requires two rune of water and a rune of greed
        # The rune of greed requires two runes of water, so the degree of the rune of greed is 1, and the degree of the rune of water is 0.
        # When we simplify the recipe, we first unpack the rune of greed into a rune of water, and then recognize that we now have four runes of water on the 'stack' (don't need to actually use this datastructure)
        # We then realize that the rune_of_water recipe creates 3 runes of water, so we can simplify by realizing we need to craft the recipe twice: 6 runes of water.
        # This is a simple example, but it's a bit more complicated with more complex recipes.
        # The degree system is used to determine the order in which to simplify the recipes.
        new = copy.deepcopy(self) * -(-amount // self.result)
        finished_unpacking = False
        while not finished_unpacking:
            finished_unpacking = True
            #find the highest degree recipe
            max_degree = -1
            max_degree_index = -1
            for i, (ingredient, amount) in enumerate(new.ingredients):
                if isinstance(ingredient, Recipe):
                    # print(ingredient.get_degree())
                    if ingredient.get_degree() > max_degree:
                        max_degree = ingredient.get_degree()
                        max_degree_index = i
            if max_degree_index != -1:
                #remove the highest degree recipe
                finished_unpacking = False
                recipe, amount = new.ingredients.pop(max_degree_index)
                whattoadd = recipe * -(-amount // recipe.result)
                # print(type(whattoadd))
                #add the single-degree unpaked version of the removed recipe
                new = new + whattoadd
        return new
                
        

rune_of_water = Recipe([("Manasteel Ingot", 3), ("Fishing Rod", 1), ("Sugar Cane", 1), ("Bone Meal", 1)], 3)
rune_of_fire = Recipe([("Manasteel Ingot", 3), ("Nether Wart", 1), ("Gunpowder", 1), ("Nether Brick", 1)], 3)
rune_of_earth = Recipe([("Manasteel Ingot", 3), ("Mushroom", 1), ("Block of Coal", 1), ("Stone", 1)], 3)
rune_of_air = Recipe([("Manasteel Ingot", 3), ("Feather", 1), ("String", 1), ("Carpet", 1)], 3)

rune_of_spring = Recipe([(rune_of_water, 1), (rune_of_fire, 1), ("Wheat", 1), ("Sapling", 3)], 1)
rune_of_summer = Recipe([(rune_of_earth, 1), (rune_of_air, 1), ("Watermelon", 1), ("Slime Ball", 1), ("Sand", 2)], 1)
rune_of_autumn = Recipe([(rune_of_fire, 1), (rune_of_air, 1), ("Spider Eye", 1), ("Leaves", 3)], 1)
rune_of_winter = Recipe([(rune_of_water, 1), (rune_of_earth, 1), ("Cake", 1), ("Wool", 1), ("Snow", 2)], 1)

rune_of_mana = Recipe([("Manasteel Ingot", 5), ("Mana Pearl", 1)], 1)

rune_of_lust = Recipe([("Mana Diamond", 2), (rune_of_air, 1), (rune_of_summer, 1)], 2)
rune_of_gluttony = Recipe([("Mana Diamond", 2), (rune_of_fire, 1), (rune_of_winter, 1)], 2)
rune_of_greed = Recipe([("Mana Diamond", 2), (rune_of_water, 1), (rune_of_spring, 1)], 2)
rune_of_sloth = Recipe([("Mana Diamond", 2), (rune_of_air, 1), (rune_of_autumn, 1)], 2)
rune_of_wrath = Recipe([("Mana Diamond", 2), (rune_of_earth, 1), (rune_of_winter, 1)], 2)
rune_of_envy = Recipe([("Mana Diamond", 2), (rune_of_water, 1), (rune_of_winter, 1)], 2)
rune_of_pride = Recipe([("Mana Diamond", 2), (rune_of_fire, 1), (rune_of_summer, 1)], 2)

# print(rune_of_spring)
# unpacked = rune_of_spring.craft()
print((rune_of_sloth + rune_of_greed).craft())
