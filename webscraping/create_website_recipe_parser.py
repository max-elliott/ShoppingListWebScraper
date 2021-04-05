from webscraping import website_scraper
from webscraping.constants import IMPLEMENTED_WEBSITES


def create_website_recipe_parser(website_link):
    for website in IMPLEMENTED_WEBSITES:
        if website.lower() in website_link.lower():
            class_name = website + 'RecipeParser'
            actual_class = getattr(website_scraper, class_name)
            return actual_class(website_link)
    raise ValueError(f"No website parser currently implemented for {website_link}")


if __name__ == '__main__':
    test_link = 'https://www.bbcgoodfood.com/recipes/roasted-aubergine-tomato-curry'
    s = create_website_recipe_parser(test_link)
    s.scrape_recipe()

    print(s.recipe)

    test_link = 'https://www.bbcgoodfood.com/recipes/carrot-cake'
    s = create_website_recipe_parser(test_link)
    s.scrape_recipe()



    print(s.recipe)