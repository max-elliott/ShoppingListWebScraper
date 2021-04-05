from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from core.recipe import Recipe
from core.misc.utilities import num
from webscraping.constants import WEBDRIVER_LOCATION, REMOVED_WORDS

import re


class WebsiteRecipeParser:

    possible_types = ['ml ', 'l ', 'liters', 'litres', 'g ', 'kg', 'kilograms', 'grams', 'sp ', 'tsp', 'tbsp',
                      'cm', 'm', 'mm', 'pinch of', '']
    num_levels = 5

    def __init__(self, website_link, webdriver_location=None):
        self.website_link = website_link
        self.webdriver_location = webdriver_location if webdriver_location is not None else WEBDRIVER_LOCATION
        self.recipe = Recipe(None)
        self.recipe.url = website_link
        self.recipe_name_html_path = None
        self.recipe_ingredient_html_path = None

        if not self.check_valid_link():
            raise FileNotFoundError(f"{self.website_link} is not valid")

    def check_valid_link(self):
        raise NotImplementedError

    def scrape_recipe(self):
        raise NotImplementedError


class BBCGoodFoodRecipeParser(WebsiteRecipeParser):
    def __init__(self, website_link, webdriver_location=None):
        super(BBCGoodFoodRecipeParser, self).__init__(website_link, webdriver_location)
        self.recipe_name_html_path = '//*[@id="__next"]/div[3]/main/div/section/div/div[3]/h1'
        self.recipe_ingredient_html_path = '/html/body/div[2]/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div/section[1]/section[__LEVEL__]/ul'

    def check_valid_link(self):
        if self.website_link is None:
            return False
        if 'bbcgoodfood' in self.website_link.lower():
            return True
        else:
            return False

    def parse_ingredient_line(self, line):
        line = line.split(',')[0]
        line = line.replace('½', '.5').replace('¼', '.25').replace('¾', '.75')
        a = re.findall(r"^\d*[.,]?\d*", line)[0]
        if a == '.5':
            a = 0.5

        measurement_list = re.findall(r"^\d*[.,]?\d* ?(?=(" + '|'.join(self.possible_types) + r"))", line)
        t = measurement_list[0].strip() if len(measurement_list) > 0 else ''
        t = t.replace('pinch of', 'pinch')

        n = re.findall(r"^\d*[.,]?\d* ?(?:" + '|'.join(self.possible_types) + r")(.*),?.*$", line)[0]
        for word in REMOVED_WORDS:
            n = n.replace(word, '')
        n = n.strip()

        return n, a, t
    
    def extract_recipe_name(self, driver):
        self.recipe.name = driver.find_element_by_xpath(self.recipe_name_html_path).text
        return self.recipe.name

    def extract_recipe_ingredients(self, driver):
        ingredient_list_full = []
        try:
            for level in range(1, self.num_levels+1):
                ingredient_element = driver.find_element_by_xpath(self.recipe_ingredient_html_path.replace('__LEVEL__', str(level)))
                ingredient_list = ingredient_element.text.split('\n')
                ingredient_list_full += ingredient_list

                for i in ingredient_list:
                    name, amount, amount_type = self.parse_ingredient_line(i)
                    self.recipe.add_ingredient(name, amount, amount_type)
        except NoSuchElementException:
            return ingredient_list_full

        return ingredient_list_full

    def extract_recipes_steps(selfself, driver):
        return 0

    def scrape_recipe(self):
        driver = webdriver.Chrome(self.webdriver_location)
        driver.get(self.website_link)

        _ = self.extract_recipe_name(driver)
        
        _ = self.extract_recipe_ingredients(driver)

        _ = self.extract_recipes_steps(driver)

        driver.close()

        return self.recipe

    def get_recipe(self):
        return self.recipe

if __name__ == '__main__':
    integer = 1
    float_val = 1.5
    print(float('.5'))

    print(num(integer))