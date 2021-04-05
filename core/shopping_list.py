from core.recipe import Recipe, RecipeExtractor
from webscraping.create_website_recipe_parser import create_website_recipe_parser
from core.constants import CURRENT_INGREDIENTS_FILE, MAIN_RECIPE_DIRECTORY
import os


def create_shopping_list(recipes=MAIN_RECIPE_DIRECTORY, current_ingredients=CURRENT_INGREDIENTS_FILE):
    sl = ShoppingList()
    sl.create_recipe_list(recipes=recipes)
    sl.create_current_ingredient_list()
    sl.create_shopping_list()
    print(sl)
    return sl


class ShoppingList:

    def __init__(self):
        self.recipes = []
        self.shopping_list = Recipe('-~-~-~-~- Shopping List -~-~-~-~-')
        self.current_ingredients = Recipe('Current Ingredients')
        self.recipe_extractor = RecipeExtractor()

    def create_recipe_list(self, recipes=MAIN_RECIPE_DIRECTORY):

        if os.path.isdir(recipes):

            recipe_files = [os.path.join(recipes, x) for x in os.listdir(recipes)]

            for f in recipe_files:
                self.recipes.append(self.recipe_extractor.extract_recipe(f))
        else:
            recipe_urls = []
            with open(recipes, 'r') as f:
                recipe_urls = f.readlines()
            for r in recipe_urls:
                parser = create_website_recipe_parser(r)
                recipe = parser.scrape_recipe()
                self.recipes.append(recipe)

    def create_current_ingredient_list(self, f=CURRENT_INGREDIENTS_FILE):
        self.current_ingredients = self.recipe_extractor.extract_recipe(f)

    def create_shopping_list(self):
        for r in self.recipes:
            self.shopping_list = self.shopping_list + r

        for ing in self.current_ingredients.ingredients:
            for i, ing2 in enumerate(self.shopping_list.ingredients):
                if ing.name == ing2.name:
                    self.shopping_list.ingredients.remove(ing2)
                    break

    def __str__(self):
        output_str = '-~-~-~-~- Recipe List -~-~-~-~-\n\n'
        for recipe in self.recipes:
            output_str += f'{recipe.name}\n'
        output_str += '\n' + str(self.shopping_list) + '-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\n'
        return output_str



if __name__ == '__main__':
    generate_shopping_list()
