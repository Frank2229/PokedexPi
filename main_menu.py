import tkinter as tk
import os

def open_app(file_name):
    '''Opens a selected application using a app name argument.'''
    os.system(f"{file_name}")


def main():
    root = tk.Tk()
    root.title("Pokedex Menu")
    root.geometry("480x320")

    iv_calculator_button = tk.Button(root, text="Open IV Calculator", command=lambda: open_app("IVCalculator.py"))
    iv_calculator_button.pack()

    root.mainloop()

main()
