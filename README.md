# Shopping List Generation via Web Scraping

This was a fun little software development project I've created to improve my general coding style and skills, separate from more numerical/scientific projects. This project involved using Selenium for webscraping, regex for recipe parsing, heirarchical object-orented programming, and overloading special methods.

# Usage

The code is run from main.py. This program can take in a list of various recipes and concatenate them together into a single shopping list of ingredients. The recipes can be supplied in two forms: a simple list of .txt files, or scraped directly from recipes online.

**Webscraping**

To generate the shopping list from online websites, a single .txt is supplied that contains a list of urls to the online recipes. The file should be located at /recipes/webscraping_recipe_lists/recipe_list.txt. The interface with the websites themselves is done through the Selenium package (tested using Chromedriver 89.0.4389.23 on 06/04/2021). This current file supplied in the repo should produce this list when run:

-~-~-~-~- Recipe List -~-~-~-~-

Creamy mushroom pasta
Courgette & lemon risotto
Sesame & spring onion stir-fried udon with crispy tofu
Mapo tofu
No-fuss shepherd's pie

-~-~-~-~- Shopping List -~-~-~-~-
Ingredients:
olive oil: 2tbsp
butter: 1tbsp, 135g
onion: 3
button chestnut mushroom: 250g
garlic clove: 2
dry white wine: 100ml
double cream: 200ml
lemon: 1
parmesan (or vegetarian alternative): 250g
tagliatelle or linguini: 300g
bunch parsley: 1
risotto rice: 180g
vegetable stock cube: 1
zest and juice 1 lemon: 1
lemon thyme sprigs: 1
courgette: 250g
crème fraîche: 2tbsp
block firm tofu: 400g
cornflour: 1tbsp, 1tsp
-1 tsp chilli flakes: 1
-.5 tsp Szechuan peppercorns: 1
vegetable oil: 1tbsp
bunch of spring onions: 1
green beans: 200g
ready-to-use thick udon noodles: 400g
sesame oil: 0.5tbsp
sesame seeds: 2tsp
low-salt soy sauce: 1tbsp
rice vinegar: 1tbsp
tofu: 450g
groundnut oil: 3tbsp
pork mince: 100g
Sichuan chilli bean paste: 2tbsp
fermented black beans: 1.5tbsp
piece ginger peeled and finely chopped: 2cm
garlic cloves: 1
light chicken stock or water: 200ml
spring onions: 1
Sichuan chilli oil (optional): 1tbsp
Sichuan peppercorns: 0.5tsp
cooked white rice: 1
sunflower oil: 1tbsp
-3 medium carrots: 1
pack lamb mince: 500g
tomato purée: 2tbsp
splash Worcestershire sauce: 1
beef stock: 500ml
potatoes: 900g
milk: 3tbsp
-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

**Other Notes**

A list of already-bought ingredients can be used to exclude items from the list, found at ./current_ingredients.txt. For ingredients that appear in multiple recipes, the amounts needed will be added and it will appear as a single ingredient in the final list. It can handle multiple measurement types (e.g. one recipes indicated 10g of an ingredient but the other indicated 1tbsp) and also the same ingredient being singular in one recipe and plural in another. 
