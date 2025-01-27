from tkinter import *
from PIL import Image, ImageTk

# Window Setup
root = Tk()
root.title("IV Calculator")
root.geometry("480x320")
#root.attributes("-fullscreen", True)

# Background Image
backgroundImage = PhotoImage(file = "MenuBackground.png")
backgroundLabel = Label(root, image = backgroundImage)
backgroundLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

# Initialize EV Variables
evValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
for value in evValues:
    value.set(0)
    
# Container for the EV labels.
evLabels = Label(backgroundLabel, padx = 0, pady = 0, bg = "#133a5e")
evLabels.place(relx = 0.775, rely = 0.578, anchor = "center")
evValueLabels = []
for i in range (0, 6):
    evValueLabels.append(Label(evLabels, textvariable = evValues[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
    evValueLabels[i].place(anchor = "center")
    if i == 0:
        evValueLabels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
    elif i == 5:
        evValueLabels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
    else:
        evValueLabels[i].pack(side = "top", padx = 7, pady = 3.5)


# Initialize IV Variables
ivValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
for value in ivValues:
    value.set(0)

# Container for the IV labels.
ivLabels = Label(backgroundLabel, padx = 0, pady = 0, bg = "#133a5e")
ivLabels.place(relx = 0.91, rely = 0.578, anchor = "center")
ivValueLabels = []
for i in range(0, 6):
    ivValueLabels.append(Label(ivLabels, textvariable = ivValues[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
    ivValueLabels[i].place(anchor = "center")
    if i == 0:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
    elif i == 5:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
    else:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = 3.5)

'''
Create the Pokemon selector.
This block iterates through a .txt to retieve all pokemon for the optionmenu.
'''
selectedPokemon = StringVar(root)
selectedPokemon.set("Bulbasaur")
pokemonList = []
with open("NationalPokedex.txt", "r") as file:
    for line in file:
        pokemonList.append(line.strip())

pokemonListSelect = OptionMenu(backgroundLabel, selectedPokemon, *pokemonList)
pokemonListSelect.place(relx = 0.225, rely = 0.25, anchor='center')

'''
Load user data.
If the file does not exist, create one.
'''
myPokemonDict = {}
try:
    with open("MyPokemon.txt", 'r') as file:
         for line in file:
            [pokemonNames, evs] = line.strip().split(":")
            evsList = evs.strip().split(",")
            myPokemonDict[pokemonNames.rstrip()] = evsList
except FileNotFoundError:
    with open("MyPokemon.txt", 'w') as file:
        file.write("")

# Take the extracted file data and organize into a list of tuples.
myPokemonList = []
temp = 0
for key in myPokemonDict:
    myPokemonList.append((key, list(myPokemonDict.get(key))))

root.mainloop()
