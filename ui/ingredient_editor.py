main_menu = '''
Ingredient Editor
-----------------
Choose one of the following options:
c -> create a new ingredient
u -> update an ingredient
d -> delete an ingredient
q -> quit
'''

new_ingredient_menu = '''
Create New Ingredient
---------------------
b -> go back
m -> main menu
s -> skip

'''

trail = []

def go_to(screen_func):
    trail.append()
    screen_func()

def go_back():
    back_func = trail.pop()
    back_func()

def main():
    go_to(main_menu)

def main_menu():
    trail = []    
    option = input(main_menu)
    if option == "q":
        return
    elif option == "c":
        go_to(new_ingredient)
    else:
        print('unrecognised option: ', option)
        main()

def new_ingredient():
    # Get a fresh ingredient;
    i = ingredient_factory.new_ingredient_data()
    # Cycle through the ingredient's properties;
    for prop in i.keys():
        if isinstance(dict)
    option = input(new_ingredient_menu)
    if option == 'b':
        go_back()
    elif option == 'm':
        go_to(main_menu)
    else

main()