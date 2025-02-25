import tkinter as tk

def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('Pokemon Data')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='images/menus/pokemon_search_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    return root, canvas


def main():
    root, canvas = create_window()
    
    # Arrow Selector
    global arrow_id, up_menu_offset, down_menu_offset, current_selection
    arrow_select_image = tk.PhotoImage(file='images/cursors/arrow.png')
    canvas.arrow_select_image = arrow_select_image
    arrow_id = canvas.create_image(290, 50, image=arrow_select_image)
    current_selection = 0
    up_menu_offset = -44
    down_menu_offset = 44

    root.mainloop()


main()
