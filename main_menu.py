import tkinter as tk
import os

def change_menu_selection(event):
    '''
    Depending on if the user presses 'up' or 'down', change the current_selection variable.
    Check if current menu is the user profile selection or application selection.
    '''
    global current_selection
    if event.keysym == 'Up' and current_selection > 0:
        canvas.move(arrow_id, 0, up_menu_offset)
        current_selection -= 1
    elif event.keysym == 'Down' and current_selection < 5:
        canvas.move(arrow_id, 0, down_menu_offset)
        current_selection += 1


def create_window():
    '''Creates and returns the application window and background.'''
    root = tk.Tk()
    root.title('PokedexPI Menu')
    root.geometry('480x320')
    canvas = tk.Canvas(root, width=480, height=320)
    canvas.pack()

    # Background and Overlay
    bg_image = load_image('images/menus/main_menu_background.png')
    canvas.bg_image = bg_image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    background_overlay_image = load_image('images/menus/main_menu_overlay.png')
    canvas.background_overlay_image = background_overlay_image
    canvas.create_image(0, 0, image=background_overlay_image, anchor="nw")

    # Logo
    logo_image = load_image('images/pokedexpi_logo.png')
    canvas.logo_image = logo_image
    canvas.create_image(130, 140, image=logo_image)
    pokeball_image = load_image('images/pokeball.png')
    canvas.pokeball_image = pokeball_image
    canvas.create_image(130, 190, image=pokeball_image)

    return canvas, root


def initialize_applications():
    '''
    Set a reference for each of the application text objects.
    Create and delete immediately just to set the reference.
    '''
    applications_ref = []
    application_list = ['Pokémon Data', 'Region Maps', 'Type Chart', 'Move List', 'IV Calculator', 'BACK']
    for i in range(0, 6):
        applications_ref.append(canvas.create_text(285, 48 + (i * 44), text=application_list[i], font=('Bahnschrift', 16), fill='white', anchor='w'))
        canvas.itemconfigure(applications_ref[i], state="hidden")

    return applications_ref


def initialize_profiles(user_profiles):
    '''Generate available user profiles.'''
    menu_offset = 44
    profiles_ref = []
    for i in range(0, 5):
        if i < len(user_profiles):
            profiles_ref.append(canvas.create_text(285, 48 + (i * menu_offset), text='User ' + str(i + 1) + ': ' + user_profiles[i], font=('Bahnschrift', 16, 'italic'), fill='white', anchor='w'))
        else:
            profiles_ref.append(canvas.create_text(285, 48 + (i * menu_offset), text='User ' + str(i + 1) + ': Empty', font=('Bahnschrift', 16, 'italic'), fill='white', anchor='w'))
    profiles_ref.append(canvas.create_text(285, 48 + (5 * menu_offset), text='DELETE USER', font=('Bahnschrift', 16), fill='white', anchor='w'))

    return profiles_ref


def load_image(path, fallback=None):
    '''Error handling while loading images.'''
    try:
        return tk.PhotoImage(file=path)
    except tk.TclError as e:
        print(f"Error loading image from {path}: {e}")
        if fallback:
            return tk.PhotoImage(file=fallback)
        return tk.PhotoImage()


def load_profiles():
    '''
    Load all user profiles from user_profiles.txt and generate the available profiles.
    If user_profiles.txt does not exist, write it.
    '''
    user_profiles = []
    try:
        with open('user_profiles.txt', 'r') as file:
            for line in file:
                user_profiles.append(line.strip())
    except FileNotFoundError:
        with open('user_profiles.txt', 'w') as file:
            file.write("")
    except Exception as e:
        print(f"Unexpected error reading user profiles: {e}")
    profiles_ref = initialize_profiles(user_profiles)

    return user_profiles, profiles_ref


def select_menu(event):
    '''
    Based on the current selection, navigate through the menu.
    If the user hasn't selected a profile, set the profile var and switch to menu selection.
    '''
    global is_profile_select, profiles_ref, selected_profile
    if is_profile_select == True:
        for i in range(0, 6):
            canvas.itemconfigure(profiles_ref[i], state='hidden')
            canvas.itemconfigure(applications_ref[i], state='normal')
        selected_profile = current_selection
        is_profile_select = False
    else:
        match current_selection:
            case 0:
                os.system('pokemon_search.py')
            case 1:
                os.system('region_map_viewer.py')
            case 2:
                os.system('type_chart.py')
            case 3:
                os.system('tm_list.py')
            case 4:
                os.system('iv_calculator.py')
            case 5:
                # Bring user back to profile select.
                for i in range(0, 6):
                    canvas.itemconfigure(applications_ref[i], state='hidden')
                    canvas.itemconfigure(profiles_ref[i], state='normal')
                is_profile_select = True


def main():
    # Window Setup
    global canvas, root
    canvas, root = create_window()

    # User Profiles
    global is_profile_select, user_profiles, profiles_ref
    is_profile_select = True    # determines if the current menu is the profile select or application select.
    user_profiles, profiles_ref = load_profiles()

    # Applications Menu
    global applications_ref
    applications_ref = initialize_applications()

    # Arrow Selector
    global arrow_id, up_menu_offset, down_menu_offset, current_selection
    arrow_select_image = tk.PhotoImage(file='images/cursors/arrow.png')
    canvas.arrow_select_image = arrow_select_image
    arrow_id = canvas.create_image(270, 50, image=arrow_select_image)
    current_selection = 0
    up_menu_offset = -44
    down_menu_offset = 44

    # Keybindings
    root.bind("<Up>", change_menu_selection)
    root.bind("<Down>", change_menu_selection)
    root.bind("<Return>", select_menu)

    root.mainloop()


main()
