import tkinter as tk
import os

def change_menu_selection(event):
    global current_selection
    if event.keysym == "Up" and current_selection > 0:
        canvas.move(arrow_id, 0, up_menu_offset)
        current_selection -= 1
    elif event.keysym == "Down" and current_selection < 5:
        canvas.move(arrow_id, 0, down_menu_offset)
        current_selection += 1


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

    return root, canvas


def open_app(file_name):
    '''Opens a selected application using a app name argument.'''
    os.system(f"{file_name}")


def select_menu(event):
    if current_selection == 0:
        open_app('pokemon_search.py')
    elif current_selection == 1:
        open_app('region_map_viewer.py')
    elif current_selection == 2:
        open_app('type_chart.py')
    elif current_selection == 3:
        open_app('tm_list.py')
    elif current_selection == 4:
        open_app('move_list.py')
    elif current_selection == 5:
        open_app('iv_calculator.py')


def main():
    global canvas
    root, canvas = create_window()

    '''Arrow selector'''
    arrow_select_image = tk.PhotoImage(file='images/cursors/arrow.png')
    canvas.arrow_select_image = arrow_select_image
    global arrow_id
    arrow_id = canvas.create_image(295, 50, image=arrow_select_image)

    '''Global variables for the movement of the selector arrow'''
    global up_menu_offset, down_menu_offset
    global current_selection
    current_selection = 0
    up_menu_offset = -44
    down_menu_offset = 44

    '''Keybindings'''
    root.bind("<Up>", change_menu_selection)
    root.bind("<Down>", change_menu_selection)
    root.bind("<Return>", select_menu)

    root.mainloop()


main()
