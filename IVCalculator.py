from tkinter import *
from PIL import Image, ImageTk
import math

def calculate_ivs(pokemon):
    '''
    This function calculates the IVs of a given pokemon given all stats and using the in-game formula.
    Before calculations, multipliers are established for each stat based on the pokemon's nature.
    HP calculations are done separately since the formula is different.
    '''
    multipliers = get_nature_mult(pokemon[1])
    pokemon_ivs = []
    pokemon_ivs.append(math.ceil((100 * (pokemon[4][0] - pokemon[2] - 10)) / pokemon[2]) - (2 * pokemon[3][0]) - (int)(pokemon[5][0] / 4))
    pokemon_ivs[0] = int(pokemon_ivs[0])
    for i in range(1, 6):
        pokemon_ivs.append(((100.0 * (math.ceil(pokemon[4][i] / multipliers[i - 1]) - 5.0)) / pokemon[2]) - (2.0 * pokemon[3][i]) - (int)(pokemon[5][i] / 4.0))
        pokemon_ivs[i] = int(pokemon_ivs[i])

    return pokemon_ivs


def load_my_pokemon_data():
    '''
    Load user data.
    If the file does not exist, create one.
    '''
    my_pokemon_dict = {}
    try:
        with open("MyPokemon.txt", 'r') as file:
            for line in file:
                [pokemon_names, nature, level, base, stats, evs] = line.strip().split(":")
                base_list = base.strip().split(",")
                stats_list = stats.strip().split(",")
                evs_list = evs.strip().split(",")
                level = int(level)
                for i in range(0, 6):
                    base_list[i] = int(base_list[i])
                    stats_list[i] = int(stats_list[i])
                    evs_list[i] = int(evs_list[i])
                my_pokemon_dict[pokemon_names.rstrip()] = (nature, level, base_list, stats_list, evs_list)
    except FileNotFoundError:
        with open("MyPokemon.txt", 'w') as file:
            file.write("")

    return my_pokemon_dict


def get_nature_mult(nature):
    '''
    This function determins stat multipliers based on a pokemon's nature.
    Returns a list of all stat multipliers except HP.
    '''
    multipliers = [1.0, 1.0, 1.0, 1.0, 1.0]

    if nature == "Adamant":
        multipliers[0] = 1.1
        multipliers[2] = 0.9
    elif nature == "Bold":
        multipliers[1] = 1.1
        multipliers[0] = 0.9
    elif nature == "Brave":
        multipliers[0] = 1.1
        multipliers[4] = 0.9
    elif nature == "Calm":
        multipliers[3] = 1.1
        multipliers[2] = 0.9
    elif nature == "Gentle":
        multipliers[3] = 1.1
        multipliers[1] = 0.9
    elif nature == "Hasty":
        multipliers[4] = 1.1
        multipliers[1] = 0.9
    elif nature == "Impish":
        multipliers[1] = 1.1
        multipliers[2] = 0.9
    elif nature == "Jolly":
        multipliers[4] = 1.1
        multipliers[2] = 0.9
    elif nature == "Lax":
        multipliers[1] = 1.1
        multipliers[3] = 0.9
    elif nature == "Lonely":
        multipliers[0] = 1.1
        multipliers[1] = 0.9
    elif nature == "Mild":
        multipliers[2] = 1.1
        multipliers[1] = 0.9
    elif nature == "Modest":
        multipliers[2] = 1.1
        multipliers[0] = 0.9
    elif nature == "Naive":
        multipliers[4] = 1.1
        multipliers[3] = 0.9
    elif nature == "Naughty":
        multipliers[0] = 1.1
        multipliers[3] = 0.9
    elif nature == "Quiet":
        multipliers[2] = 1.1
        multipliers[4] = 0.9
    elif nature == "Rash":
        multipliers[2] = 1.1
        multipliers[3] = 0.9
    elif nature == "Relaxed":
        multipliers[1] = 1.1
        multipliers[4] = 0.9
    elif nature == "Sassy":
        multipliers[3] = 1.1
        multipliers[4] = 0.9
    elif nature == "Timid":
        multipliers[4] = 1.1
        multipliers[0] = 0.9

    return multipliers


