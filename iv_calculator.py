import tkinter as tk
import math

def animate_gif(frame_number):
    '''
    Animate gif image recursively.
    Once all frames have been cycled through, start back to frame 0.
    '''
    try:
        canvas.pokemon_image.configure(format=f"gif -index {frame_number}")
        canvas.itemconfig(canvas.pokemon_image_item, image=canvas.pokemon_image)
        root.after(30, animate_gif, frame_number + 1) # First argument controls the animation speed.
    except tk.TclError:
        animate_gif(0)
            

def calculate_ivs(pokemon):
    '''
    Calculates the IVs of a given pokemon given all stats and using the in-game formula.
    Before calculations, declare multiplier vars for each stat based on the pokemon's nature.
    Calculate HP separately with formula variant.
    '''
    multipliers = get_nature_mult(pokemon[1])
    pokemon_ivs = []
    pokemon_ivs.append(math.ceil((100 * (pokemon[4][0] - pokemon[2] - 10)) / pokemon[2]) - (2 * pokemon[3][0]) - (int)(pokemon[5][0] / 4))
    pokemon_ivs[0] = int(pokemon_ivs[0])
    for i in range(1, 6):
        pokemon_ivs.append(((100.0 * (math.ceil(pokemon[4][i] / multipliers[i - 1]) - 5.0)) / pokemon[2]) - (2.0 * pokemon[3][i]) - (int)(pokemon[5][i] / 4.0))
        pokemon_ivs[i] = int(pokemon_ivs[i])

    return pokemon_ivs


def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('IV Calculator')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='Images/menus/iv_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    return root, canvas


def generate_stat_table(my_pokemon_list):
    '''
    Populate the stat table with pokemon data.
    Level: Top-left
    Column 1: Base Stats
    Column 2: EVs
    Column 3: IVs
    '''
    level_ref = canvas.create_text(294, 59, text=str(my_pokemon_list[0][2]), font=("Arial", 20), fill="white", anchor="center")
    
    column_initial = 340
    column_spacing = 55
    row_top = 95
    row_current = row_top
    row_spacing = 36
    
    # Base Stats
    stat_values = []
    stat_ref = []
    for i in range(0, 6):
        stat_values.append(my_pokemon_list[0][4][i])
    for i in range(0, 6):
        stat_ref.append(canvas.create_text(column_initial, row_current, text=str(stat_values[i]), font=("Arial", 20), fill="white", anchor="center"))
        row_current += row_spacing
        
    column_initial += column_spacing
    row_current = row_top
    
    # EVs
    ev_values = []
    ev_ref = []
    for i in range(0, 6):
        ev_values.append(my_pokemon_list[0][5][i])
    for i in range(0, 6):
        ev_ref.append(canvas.create_text(column_initial, row_current, text=str(ev_values[i]), font=("Arial", 20), fill="white", anchor="center"))
        row_current += row_spacing
        
    column_initial += column_spacing
    row_current = row_top
    
    # IVs
    iv_values = calculate_ivs(my_pokemon_list[0])
    iv_ref = []
    for i in range(0, 6):
        iv_ref = canvas.create_text(column_initial, row_current, text=str(iv_values[i]), font=("Arial", 20), fill="white", anchor="center")
        row_current += row_spacing
        
    return level_ref, stat_ref, ev_ref, iv_ref

def get_nature_mult(nature):
    '''
    Determines stat multipliers based on a pokemon's nature.
    Returns a list of all stat multipliers except HP.
    '''
    multipliers = [1.0, 1.0, 1.0, 1.0, 1.0]

    match nature:
        case "Adamant":
            multipliers[0] = 1.1
            multipliers[2] = 0.9
        case "Bold":
            multipliers[1] = 1.1
            multipliers[0] = 0.9
        case "Brave":
            multipliers[0] = 1.1
            multipliers[4] = 0.9
        case "Calm":
            multipliers[3] = 1.1
            multipliers[2] = 0.9
        case "Gentle":
            multipliers[3] = 1.1
            multipliers[1] = 0.9
        case "Hasty":
            multipliers[4] = 1.1
            multipliers[1] = 0.9
        case "Impish":
            multipliers[1] = 1.1
            multipliers[2] = 0.9
        case "Jolly":
            multipliers[4] = 1.1
            multipliers[2] = 0.9
        case "Lax":
            multipliers[1] = 1.1
            multipliers[3] = 0.9
        case "Lonely":
            multipliers[0] = 1.1
            multipliers[1] = 0.9
        case "Mild":
            multipliers[2] = 1.1
            multipliers[1] = 0.9
        case "Modest":
            multipliers[2] = 1.1
            multipliers[0] = 0.9
        case "Naive":
            multipliers[4] = 1.1
            multipliers[3] = 0.9
        case "Naughty":
            multipliers[0] = 1.1
            multipliers[3] = 0.9
        case "Quiet":
            multipliers[2] = 1.1
            multipliers[4] = 0.9
        case "Rash":
            multipliers[2] = 1.1
            multipliers[3] = 0.9
        case "Relaxed":
            multipliers[1] = 1.1
            multipliers[4] = 0.9
        case "Sassy":
            multipliers[3] = 1.1
            multipliers[4] = 0.9
        case "Timid":
            multipliers[4] = 1.1
            multipliers[0] = 0.9

    return multipliers


def load_my_pokemon_data():
    '''
    Load user data and return in a dictionary.
    If the file does not exist, create one.
    '''
    my_pokemon_dict = {}
    try:
        with open("MyPokemon.txt", 'r') as file:
            for line in file:
                print(line)
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
    
    my_pokemon_list = []        
    for key in my_pokemon_dict:
        my_pokemon_list.append((key, my_pokemon_dict.get(key)[0], my_pokemon_dict.get(key)[1], list(my_pokemon_dict.get(key))[2], list(my_pokemon_dict.get(key))[3], list(my_pokemon_dict.get(key))[4]))
    
    return my_pokemon_list


def main():
    global root, canvas
    root, canvas = create_window()
    
    my_pokemon_list = load_my_pokemon_data()
    
    canvas.pokemon_image = tk.PhotoImage(file='images/sprites/charizard.gif')
    canvas.pokemon_image_item = canvas.create_image(105, 175, anchor='center', image=canvas.pokemon_image)
    animate_gif(0)
    
    level_ref, stat_ref, ev_ref, iv_ref = generate_stat_table(my_pokemon_list)

    root.mainloop()


main()
