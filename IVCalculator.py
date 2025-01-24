from tkinter import *
from PIL import ImageTk

root = Tk()
root.title("IV Calculator")
root.geometry("480x320")

img = PhotoImage(file = 'menu_background.png')
img_label = Label(root, image = img)

img_label.place(x = 0, y = 0)

root.mainloop()
