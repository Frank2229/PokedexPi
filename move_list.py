import tkinter as tk

def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('Pokemon Data')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='Images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    return root, canvas


def main():
    root, canvas = create_window()

    root.mainloop()


main()