def main():
    root = Tk()
    root.title("IV Calculator")
    root.geometry("480x320")
    #root.attributes("-fullscreen", True)

    background_image = PhotoImage(file = "MenuBackground.png")
    background_label = Label(root, image = background_image)
    background_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    my_pokemon_dict = load_my_pokemon_data()

    '''
    Take the extracted file data and organize into a list of tuples.
    Tuple indices: 0 = name, 1 = level, 2 = evs list
    '''
    my_pokemon_list = []
    temp = 0
    for key in my_pokemon_dict:
        my_pokemon_list.append((key, my_pokemon_dict.get(key)[0], my_pokemon_dict.get(key)[1], list(my_pokemon_dict.get(key))[2], list(my_pokemon_dict.get(key))[3], list(my_pokemon_dict.get(key))[4]))

    '''
    Create the Pokemon selector.
    This block iterates through a .txt to retieve all pokemon for the optionmenu.
    '''
    selected_pokemon = StringVar(root)
    if len(my_pokemon_list) == 0:
        selected_pokemon.set("Bulbasaur")
    else:
        selected_pokemon.set(my_pokemon_list[0][0])
    pokemon_list = []
    with open("NationalPokedex.txt", "r") as file:
        for line in file:
            pokemon_list.append(line.strip())
    pokemon_list_select = OptionMenu(background_label, selected_pokemon, *pokemon_list)
    pokemon_list_select.place(relx = 0.125, rely = 0.25, anchor='center')

    # Setup nature
    nature_selected = StringVar(root)
    if len(my_pokemon_list) == 0:
        nature_selected.set("Bulbasaur")
    else:
        nature_selected.set(my_pokemon_list[0][1])
    nature_list = []
    with open("Natures.txt", "r") as file:
        for line in file:
            nature_list.append(line.strip())
    natures_list_select = OptionMenu(background_label, nature_selected, *nature_list)
    natures_list_select.place(relx = 0.325, rely = 0.25, anchor = "center")

    # Setup level
    pokemon_lvl = IntVar()
    if len(my_pokemon_list) == 0:
        pokemon_lvl.set(0)
    else:
        pokemon_lvl.set(my_pokemon_list[0][2])
    lvl_label = Label(background_label, padx = 7, pady = 0, textvariable = pokemon_lvl, font = ("Arial", 14), fg = "white", bg = "#1f5387")
    lvl_label.place(relx = 0.6, rely = 0.185, anchor = "center")

    # Initialize and Setup Stat Variables
    stat_values = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
    temp = 0
    for value in stat_values:
        if len(my_pokemon_list) == 0:
            value.set(0)
        else:
            value.set(my_pokemon_list[0][4][temp])
        temp += 1
    stat_labels = Label(background_label, padx = 0, pady = 0, bg = "#133a5e")
    stat_labels.place(relx = 0.71, rely = 0.578, anchor = "center")
    stat_value_labels = []
    for i in range (0, 6):
        stat_value_labels.append(Label(stat_labels, textvariable = stat_values[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
        stat_value_labels[i].place(anchor = "center")
        if i == 0:
            stat_value_labels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
        elif i == 5:
            stat_value_labels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
        else:
            stat_value_labels[i].pack(side = "top", padx = 7, pady = 3.5)

    # Initialize and Setup EV Variables
    ev_values = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
    temp = 0
    for value in ev_values:
        if len(my_pokemon_list) == 0:
            value.set(0)
        else:
            value.set(my_pokemon_list[0][5][temp])
        temp += 1
    ev_labels = Label(background_label, padx = 0, pady = 0, bg = "#133a5e")
    ev_labels.place(relx = 0.83, rely = 0.578, anchor = "center")
    ev_value_labels = []
    for i in range (0, 6):
        ev_value_labels.append(Label(ev_labels, textvariable = ev_values[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
        ev_value_labels[i].place(anchor = "center")
        if i == 0:
            ev_value_labels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
        elif i == 5:
            ev_value_labels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
        else:
            ev_value_labels[i].pack(side = "top", padx = 7, pady = 3.5)

    # Initialize and Setup IV Variables
    my_ivs = calculate_ivs(my_pokemon_list[0])
    iv_values = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
    temp = 0
    for value in iv_values:
        if len(my_pokemon_list) == 0:
            value.set(0)
        else:
            value.set(my_ivs[temp])
        temp += 1
    iv_labels = Label(background_label, padx = 0, pady = 0, bg = "#133a5e")
    iv_labels.place(relx = 0.932, rely = 0.578, anchor = "center")
    iv_value_labels = []
    for i in range(0, 6):
        iv_value_labels.append(Label(iv_labels, textvariable = iv_values[i], font = ("Arial", 14), fg = "white", bg = "#133a5e"))
        iv_value_labels[i].place(anchor = "center")
        if i == 0:
            iv_value_labels[i].pack(side = "top", padx = 7, pady = (0, 3.5))
        elif i == 5:
            iv_value_labels[i].pack(side = "top", padx = 7, pady = (3.5, 0))
        else:
            iv_value_labels[i].pack(side = "top", padx = 7, pady = 3.5)

    root.mainloop()

main()
