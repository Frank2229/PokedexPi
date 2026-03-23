import os
import time
import torch
import json
import threading
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image as PILImage
from kivy.config import Config
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu

# 1. HARDWARE & WINDOW CONFIG
Config.set('graphics', 'fullscreen', '0') 
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '0')
Config.set('graphics', 'left', '1920') 

os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel # Required for swiping data
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from picamera2 import Picamera2

# --- AI & DATA WRAPPER ---
class PokedexAI:
    def __init__(self, model_path, num_classes=149):
        self.device = torch.device("cpu")
        self.model = models.resnet18(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes) 
        
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.lore_path = 'assets/data/pokedex_data.json'
        if os.path.exists(self.lore_path):
            with open(self.lore_path, 'r') as f:
                self.pokemon_lore = json.load(f)
        else:
            self.pokemon_lore = {}

        self.class_names = [
            "Abra", "Aerodactyl", "Alakazam", "Arbok", "Arcanine", "Articuno", 
            "Beedrill", "Bellsprout", "Blastoise", "Bulbasaur", "Butterfree", 
            "Caterpie", "Chansey", "Charizard", "Charmander", "Charmeleon", 
            "Clefable", "Clefairy", "Cloyster", "Cubone", "Dewgong", "Diglett", 
            "Ditto", "Dodrio", "Doduo", "Dragonair", "Dragonite", "Dratini", 
            "Drowzee", "Dugtrio", "Eevee", "Ekans", "Electabuzz", "Electrode", 
            "Exeggcute", "Exeggutor", "Farfetch'd", "Fearow", "Flareon", 
            "Gastly", "Gengar", "Geodude", "Gloom", "Golbat", "Goldeen", 
            "Golduck", "Goldeen", "Graveler", "Grimer", "Growlithe", "Gyarados", 
            "Haunter", "Hitmonchan", "Hitmonlee", "Horsea", "Hypno", "Ivysaur", 
            "Jigglypuff", "Jolteon", "Jynx", "Kabuto", "Kabutops", "Kadabra", 
            "Kakuna", "Kangaskhan", "Kingler", "Koffing", "Krabby", "Lapras", 
            "Lickitung", "Machamp", "Machoke", "Machop", "Magikarp", "Magmar", 
            "Magnemite", "Magneton", "Mankey", "Marowak", "Meowth", "Metapod", 
            "Mew", "Mewtwo", "Moltres", "Mr. Mime", "Muk", "Nidoking", "Nidoran-m", 
            "Nidorina", "Nidorino", "Ninetales", "Oddish", "Omanyte", "Omastar", 
            "Onix", "Paras", "Parasect", "Persian", "Pidgeot", "Pidgeotto", "Pidgey", 
            "Pikachu", "Pinsir", "Poliwag", "Poliwhirl", "Poliwrath", "Ponyta", 
            "Porygon", "Primeape", "Psyduck", "Raichu", "Rapidash", "Raticate", 
            "Rattata", "Rhydon", "Rhyhorn", "Sandshrew", "Sandslash", "Scyther", 
            "Seadra", "Seaking", "Seel", "Shellder", "Slowbro", "Slowpoke", 
            "Snorlax", "Spearow", "Squirtle", "Starmie", "Staryu", "Tangela", 
            "Tauros", "Tentacool", "Tentacruel", "Vaporeon", "Venomoth", "Venonat", 
            "Venusaur", "Victreebel", "Vileplume", "Voltorb", "Vulpix", "Wartortle", 
            "Weedle", "Weepinbell", "Weezing", "Wigglytuff", "Zapdos", "Zubat"
        ]

    def predict(self, image_path):
        img = PILImage.open(image_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            outputs = self.model(img_t)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            conf, pred = torch.max(probs, 1)
        return self.class_names[pred.item()], conf.item()

    def get_info(self, name, gen):
        # Access the nested JSON: data[generation][pokemon]
        gen_data = self.pokemon_lore.get(gen, {})
        return gen_data.get(name.lower(), {
            "species": "UNKNOWN", "description": "No data for this gen.",
            "learnset": [], "tm_moves": [], "locations": []
        })

# --- MAIN APPLICATION ---
class PokedexApp(MDApp):
    def build(self):
        # 1. SET WINDOW PROPERTIES MANUALLY
        Window.borderless = True
        Window.fullscreen = False  # Set to False so it respects our coordinates
        
        # 2. FORCE POSITION TO SECOND MONITOR
        # Change 1920 to the exact width of your first monitor
        Window.left = 0
        Window.top = 0
        
        # 3. FORCE SIZE (Matches your Config)
        Window.size = (720, 1280)
        
        self.is_analyzing = False
        self.last_press_time = 0
        self.current_gen = "gen1"
        self.ai_brain = PokedexAI('models/first_poke_model.pth', num_classes=149)
        
        self.root = MDFloatLayout()
        self.root.add_widget(Image(source='assets/images/background.jpg', allow_stretch=True, keep_ratio=False))

        # 1. Main Vertical Stack
        self.main_stack = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=[50, 50, 50, 30], 
            spacing=15 
        )

        # --- A. TOP BANNER ---
        self.id_banner = MDCard(
            size_hint=(1, None), height="100dp",
            md_bg_color=[0.05, 0.38, 0.45, 1], radius=[15,],
            opacity=1 
        )
        self.status_label = MDLabel(
            text="SCAN POKÉMON", halign="center", theme_text_color="Custom", 
            text_color=[1,1,1,1], bold=True, font_style="H4"
        )
        self.id_banner.add_widget(self.status_label)

        # --- B. IMAGE WINDOW ---
        self.display_card = MDCard(
            size_hint=(1, 1), md_bg_color=[0,0,0,1], radius=[20,], 
            elevation=2, padding=[20, 20, 20, 20] 
        )
        self.main_image = Image(fit_mode="contain") 
        self.display_card.add_widget(self.main_image)

        # --- C. THE FULL-WIDTH RESULTS CAROUSEL ---
        # We increase the height slightly to 350dp to handle the bigger text
        self.results_container = MDCard(
            size_hint=(1, None), height="350dp", 
            md_bg_color=[1,1,1,0.1], radius=[15,], opacity=1 
        )
        
        self.main_carousel = Carousel(direction='right', loop=True)

        # Slide 1: Data (Title + Columns + Description Text)
        self.bio_slide_container = MDBoxLayout(
            orientation='vertical',
            padding=[20, 10, 20, 10],
            spacing=0
        )

        # 1. Centered Title
        self.bio_title = MDLabel(
            text="DATA", halign="center", font_style="H5", bold=True,
            theme_text_color="Custom", text_color=[1, 1, 1, 1],
            size_hint_y=None, height="35dp"
        )
        
        # 2. The Two-Column Grid (Property: Value)
        self.grid_anchor = MDBoxLayout(
            orientation='horizontal',
            pos_hint={'center_x': 0.5},
            size_hint=(None, None),
            width="460dp",
            height="175dp" # Adjusted to give columns enough room
        )
        self.bio_keys_label = MDLabel(
            text="", halign="right", font_style="H6",
            theme_text_color="Custom", text_color=[1, 1, 1, 1],
            markup=True, size_hint_x=0.45
        )
        self.bio_values_label = MDLabel(
            text="", halign="left", font_style="H6",
            theme_text_color="Custom", text_color=[0, 1, 1, 1],
            size_hint_x=0.55, padding=[10, 0]
        )
        self.grid_anchor.add_widget(self.bio_keys_label)
        self.grid_anchor.add_widget(self.bio_values_label)

        # 3. THE RAW DESCRIPTION TEXT (No Header)
        self.bio_desc_label = MDLabel(
            text="", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=[1, 1, 1, 1], 
            italic=True, 
            markup=True, 
            font_style="H5",
            line_height=1.1,
            size_hint_y=None,
            height="100dp"
        )

        # Assemble Slide 1
        self.bio_slide_container.add_widget(self.bio_title)
        self.bio_slide_container.add_widget(self.grid_anchor)
        self.bio_slide_container.add_widget(self.bio_desc_label)
        
        # Slide 2: Learnset (Scrollable)
        self.learn_slide_container = MDBoxLayout(
            orientation='vertical',
            padding=[10, 5, 10, 5],
            spacing=0
        )

        # 1. Main Slide Title
        self.learn_title = MDLabel(
            text="LEARNSET", halign="center", font_style="H5", bold=True,
            theme_text_color="Custom", text_color=[1, 1, 1, 1],
            size_hint_y=None, height="40dp"
        )

        self.moves_scroll = ScrollView(size_hint=(1, 1), bar_width="4dp")
        
        # We'll use a BoxLayout inside the ScrollView so we can stack 
        # a "Level Up" section and a "TM" section vertically.
        self.scroll_content = MDBoxLayout(
            orientation='vertical', 
            adaptive_height=True,
            spacing=10
        )

        self.moves_scroll.add_widget(self.scroll_content)
        self.learn_slide_container.add_widget(self.learn_title)
        self.learn_slide_container.add_widget(self.moves_scroll)

        # Slide 3: Base Stats (Vertical Wrapper for Title + Columns)
        self.stats_page_wrapper = MDBoxLayout(
            orientation='vertical',
            padding=[20, 10, 20, 10],
            spacing=10
        )

        # --- THE CENTERED TITLE ---
        self.stats_title = MDLabel(
            text="BASE STATS",
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            bold=True,
            font_style="H5", # Larger font for the title
            size_hint_y=None,
            height="50dp"
        )

        # The Two-Column Container (Inside the wrapper)
        self.stats_columns_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(None, 1), 
            width="450dp",       # Slightly wider to handle the big bars
            pos_hint={'center_x': 0.5},
            spacing=15
        )

        # Column A: Names and Values
        self.stats_names_label = MDLabel(
            text="", halign="right", theme_text_color="Custom", 
            text_color=[1, 1, 1, 1], markup=True, font_style="H5",
            size_hint_x=0.4
        )

        # Column B: The Bars
        self.stats_bars_label = MDLabel(
            text="", halign="left", theme_text_color="Custom", 
            text_color=[0, 1, 1, 1], markup=True, font_style="H5",
            size_hint_x=0.6
        )

        # Assemble Slide 3
        self.stats_columns_layout.add_widget(self.stats_names_label)
        self.stats_columns_layout.add_widget(self.stats_bars_label)
        
        self.stats_page_wrapper.add_widget(self.stats_title)
        self.stats_page_wrapper.add_widget(self.stats_columns_layout)

        # Slide 4: Catch Locations (Scrollable List)
        self.loc_slide_container = MDBoxLayout(
            orientation='vertical',
            padding=[10, 5, 10, 5],
            spacing=0
        )

        # 1. Title
        self.loc_title = MDLabel(
            text="LOCATIONS", halign="center", font_style="H5", bold=True,
            theme_text_color="Custom", text_color=[1, 1, 1, 1],
            size_hint_y=None, height="40dp"
        )

        # 2. Scrollable Grid for Areas
        self.loc_scroll = ScrollView(size_hint=(1, 1), bar_width="4dp")
        
        self.loc_grid = MDGridLayout(
            cols=3,             # Single column is better for long location names
            adaptive_height=True, 
            padding=[20, 10], 
            spacing=10
        )

        # Inside add_move_section()
        grid = MDGridLayout(
            cols=3, 
            adaptive_height=True, # This is the key
            spacing=[10, 5], 
            padding=[5, 5]
        )

        self.loc_scroll.add_widget(self.loc_grid)
        self.loc_slide_container.add_widget(self.loc_title)
        self.loc_slide_container.add_widget(self.loc_scroll)

        # --- FINAL CAROUSEL ASSEMBLY ---
        # Ensure you add them in the order you want to swipe
        self.main_carousel.clear_widgets()
        self.main_carousel.add_widget(self.bio_slide_container) # Slide 1: Data/Desc
        self.main_carousel.add_widget(self.learn_slide_container) # Slide 2: Learnset
        self.main_carousel.add_widget(self.stats_page_wrapper)   # Slide 3: Stats
        self.main_carousel.add_widget(self.loc_slide_container)

        self.results_container.add_widget(self.main_carousel)

        # --- D. BOTTOM NAVIGATION BAR ---
        self.nav_bar = MDBoxLayout(
            orientation='horizontal', 
            size_hint=(1, None), height="140dp",
            spacing=80, # More space between the two big buttons
            padding=[100, 10, 100, 10] 
        )

        # 1. HOME BUTTON (Manual Circular Card)
        self.home_container = MDCard(
            size_hint=(None, None), size=("100dp", "100dp"),
            radius=[50,], # Makes it a perfect circle
            md_bg_color=[0.2, 0.2, 0.2, 1],
            elevation=4,
            pos_hint={'center_y': 0.5}
        )
        self.home_btn = MDIconButton(
            icon="home",
            icon_size="64sp", # MASSIVE ICON
            theme_icon_color="Custom",
            icon_color=[1, 1, 1, 1],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.home_container.add_widget(self.home_btn)

        # 2. ACTION BUTTON (Manual Circular Card)
        self.action_container = MDCard(
            size_hint=(None, None), size=("100dp", "100dp"),
            radius=[50,], 
            md_bg_color=[0.05, 0.38, 0.45, 1],
            elevation=4,
            pos_hint={'center_y': 0.5}
        )
        self.action_btn = MDIconButton(
            icon="camera-iris",
            icon_size="64sp", # MASSIVE ICON
            theme_icon_color="Custom",
            icon_color=[1, 1, 1, 1],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.action_btn.bind(on_press=self.handle_action)
        self.action_container.add_widget(self.action_btn)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "GEN 1 (KANTO)",
                "on_release": lambda x="gen1": self.set_gen(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "GEN 2 (JOHTO)",
                "on_release": lambda x="gen2": self.set_gen(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "GEN 3 (HOENN)",
                "on_release": lambda x="gen3": self.set_gen(x),
            },
        ]
        
        # We define the menu but don't open it yet
        self.gen_menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        # --- UPDATE NAV BAR ---
        # Modify your self.nav_bar padding/spacing to fit 3 buttons
        self.nav_bar.spacing = 40 
        self.nav_bar.padding = [50, 10, 50, 10]

        # 3. GEN SELECTION BUTTON (The Middle Button)
        self.gen_container = MDCard(
            size_hint=(None, None), size=("100dp", "100dp"),
            radius=[50,], 
            md_bg_color=[0.15, 0.15, 0.15, 1],
            elevation=4,
            pos_hint={'center_y': 0.5}
        )
        self.gen_btn = MDIconButton(
            icon="pokeball",
            icon_size="64sp",
            theme_icon_color="Custom",
            icon_color=[1, 1, 1, 1],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.gen_btn.bind(on_release=self.open_gen_menu)
        self.gen_container.add_widget(self.gen_btn)

        # Add it to the nav bar between Home and Camera
        self.nav_bar.add_widget(self.home_container)
        self.nav_bar.add_widget(self.gen_container) # New Middle Button
        self.nav_bar.add_widget(self.action_container)

        # Assembly
        self.main_stack.add_widget(self.id_banner)
        self.main_stack.add_widget(self.display_card)
        self.main_stack.add_widget(self.results_container)
        self.main_stack.add_widget(self.nav_bar)

        self.root.add_widget(self.main_stack)

        # --- AUTO-FOCUS RE-ENABLE ---
        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
            self.picam2.configure(config)
            
            # This line forces the camera to hunt for focus constantly
            self.picam2.set_controls({"AfMode": 2}) # 2 = Continuous Auto Focus
            
            self.picam2.start()
        except Exception as e:
            print(f"Camera Error: {e}")
            self.picam2 = None

        self.camera_clock = Clock.schedule_interval(self.update_viewport, 1.0 / 30.0)
        return self.root

    def handle_action(self, *args):
        if time.time() - self.last_press_time < 1.5: return
        self.last_press_time = time.time()
        if self.is_analyzing: self.enter_live_state()
        else: self.take_photo()

    def update_viewport(self, dt):
        if not self.is_analyzing and self.picam2:
            frame = self.picam2.capture_array()
            if frame is not None:
                if not self.main_image.texture:
                    self.main_image.texture = Texture.create(size=(640, 480), colorfmt='rgb')
                self.main_image.texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                self.main_image.texture.flip_vertical()
                self.main_image.canvas.ask_update()

    def take_photo(self, *args):
        Clock.unschedule(self.camera_clock)
        self.is_analyzing = True
        filename = f"test_images/scan_{int(time.time())}.jpg"
        if self.picam2: self.picam2.capture_file(filename)
        self.main_image.texture = None
        self.main_image.source = filename
        self.id_banner.opacity = 1
        self.action_btn.icon = "refresh"
        self.action_btn.md_bg_color = [0.7, 0.1, 0.1, 1]
        Window.canvas.ask_update()
        threading.Thread(target=self.run_ai, args=(filename,)).start()

    def run_ai(self, filename):
        # 1. Run the Prediction
        name, conf = self.ai_brain.predict(filename)
        
        # 2. Update the UI
        Clock.schedule_once(lambda dt: self.show_result(name, conf), 0)
        
        # 3. --- THE INSTANT DELETE FIX ---
        # We delete it here so it's gone before the user even sees the result
        try:
            # Short sleep to prevent 'File in use' errors on some systems
            time.sleep(0.1) 
            if os.path.exists(filename):
                os.remove(filename)
                print(f"[AI-CLEANUP] Prediction complete. Deleted: {filename}")
        except Exception as e:
            print(f"[ERROR] Auto-delete failed: {e}")

    def show_result(self, name, conf):
        if conf > 0.40:
            info = self.ai_brain.get_info(name, self.current_gen)
            self.status_label.text = f"MATCH FOUND: {name.upper()}"
            self.scroll_content.clear_widgets()
            
            # Retrieve Data from JSON
            species = info.get('species','').upper()
            poke_type = info.get('type','').capitalize()
            height = info.get('height','')
            weight = info.get('weight','')
            ability = info.get('ability','')
            hidden_ability = info.get('hidden_ability','')
            
            # --- POPULATE THE TWO-COLUMN LAYOUT ---
            
            # Set the static property names with bold markup
            self.bio_keys_label.text = "[b]SPECIES:\nTYPE:\nHT:\nWT:\nABILITY:\nH. ABILITY:[/b]"
            
            # Set the dynamic data values
            self.bio_values_label.text = (
                f"{species}\n"
                f"{poke_type}\n"
                f"{height}\n"
                f"{weight}\n"
                f"{ability}\n"
                f"{hidden_ability}"
            )
            
            # Populate Raw Description Text at the bottom
            self.bio_desc_label.text = f"\"{info.get('description', 'No biometric lore available.')}\""
            
            # --- POPULATE LEARNSET GRID ---
            # --- SECTION 1: LEVEL UP ---
            self.add_move_section("BY LEVEL UP", info.get('learnset', []))
            
            # --- SECTION 2: TM / MACHINE ---
            # Assuming your JSON has a key called 'tm_moves' or similar
            self.add_move_section("BY TM / HM", info.get('tm_moves', []))

            # --- SLIDE 3: BASE STATS (The Dual-Column Fix) ---
            base_stats = info.get('base_stats', {})
            names_text = ""
            bars_text = ""
            
            # Mapping long API names to clean 3-letter Pokedex shorts
            stat_map = {
                "HP": "HP", 
                "ATTACK": "ATK", 
                "DEFENSE": "DEF", 
                "SPECIAL-ATTACK": "SPA", 
                "SPECIAL-DEFENSE": "SPD", 
                "SPEED": "SPE"
            }
            
            for s_name, s_val in base_stats.items():
                short_name = stat_map.get(s_name.upper(), s_name[:3].upper())
                
                # Column 1: Labels and Values (Left Aligned in its box)
                names_text += f"[b]{short_name}:[/b] {str(s_val).zfill(3)}\n"
                
                # Column 2: Wide Bars (Left Aligned in its box)
                # Divisor of 5 for wide bars (adjust to 10 if they hit the edge)
                bar_count = max(1, int(s_val / 5)) 
                bars_text += f"{'█' * bar_count}\n"
            
            # Update the two separate labels we defined in build()
            self.stats_names_label.text = names_text
            self.stats_bars_label.text = bars_text

            # --- POPULATE LOCATIONS ---
            self.loc_grid.clear_widgets()
            loc_data = info.get('locations', [])
            
            if not loc_data:
                # Fallback for Starters, Fossils, or Legendaries
                none_label = MDLabel(
                    text="[i]Special Encounter Only\n(Gift, Trade, or Static)[/i]",
                    markup=True, theme_text_color="Custom", text_color=[0.7, 0.7, 0.7, 1],
                    halign="center", size_hint_y=None, height="100dp"
                )
                self.loc_grid.add_widget(none_label)
            else:
                for entry in loc_data:
                    loc_text = (
                        f"[b]{entry['area']}[/b]\n"
                        f"[size=14]Method: {entry['method']} | Chance: {entry['chance']}[/size]"
                    )
                    loc_label = MDLabel(
                        text=loc_text,
                        markup=True,
                        theme_text_color="Custom",
                        text_color=[1, 1, 1, 1],
                        halign="left",
                        size_hint_y=None,
                        height="60dp"
                    )
                    self.loc_grid.add_widget(loc_label)

            # --- UI STATE UPDATE ---
            self.results_container.opacity = 1  
            self.main_carousel.index = 0       
            
            # --- SPRITE SWAP ---
            sprite_path = f"assets/sprites/{name.lower()}.png"
                
            if os.path.exists(sprite_path):
                self.main_image.texture = None
                self.main_image.source = sprite_path
            
        else:
            self.status_label.text = "UNKNOWN POKÉMON"
            self.desc_label.text = "Biometric signature not found in database. Adjust scan angle."
            self.results_container.opacity = 1
            self.main_carousel.index = 1 
        
        Window.canvas.ask_update()

    def add_move_section(self, title, moves_list):
        if not moves_list: return

        # 1. Header (Level Up or TMs)
        header = MDLabel(
            text=f"{title}", halign="center", font_style="Button",
            theme_text_color="Custom", text_color=[0, 1, 1, 1],
            size_hint_y=None, height="40dp", markup=True
        )
        self.scroll_content.add_widget(header)

        # 2. Grid setup
        grid = MDGridLayout(cols=3, adaptive_height=True, spacing=[10, 5], padding=[5, 5])
        
        for item in moves_list:
            lvl = item.get('level', '??')
            move = item.get('move', 'Unknown')
            m_type = item.get('type', 'Normal')
            
            # --- THE SIMPLE OVERRIDE ---
            # If the level is 0 (API default for TMs) or explicitly "TM", show "TM"
            # Otherwise, show "L" + the number
            lvl_str = str(lvl)
            if lvl_str == "0" or lvl_str == "TM":
                display_lvl = "TM"
            else:
                display_lvl = f"L{lvl_str}"
            
            move_label = MDLabel(
                text=f"[b]{display_lvl}:[/b] {move}\n[size=12]({m_type})[/size]",
                markup=True, theme_text_color="Custom", text_color=[1, 1, 1, 1],
                halign="center", size_hint_y=None, height="60dp", font_style="H6"
            )
            grid.add_widget(move_label)
        
        # 3. Add to scroll content
        self.scroll_content.add_widget(grid)

    def enter_live_state(self, *args):
        self.is_analyzing = False
        self.id_banner.opacity = 1
        self.status_label.text = "SCAN POKÉMON"
        self.results_container.opacity = 0
        self.main_image.source = ''
        self.main_image.texture = None
        self.action_btn.icon = "camera-iris"
        self.action_btn.md_bg_color = [0.05, 0.38, 0.45, 1]
        self.camera_clock = Clock.schedule_interval(self.update_viewport, 1.0 / 30.0)
        Window.canvas.ask_update()

    def open_gen_menu(self, instance):
        # This tells the menu where to appear (on top of the pokeball button)
        self.gen_menu.caller = instance
        self.gen_menu.open()

    def set_gen(self, gen_selection):
        # 1. Update the internal generation variable
        self.current_gen = gen_selection
        self.gen_menu.dismiss()
        
        # 2. Update UI colors for visual feedback
        color_map = {
            "gen1": [0.05, 0.38, 0.45, 1], # Teal (Kanto)
            "gen2": [0.7, 0.5, 0.1, 1],    # Gold (Johto)
            "gen3": [0.6, 0.1, 0.1, 1]     # Ruby (Hoenn)
        }
        
        self.id_banner.md_bg_color = color_map.get(gen_selection, [0.2, 0.2, 0.2, 1])
        
        # 3. Update the label so you know what gen you're in
        gen_display = gen_selection.replace("gen", "GENERATION ")
        self.status_label.text = f"ACTIVE: {gen_display}"
        
        # 4. If we were looking at a result, reset to scan mode to avoid data mismatch
        if self.is_analyzing:
            self.enter_live_state()
            
        print(f"Switched to {gen_selection}")

if __name__ == "__main__":
    PokedexApp().run()