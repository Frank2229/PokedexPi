import tkinter as tk
import os

def change_menu_selection(event):
    '''Depending on if the user preses 'up' or 'down', change the current_selection variable.'''
    global current_selection
    if event.keysym == "Up" and current_selection > 0:
        canvas.move(arrow_id, 0, up_menu_offset)
        current_selection -= 1
    elif event.keysym == "Down" and current_selection < 5:
        canvas.move(arrow_id, 0, down_menu_offset)
        current_selection += 1


def create_menu_options():
    '''Create all selectable options on the main menu'''
    menu_offset = 44
    canvas.create_text(310, 48 + (0 * menu_offset), text="Pokémon Data", font=("Bahnschrift", 16), fill="white", anchor="w")
    canvas.create_text(310, 48 + (1 * menu_offset), text="Region Maps", font=("Bahnschrift", 16), fill="white", anchor="w")
    canvas.create_text(310, 48 + (2 * menu_offset), text="Type Chart", font=("Bahnschrift", 16), fill="white", anchor="w")
    canvas.create_text(310, 48 + (3 * menu_offset), text="TM/HM List", font=("Bahnschrift", 16), fill="white", anchor="w")
    canvas.create_text(310, 48 + (4 * menu_offset), text="Move List", font=("Bahnschrift", 16), fill="white", anchor="w")
    canvas.create_text(310, 48 + (5 * menu_offset), text="IV Calculator", font=("Bahnschrift", 16), fill="white", anchor="w")


def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('PokedexPI Menu')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    background_overlay_image = tk.PhotoImage(file='images/menus/main_menu_overlay.png')
    canvas.background_overlay_image = background_overlay_image
    global background_overlay_id
    background_overlay_id = canvas.create_image(0, 0, image=background_overlay_image, anchor="nw")

    return root, canvas


def profile_select():
    '''Generate available user profiles.'''
    menu_offset = 44
    canvas.create_text(310, 48 + (0 * menu_offset), text="User 1: ", font=("Bahnschrift", 16, 'italic'), fill="white", anchor="w")
    canvas.create_text(310, 48 + (1 * menu_offset), text="User 2: ", font=("Bahnschrift", 16, 'italic'), fill="white", anchor="w")
    canvas.create_text(310, 48 + (2 * menu_offset), text="User 3: ", font=("Bahnschrift", 16, 'italic'), fill="white", anchor="w")
    canvas.create_text(310, 48 + (3 * menu_offset), text="User 4: ", font=("Bahnschrift", 16, 'italic'), fill="white", anchor="w")
    canvas.create_text(310, 48 + (4 * menu_offset), text="User 5: ", font=("Bahnschrift", 16, 'italic'), fill="white", anchor="w")
    canvas.create_text(310, 48 + (5 * menu_offset), text="Delete User", font=("Bahnschrift", 16), fill="white", anchor="w")

    return 0


def open_app(file_name):
    '''Opens a selected application using a app name argument.'''
    os.system(f"{file_name}")


def select_menu(event):
    '''Based on the current selection, open the corresponding Python application'''
    match current_selection:
        case 0:
            open_app('pokemon_search.py')
        case 1:
            open_app('region_map_viewer.py')
        case 2:
            open_app('type_chart.py')
        case 3:
            open_app('tm_list.py')
        case 4:
            open_app('move_list.py')
        case 5:
            open_app('iv_calculator.py')


def main():
    global canvas, root
    root, canvas = create_window()

    # Logo
    logo_image = tk.PhotoImage(file='images/pokedexpi_logo.png')
    canvas.logo_image = logo_image
    global logo_id
    logo_id = canvas.create_image(130, 140, image=logo_image)
    pokeball_image = tk.PhotoImage(file='images/pokeball.png')
    canvas.pokeball_image = pokeball_image
    global pokeball_id
    pokeball_id = canvas.create_image(130, 190, image=pokeball_image)

    profile_select()
    '''
    # Menu Options
    create_menu_options()
    '''
    # Arrow Selector
    arrow_select_image = tk.PhotoImage(file='images/cursors/arrow.png')
    canvas.arrow_select_image = arrow_select_image
    global arrow_id
    arrow_id = canvas.create_image(295, 50, image=arrow_select_image)
    global up_menu_offset, down_menu_offset
    global current_selection
    current_selection = 0
    up_menu_offset = -44
    down_menu_offset = 44

    # Keybindings
    root.bind("<Up>", change_menu_selection)
    root.bind("<Down>", change_menu_selection)
    root.bind("<Return>", select_menu)

    root.mainloop()


main()
