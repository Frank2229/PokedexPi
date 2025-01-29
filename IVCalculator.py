from tkinter import *
from PIL import Image, ImageTk

def calculateIVs(pokemon, index):
    pokemonIVs = []
    pokemonIVs.append(((100 * (pokemon[4][0] - pokemon[2] - 10)) / pokemon[2]) - (2 * pokemon[3][0]) - (pokemon[5][0] / 4))
    for i in range(1, 6):
        pokemonIVs.append()
    return 0

# Window Setup
root = Tk()
root.title("IV Calculator")
root.geometry("480x320")
#root.attributes("-fullscreen", True)

# Background Image
backgroundImage = PhotoImage(file = "MenuBackground.png")
backgroundLabel = Label(root, image = backgroundImage)
backgroundLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

'''
Load user data.
If the file does not exist, create one.
'''
myPokemonDict = {}
try:
    with open("MyPokemon.txt", 'r') as file:
         for line in file:
            [pokemonNames, nature, level, base, stats, evs] = line.strip().split(":")
            baseList = base.strip().split(",")
            statsList = stats.strip().split(",")
            evsList = evs.strip().split(",")
            myPokemonDict[pokemonNames.rstrip()] = (nature, level, baseList, statsList, evsList)
except FileNotFoundError:
    with open("MyPokemon.txt", 'w') as file:
        file.write("")

'''
Take the extracted file data and organize into a list of tuples.
Tuple indices: 0 = name, 1 = level, 2 = evs list
'''
myPokemonList = []
temp = 0
for key in myPokemonDict:
    myPokemonList.append((key, myPokemonDict.get(key)[0], myPokemonDict.get(key)[1], list(myPokemonDict.get(key))[2], list(myPokemonDict.get(key))[3], list(myPokemonDict.get(key))[4]))

'''
Create the Pokemon selector.
This block iterates through a .txt to retieve all pokemon for the optionmenu.
'''
selectedPokemon = StringVar(root)
if len(myPokemonList) == 0:
    selectedPokemon.set("Bulbasaur")
else:
    selectedPokemon.set(myPokemonList[0][0])
pokemonList = []
with open("NationalPokedex.txt", "r") as file:
    for line in file:
        pokemonList.append(line.strip())
pokemonListSelect = OptionMenu(backgroundLabel, selectedPokemon, *pokemonList)
pokemonListSelect.place(relx = 0.125, rely = 0.25, anchor='center')

# Setup nature
natureSelected = StringVar(root)
if len(myPokemonList) == 0:
    natureSelected.set("Bulbasaur")
else:
    natureSelected.set(myPokemonList[0][1])
natureList = []
with open("Natures.txt", "r") as file:
    for line in file:
        natureList.append(line.strip())
naturesListSelect = OptionMenu(backgroundLabel, natureSelected, *natureList)
naturesListSelect.place(relx = 0.325, rely = 0.25, anchor = "center")

# Setup level
pokemonLvl = IntVar()
if len(myPokemonList) == 0:
    pokemonLvl.set(0)
else:
    pokemonLvl.set(myPokemonList[0][2])
lvlLabel = Label(backgroundLabel, padx = 7, pady = 0, textvariable = pokemonLvl, font = ("Arial", 14), fg = "white", bg = "#1f5387")
lvlLabel.place(relx = 0.6, rely = 0.185, anchor = "center")

# Initialize Stat Variables
statValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
temp = 0
for value in statValues:
    if len(myPokemonList) == 0:
        value.set(0)
    else:
        value.set(myPokemonList[0][4][temp])
    temp += 1

# Container for the Stat labels.
statLabels = Label(backgroundLabel, padx = 0, pady = 0, bg = "#133a5e")
statLabels.place(relx = 0.71, rely = 0.578, anchor = "center")
statValueLabels = []
for i in range (0, 6):
    statValueLabels.append(Label(statLabels, textvariable = statValues[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
    statValueLabels[i].place(anchor = "center")
    if i == 0:
        statValueLabels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
    elif i == 5:
        statValueLabels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
    else:
        statValueLabels[i].pack(side = "top", padx = 7, pady = 3.5)

# Initialize EV Variables
evValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
temp = 0
for value in evValues:
    if len(myPokemonList) == 0:
        value.set(0)
    else:
        value.set(myPokemonList[0][5][temp])
    temp += 1
    
# Container for the EV labels.
evLabels = Label(backgroundLabel, padx = 0, pady = 0, bg = "#133a5e")
evLabels.place(relx = 0.83, rely = 0.578, anchor = "center")
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
ivLabels.place(relx = 0.932, rely = 0.578, anchor = "center")
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

root.mainloop()
