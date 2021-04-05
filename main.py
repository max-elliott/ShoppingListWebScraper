from core.shopping_list import create_shopping_list


def main():
    # TODO: Add optional command line parameter to set recipes filepath
    recipes = './recipes/webscraping_recipe_lists/recipe_list.txt'
    create_shopping_list(recipes=recipes)


if __name__ == '__main__':
    main()
