import os
from copy import deepcopy
import re

from core.constants import SECTION_BREAK, SECTION_HEADERS
from core.misc.utilities import num


class IngredientAmount:
    def __init__(self):
        self.amounts = {}

    def __getitem__(self, item):
        return self.amounts[item]

    def __iter__(self):
        return iter(self.amounts.items())

    def add_amount(self, amount, amount_type):
        if amount_type in self.amounts:
            self.amounts[amount_type] = num(self.amounts[amount_type]) + num(amount)
        else:
            self.amounts[amount_type] = num(amount)

    def __add__(self, other):
        new_amount = IngredientAmount()
        for key, val in self.amounts.items():
            new_amount.add_amount(val, key)
        for key, val in other.amounts.items():
            new_amount.add_amount(val, key)
        return new_amount

    def __str__(self):
        output_str = ''
        for t, val in self:
            output_str += f'{val}{t}, '
        return output_str[:-2]
    
    def __deepcopy__(self, memodict=None):
        return IngredientAmount() + self
        

class Ingredient:

    def __init__(self, name):
        self.name = name
        self.amount = IngredientAmount()

    def add_amount(self, amount, amount_type):
        self.amount.add_amount(amount, amount_type)

    def __str__(self):
        output_str = self.name + ': ' + str(self.amount)

        return output_str

    def __add__(self, other):
        if self.name != other.name:
            raise ValueError(f'Trying to add ingredient with name {self.name} to ingredient with name {other.name}.'
                             f' Addition can only be performed on a single ingredient.')
        new_ingredient = Ingredient(self.name)
        new_ingredient.amount = self.amount + other.amount
        return new_ingredient

    def __deepcopy__(self, memodict=None):
        return Ingredient(self.name) + self


class Recipe:

    def __init__(self, name):
        self.name = name
        self.ingredients = []  # should this be a dictionary? Or an IngredientList object?
        self.url = ''
        self.steps = ''

    def add_ingredient(self, name, amount, amount_type=None):

        # TODO: If two ingredients are same but singular + plural, make both singular and use that as ingredient name
        amount_type = '' if amount_type is None else amount_type
        amount = 1 if amount_type is '' else amount
        new_ingredient = Ingredient(name)
        new_ingredient.add_amount(amount, amount_type)
        self.add_ingredient_object(new_ingredient)

    def add_ingredient_object(self, ingredient_obj):
        bool_added = False
        for i, ing in enumerate(self.ingredients):
            if ingredient_obj.name == ing.name:
                self.ingredients[i] = ing + ingredient_obj
                bool_added = True
                break
        if not bool_added:
            self.ingredients.append(ingredient_obj)

    def __add__(self, other):
        new_recipe = Recipe(self.name)
        new_recipe.url = self.url
        new_recipe.steps = self.steps
        new_recipe.ingredients = deepcopy(self.ingredients)
        for ing in other.ingredients:
            new_recipe.add_ingredient_object(ing)

        return new_recipe

    def __str__(self):
        output_str = f'{self.name}\nIngredients:\n'
        for ing in self.ingredients:
            output_str += f'{str(ing)}\n'
        if self.url != '':
            output_str += f'Steps:\n\t{self.steps}\n'
        if self.steps != '':
            output_str += f'Webisite:\n\t{self.url}'

        return output_str


class RecipeExtractor:

    def __init__(self):
        pass

    def extract_recipe(self, file):

        recipe = Recipe(os.path.basename(file.replace('.txt', '')))

        with open(file, 'r') as f:

            read_file = f.readlines()
            for i, line in enumerate(read_file):
                if line.lower().strip() in SECTION_HEADERS:
                    recipe = self.extract_section(recipe, read_file[i:])

        return recipe

    def extract_section(self, recipe, read_file):
        header_line = read_file[0].lower()
        body_lines = read_file[1:]

        if 'ingredients' in header_line:
            recipe = self.extract_ingredients(recipe, body_lines)
        elif 'url' in header_line:
            recipe = self.extract_url(recipe, body_lines)
        elif 'steps' in header_line:
            recipe = self.extract_steps(recipe, body_lines)

        return recipe

    def extract_ingredients(self, recipe, lines):

        def parse_line(l):

            split_line = l.split(':')
            n = split_line[0].strip().lower()
            if len(split_line) != 1:
                r_a = re.compile(r"^\d*[.,]?\d*")
                r_t = re.compile(r"\s?[a-zA-Z]*")
                a = r_a.findall(split_line[1].strip())[0]
                a = num(a)
                t_matches = r_t.findall(split_line[1])
                t = ''
                for m in t_matches:
                    t = m if (len(m) > len(t) and '\n' not in m and m != ' ') else t
            else:
                a = 1
                t = ''
            return n, a, t

        for line in lines:
            if line.lower().strip() in SECTION_HEADERS:
                break

            name, amount, amount_type = parse_line(line)
            recipe.add_ingredient(name, amount, amount_type=amount_type)

        return recipe

    def extract_url(self, recipe, lines):
        return recipe

    def extract_steps(self, recipe, lines):
        return recipe


if __name__ == '__main__':
    extractor = RecipeExtractor()
    recipe_file = '/Users/Max/MiscProjects/ShoppingListBuilder/recipes/Shepherds Pie.txt'

    r = extractor.extract_recipe(recipe_file)
    # x = 2
    #
    # i1 = Ingredient('carrot')
    # i1.add_amount(500, 'g')
    # i1.add_amount(3, '')
    # i1.add_amount(100, 'g')
    # i2 = Ingredient('carrot')
    # i2.add_amount(200, 'g')
    # i2.add_amount(2, 'oz')
    # i3 = i1 + i2
    # print(str(i1))
    # print(str(i2))
    # print(str(i3))
    # print(str(recipe))
    recipe_double = r + r
    print(recipe_double)
    print(r)