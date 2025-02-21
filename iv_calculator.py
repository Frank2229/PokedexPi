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
        root.after(25, animate_gif, frame_number + 1) # First argument controls the animation speed.
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


def change_selected_pokemon(event):
    '''
    Cycles through pokemon roster.
    '''
    global current_pokemon_index
    if event.keysym == "Left":
        if current_pokemon_index == 0:
            current_pokemon_index = len(my_pokemon_list) - 1
        else:
            current_pokemon_index -= 1
    elif event.keysym == "Right":
        if current_pokemon_index == len(my_pokemon_list) - 1:
            current_pokemon_index = 0
        else:
            current_pokemon_index += 1
    pokemon_image = tk.PhotoImage(file='images/sprites/' + my_pokemon_list[current_pokemon_index][0].lower() + '.gif')
    canvas.itemconfig(canvas.pokemon_image_item, image=pokemon_image)
    canvas.pokemon_image = pokemon_image
    canvas.itemconfig(name_ref, text=my_pokemon_list[current_pokemon_index][0])
    update_stat_table()


def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('IV Calculator')
    root.geometry('480x320')

    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    bg_image = tk.PhotoImage(file='images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    background_overlay_image = tk.PhotoImage(file='images/menus/iv_menu_overlay.png')
    canvas.background_overlay_image = background_overlay_image
    global background_overlay_id
    background_overlay_id = canvas.create_image(0, 0, image=background_overlay_image, anchor="nw")

    return root, canvas


def generate_pokemon_viewer(my_pokemon_list):
    '''
    Generate basic info of currently selected pokemon.
    '''
    global current_pokemon_index

    # Name
    name_ref = canvas.create_text(120, header_y, text=str(my_pokemon_list[current_pokemon_index][0]), font=("Bahnschrift", font_size), fill="white", anchor="center")

    # Level
    canvas.create_text(100, header_y+25, text="Lv:", font=("Bahnschrift", 12), fill="white", anchor="center")
    nature_ref = canvas.create_text(120, header_y+25, text=str(my_pokemon_list[0][2]), font=("Bahnschrift", 12), fill="white", anchor="center")

    # Nature
    canvas.create_text(100, header_y+47, text="Nature:", font=("Bahnschrift", 12), fill="white", anchor="center")
    level_ref = canvas.create_text(150, header_y+47, text=str(my_pokemon_list[0][1]), font=("Bahnschrift", 12), fill="white", anchor="center")

    # Selector Arrows
    arrow_left_image = tk.PhotoImage(file='images/cursors/arrow_left.png')
    canvas.arrow_left_image = arrow_left_image
    global arrow_left_id
    arrow_left_id = canvas.create_image(40, 190, image=arrow_left_image)

    arrow_right_image = tk.PhotoImage(file='images/cursors/arrow.png')
    canvas.arrow_right_image = arrow_right_image
    global arrow_right_id
    arrow_right_id = canvas.create_image(190, 190, image=arrow_right_image)

    # Selected Pokemon Image
    canvas.pokemon_image = tk.PhotoImage(file='images/sprites/' + my_pokemon_list[current_pokemon_index][0].lower() + '.gif')
    canvas.pokemon_image_item = canvas.create_image(120, 190, anchor='center', image=canvas.pokemon_image)
    animate_gif(0)

    return name_ref, level_ref, nature_ref


def generate_stat_table(my_pokemon_list):
    '''
    Populate the stat table with pokemon data.
    Level: Top-left
    Column 1: Base Stats
    Column 2: EVs
    Column 3: IVs
    '''
    column_initial = 330
    column_spacing = 55
    row_top = 95
    row_current = row_top
    row_spacing = 36
    header_x = 265

    canvas.create_text(350, 25, text="IV Calculator", font=("Bahnschrift", font_size), fill="white", anchor="center")

    # Column Titles
    canvas.create_text(column_initial+(0*column_spacing), header_y, text="Base", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(column_initial+(1*column_spacing), header_y, text="EVs", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(column_initial+(2*column_spacing), header_y, text="IVs", font=("Bahnschrift", font_size), fill="white", anchor="center")

    # Row Titles
    canvas.create_text(header_x, row_top + (0*row_spacing), text="HP", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(header_x, row_top + (1*row_spacing), text="Atk", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(header_x, row_top + (2*row_spacing), text="Def", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(header_x, row_top + (3*row_spacing), text="SpA", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(header_x, row_top + (4*row_spacing), text="SpD", font=("Bahnschrift", font_size), fill="white", anchor="center")
    canvas.create_text(header_x, row_top + (5*row_spacing), text="Spe", font=("Bahnschrift", font_size), fill="white", anchor="center")
    
    # Base Stats
    stat_values = []
    stat_ref = []
    for i in range(0, 6):
        stat_values.append(my_pokemon_list[0][4][i])
    for i in range(0, 6):
        stat_ref.append(canvas.create_text(column_initial, row_current, text=str(stat_values[i]), font=("Arial", font_size), fill="white", anchor="center"))
        row_current += row_spacing
        
    column_initial += column_spacing
    row_current = row_top
    
    # EVs
    ev_values = []
    ev_ref = []
    for i in range(0, 6):
        ev_values.append(my_pokemon_list[0][5][i])
    for i in range(0, 6):
        ev_ref.append(canvas.create_text(column_initial, row_current, text=str(ev_values[i]), font=("Arial", font_size), fill="white", anchor="center"))
        row_current += row_spacing
        
    column_initial += column_spacing
    row_current = row_top
    
    # IVs
    iv_values = calculate_ivs(my_pokemon_list[0])
    iv_ref = []
    for i in range(0, 6):
        iv_ref.append(canvas.create_text(column_initial, row_current, text=str(iv_values[i]), font=("Arial", font_size), fill="white", anchor="center"))
        row_current += row_spacing
        
    return stat_ref, ev_ref, iv_ref

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
        with open("my_pokemon.txt", 'r') as file:
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
        with open("my_pokemon.txt", 'w') as file:
            file.write("")
    
    my_pokemon_list = []        
    for key in my_pokemon_dict:
        my_pokemon_list.append((key, my_pokemon_dict.get(key)[0], my_pokemon_dict.get(key)[1], list(my_pokemon_dict.get(key))[2], list(my_pokemon_dict.get(key))[3], list(my_pokemon_dict.get(key))[4]))
    
    return my_pokemon_list


def update_stat_table():
    '''
    Change stat table values after user changes current pokemon.
    '''
    canvas.itemconfig(level_ref, text=my_pokemon_list[current_pokemon_index][1])
    canvas.itemconfig(nature_ref, text=my_pokemon_list[current_pokemon_index][2])
    for i in range(0, 6):
        canvas.itemconfig(stat_ref[i], text=my_pokemon_list[current_pokemon_index][3][i])
    for i in range(0, 6):
        canvas.itemconfig(ev_ref[i], text=my_pokemon_list[current_pokemon_index][5][i])
    iv_values = calculate_ivs(my_pokemon_list[current_pokemon_index])
    for i in range(0, 6):
        canvas.itemconfig(iv_ref[i], text=str(iv_values[i]))
    

def main():
    global root, canvas
    root, canvas = create_window()

    # Initialize Global Variables
    global header_y, font_size, current_pokemon_index, my_pokemon_list
    header_y = 59
    font_size = 16
    current_pokemon_index = 0
    my_pokemon_list = load_my_pokemon_data()
    
    # Generate UI Elements
    global name_ref, level_ref, nature_ref, stat_ref, ev_ref, iv_ref
    name_ref, level_ref, nature_ref = generate_pokemon_viewer(my_pokemon_list)
    stat_ref, ev_ref, iv_ref = generate_stat_table(my_pokemon_list)

    # Keybindings
    root.bind("<Left>", change_selected_pokemon)
    root.bind("<Right>", change_selected_pokemon)

    root.mainloop()


main()
