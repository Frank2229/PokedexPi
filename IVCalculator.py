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
evLabels = Label(backgroundLabel, padx = 0, pady = 0)
evLabels.place(relx = 0.775, rely = 0.578, anchor = "center")
evValueLabels = []
for i in range (0, 6):
    evValueLabels.append(Label(evLabels, textvariable = evValues[i], font = ("Arial", 20), fg = "white"))
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
ivLabels = Label(backgroundLabel, padx = 0, pady = 0)
ivLabels.place(relx = 0.91, rely = 0.578, anchor = "center")
ivValueLabels = []
for i in range(0, 6):
    ivValueLabels.append(Label(ivLabels, textvariable = ivValues[i], font = ("Arial", 20), fg = "white"))
    ivValueLabels[i].place(anchor = "center")
    if i == 0:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
    elif i == 5:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
    else:
        ivValueLabels[i].pack(side = "top", padx = 7, pady = 3.5)

selectedPokemon = StringVar(root)
selectedPokemon.set("Bulbasaur")
pokemonList = []
pokemonList.append("Bulbasaur")
pokemonList.append("Ivysaur")
pokemonList.append("Venusaur")
pokemonList.append("Charmander")
pokemonList.append("Charmeleon")
pokemonList.append("Charizard")
pokemonList.append("Squirtle")
pokemonList.append("Wartortle")
pokemonList.append("Blastoise")
pokemonList.append("Caterpie")
pokemonList.append("Metapod")
pokemonList.append("Butterfree")
pokemonList.append("Weedle")
pokemonList.append("Kakuna")
pokemonList.append("Beedrill")

w = OptionMenu(backgroundLabel, selectedPokemon, *pokemonList)
w.place(relx = 0.225, rely = 0.25, anchor='center')

root.mainloop()
