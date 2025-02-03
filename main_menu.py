import tkinter as tk
import os

def create_button(root, button_text, app_name, canvas, x_position, y_position):
    '''Creates and returns a menu button.'''
    button = tk.Button(root, text=button_text, command=lambda: open_app(app_name), bg='#256063', fg='white', height=2, width=15)
    canvas.create_window(360+(1*x_position), 110+(50*y_position), window=button)

    return button


def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('Pokedex Menu')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='Images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    return root, canvas


def open_app(file_name):
    '''Opens a selected application using a app name argument.'''
    os.system(f"{file_name}")


def main():
    root, canvas = create_window()

    pokemon_data_button= create_button(root, 'Pokemon Data', 'pokemon_data_viewer.py', canvas, 1, 0)  # Pokemon Data button
    pokemon_data_button= create_button(root, 'Region Maps', 'region_map_viewer.py', canvas, 1, 1)   # Region Map button
    pokemon_data_button= create_button(root, 'IV Calculator', 'iv_calculator.py', canvas, 1, 2) # IV Calculator button

    root.mainloop()

main()
