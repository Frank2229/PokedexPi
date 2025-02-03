import tkinter as tk
import os

def open_app(file_name):
    '''Opens a selected application using a app name argument.'''
    os.system(f"{file_name}")


def main():
    root = tk.Tk()
    root.title('Pokedex Menu')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='Images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    iv_calculator_button = tk.Button(root, text='IV Calculator', command=lambda: open_app('IVCalculator.py'))
    canvas.create_window(360, 160, window=iv_calculator_button)

    root.mainloop()

main()
