"""
PokedexPi: A Multi-Module Handheld Pokémon Encyclopedia
Built for Raspberry Pi 5 with KivyMD and Libcamera.
Features: AI Image Identification, Multi-Gen Data Support, and Module Navigation.
"""

import os
import time
import torch
import json
import threading
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image as PILImage

# Kivy & UI Framework
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivy.animation import Animation

# KivyMD Components
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu

# Hardware Interface
from picamera2 import Picamera2

# --- 1. GLOBAL WINDOW CONFIGURATION ---
# Optimized for 7-inch Raspberry Pi Display
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '0')
Config.set('graphics', 'left', '1920') 
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

# --- 2. REGIONAL COORDINATE DATABASE ---
MAP_DATA = {
    "KANTO": {
        "Pallet Town": {"pos": (0.24, 0.22), "info": "Home of Prof. Oak."},
        "Viridian City": {"pos": (0.24, 0.35), "info": "Gym: Giovanni (Ground)."},
        "Pewter City": {"pos": (0.24, 0.72), "info": "Gym: Brock (Rock)."},
        "Cerulean City": {"pos": (0.71, 0.81), "info": "Gym: Misty (Water)."},
        "Vermilion City": {"pos": (0.71, 0.45), "info": "Gym: Lt. Surge (Electric)."},
        "Lavender Town": {"pos": (0.88, 0.58), "info": "Pokemon Tower."},
        "Celadon City": {"pos": (0.58, 0.58), "info": "Gym: Erika (Grass)."},
        "Saffron City": {"pos": (0.71, 0.58), "info": "Gym: Sabrina (Psychic)."},
        "Fuchsia City": {"pos": (0.58, 0.22), "info": "Gym: Koga (Poison)."},
        "Cinnabar Island": {"pos": (0.24, 0.10), "info": "Gym: Blaine (Fire)."},
        "Indigo Plateau": {"pos": (0.12, 0.85), "info": "The Pokemon League."}
    },
    "JOHTO": {
        "New Bark Town": {"pos": (0.85, 0.35), "info": "Home of Prof. Elm."},
        "Goldenrod City": {"pos": (0.32, 0.40), "info": "Gym: Whitney (Normal)."},
        "Ecruteak City": {"pos": (0.45, 0.65), "info": "Gym: Morty (Ghost)."}
    },
    "HOENN": {
        "Littleroot Town": {"pos": (0.25, 0.15), "info": "Home of Prof. Birch."},
        "Rustboro City": {"pos": (0.15, 0.55), "info": "Gym: Roxanne (Rock)."},
        "Ever Grande City": {"pos": (0.92, 0.15), "info": "Hoenn League."}
    }
}

class PokedexAI:
    """Handles ResNet-18 model inference and local Pokedex data retrieval."""
    
    def __init__(self, model_path, num_classes=149):
        self.device = torch.device("cpu")
        
        # Load Architecture
        self.model = models.resnet18(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        
        # Load Weights
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

        # Image Preprocessing Pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Load Pokedex JSON Data
        self.lore_path = 'assets/data/pokedex_data.json'
        self.pokemon_lore = {}
        if os.path.exists(self.lore_path):
            with open(self.lore_path, 'r') as f:
                self.pokemon_lore = json.load(f)

        # Mapping Model Indices to Species Names
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
        """Processes an image and returns (Species, Confidence Score)."""
        img = PILImage.open(image_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            outputs = self.model(img_t)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            conf, pred = torch.max(probs, 1)
        return self.class_names[pred.item()], conf.item()

    def get_info(self, name, gen):
        """Fetches Gen-specific data from the nested JSON dictionary."""
        gen_data = self.pokemon_lore.get(gen, {})
        return gen_data.get(name.lower(), {
            "species": "UNKNOWN", "description": "No data for this gen.",
            "learnset": [], "tm_moves": [], "locations": []
        })

class MapScreen(Screen):
    """Module for regional map navigation and POI discovery."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDFloatLayout()
        
        # 1. THE BACKGROUND (Absolute Bottom)
        self.layout.add_widget(Image(
            source='assets/images/background.jpg', 
            allow_stretch=True, keep_ratio=False
        ))
        
        # 2. THE MAP CONTAINER 
        # We use a height based on width to maintain a standard map aspect ratio
        self.map_frame = MDFloatLayout(
            size_hint=(0.95, None),
            height=Window.width * 0.95 * (0.75), 
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        # 3. THE MAP IMAGE (Base layer of the frame)
        self.map_image = Image(
            source='assets/maps/kanto.jpg', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True, 
            keep_ratio=True
        )
        
        # 4. THE SCAN LINE (Overlays map image)
        self.scan_line = MDCard(
            size_hint=(1, None), height="3dp",
            md_bg_color=[0, 1, 1, 0.6], 
            pos_hint={'center_x': 0.5, 'center_y': 1},
            opacity=0
        )

        # IMPORTANT: Add Map FIRST, then Scan Line to ensure correct Z-indexing
        self.map_frame.add_widget(self.map_image)
        self.map_frame.add_widget(self.scan_line)
        self.layout.add_widget(self.map_frame)
        
        # 5. UI OVERLAYS (Header and Info Card)
        self.region_label = MDLabel(
            text="KANTO REGION", halign="center", font_style="H4",
            theme_text_color="Custom", text_color=[1, 1, 1, 1],
            bold=True, pos_hint={'center_y': 0.88}
        )
        self.layout.add_widget(self.region_label)

        self.info_card = MDCard(
            size_hint=(0.9, None), 
            height="100dp",
            pos_hint={'center_x': 0.5, 'y': 0.12},
            md_bg_color=[0, 0, 0, 0.75], 
            radius=[15,],
            opacity=0, 
            elevation=2
        )
        
        self.location_info_label = MDLabel(
            text="", halign="center", theme_text_color="Custom",
            text_color=[0, 1, 1, 1], bold=True, padding=[15, 10],
            markup=True, font_style="H6" 
        )
        self.info_card.add_widget(self.location_info_label)
        self.layout.add_widget(self.info_card)

        # 6. NAVIGATION BAR
        self._build_nav_bar()
        
        # 7. REGION SELECTION DROPDOWN
        map_items = [
            {"viewclass": "OneLineListItem", "text": "KANTO", "on_release": lambda x="KANTO", i="kanto.jpg": self.change_map(x, i)},
            {"viewclass": "OneLineListItem", "text": "JOHTO", "on_release": lambda x="JOHTO", i="johto.jpg": self.change_map(x, i)},
            {"viewclass": "OneLineListItem", "text": "HOENN", "on_release": lambda x="HOENN", i="hoenn.jpg": self.change_map(x, i)},
        ]
        self.map_menu = MDDropdownMenu(items=map_items, width_mult=4)

        self.add_widget(self.layout)

    def _build_nav_bar(self):
        self.nav_bar = MDBoxLayout(
            orientation='horizontal', size_hint=(1, None), height="140dp",
            spacing=40, padding=[50, 10, 50, 10], pos_hint={'center_x': 0.5, 'y': 0}
        )
        
        # Home
        home_box = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.2, 0.2, 0.2, 1])
        home_box.add_widget(MDIconButton(icon="home", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=lambda x: self.go_home()))
        
        # Menu
        menu_box = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.15, 0.15, 0.15, 1])
        menu_box.add_widget(MDIconButton(icon="map-search", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=self.open_map_menu))
        
        # GPS
        gps_box = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.05, 0.38, 0.45, 1])
        gps_box.add_widget(MDIconButton(icon="crosshairs-gps", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=self.start_gps_scan))

        self.nav_bar.add_widget(home_box); self.nav_bar.add_widget(menu_box); self.nav_bar.add_widget(gps_box)
        self.layout.add_widget(self.nav_bar)

    def start_gps_scan(self, *args):
        self.info_card.opacity = 0 
        self.scan_line.opacity = 1
        self.scan_line.pos_hint = {'center_y': 1}
        
        # Animation requires: from kivy.animation import Animation at the top of main.py
        anim = Animation(pos_hint={'center_y': 0}, duration=1.5, t='in_out_quad')
        anim.bind(on_complete=lambda *x: self.plot_locations(self.region_label.text.split()[0]))
        anim.start(self.scan_line)

    def plot_locations(self, region_name):
        # 1. Clean up only existing markers
        for child in list(self.map_frame.children):
            if isinstance(child, MDIconButton) and child.icon == "map-marker-radius":
                self.map_frame.remove_widget(child)

        region_key = region_name.upper()
        if region_key in MAP_DATA:
            for loc_name, data in MAP_DATA[region_key].items():
                marker = MDIconButton(
                    icon="map-marker-radius",
                    theme_icon_color="Custom", icon_color=[1, 0, 0, 1],
                    pos_hint={'center_x': data['pos'][0], 'center_y': data['pos'][1]},
                    on_release=lambda x, n=loc_name, i=data['info']: self.update_info_bar(n, i)
                )
                self.map_frame.add_widget(marker)
        
        Animation(opacity=0, duration=0.5).start(self.scan_line)

    def update_info_bar(self, name, info):
        self.location_info_label.text = (
            f"[size=28sp][b]{name.upper()}[/b][/size]\n"
            f"[size=20sp]{info}[/size]"
        )
        Animation(opacity=1, duration=0.3).start(self.info_card)

    def open_map_menu(self, instance):
        self.map_menu.caller = instance
        self.map_menu.open()

    def change_map(self, name, img_path):
        self.region_label.text = f"{name} REGION"
        self.map_image.source = f'assets/maps/{img_path}'
        self.map_menu.dismiss()
        self.info_card.opacity = 0
        # Clear markers when switching maps
        self.plot_locations("CLEAR")

    def go_home(self):
        self.manager.current = 'menu'

class PokedexApp(MDApp):
    """Main UI Application for the PokedexPi."""

    def build(self):
        # Window & State Initialization
        Window.borderless = True
        Window.left, Window.top = 0, 0
        Window.size = (720, 1280)
        
        self.is_analyzing = False
        self.last_press_time = 0
        self.current_gen = "gen1"
        self.ai_brain = PokedexAI('models/first_poke_model.pth', num_classes=149)
        
        # UI Navigation System
        self.sm = ScreenManager(transition=FadeTransition())
        self.menu_screen = Screen(name='menu')
        self.id_screen = Screen(name='identifier')
        self.map_screen = MapScreen(name='maps')
        
        self.menu_screen.add_widget(self.create_menu_layout())
        self.id_screen.add_widget(self.create_identifier_layout())

        self.sm.add_widget(self.menu_screen)
        self.sm.add_widget(self.id_screen)
        self.sm.add_widget(self.map_screen)

        # Hardware Camera Initialization
        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
            self.picam2.configure(config)
            self.picam2.set_controls({"AfMode": 2}) # Continuous Auto-Focus
            self.picam2.start()
        except Exception as e:
            print(f"Camera Initialization Failed: {e}")
            self.picam2 = None

        # Start Camera Thread (30 FPS)
        self.camera_clock = Clock.schedule_interval(self.update_viewport, 1.0 / 30.0)
        
        self.sm.current = 'menu'
        return self.sm

    # --- MENU MODULE ---
    def create_menu_layout(self):
        """Constructs the high-tech module launcher screen."""
        layout = MDFloatLayout()
        layout.add_widget(Image(source='assets/images/background.jpg', allow_stretch=True, keep_ratio=False))
        
        # Logo Assembly (Overlapping Logo and Pokeball)
        logo_assembly = MDFloatLayout(size_hint=(1, None), height="220dp", pos_hint={'top': 0.9})

        pokeball_img = Image(
            source='assets/icons/pokeball.png', 
            size_hint=(None, None), size=("110dp", "110dp"),
            allow_stretch=True, keep_ratio=True,
            pos_hint={'center_x': 0.8, 'center_y': 0.3}
        )
        pokedex_logo_img = Image(
            source='assets/icons/pokedexpi_logo.png',
            size_hint=(0.7, 1), fit_mode="contain",
            pos_hint={'center_x': 0.42, 'top': 0.8}
        )

        logo_assembly.add_widget(pokeball_img)
        logo_assembly.add_widget(pokedex_logo_img)
        layout.add_widget(logo_assembly)

        # Module Cards
        center_box = MDBoxLayout(orientation='vertical', size_hint=(0.8, 0.55), pos_hint={'center_x': 0.5, 'top': 0.70}, spacing=30)
        modules = [
            ("POKÉMON IDENTIFIER", "camera-iris", "identifier"),
            ("IV CALCULATOR", "calculator", "menu"),
            ("REGIONAL MAPS", "map-legend", "maps")
        ]

        for name, icon, target in modules:
            btn_card = MDCard(
                orientation='vertical', padding=20, spacing=10,
                md_bg_color=[0.05, 0.38, 0.45, 1], radius=[15,],
                on_release=lambda x, t=target: self.change_screen(t)
            )
            btn_card.add_widget(MDIconButton(icon=icon, pos_hint={'center_x': 0.5}, theme_icon_color="Custom", icon_color=[1,1,1,1], icon_size="48sp"))
            btn_card.add_widget(MDLabel(text=name, halign="center", theme_text_color="Custom", text_color=[1,1,1,1], bold=True))
            center_box.add_widget(btn_card)
        
        layout.add_widget(center_box)
        return layout

    def change_screen(self, name):
        """Handles Screen Transitions."""
        self.sm.current = name

    # --- IDENTIFIER MODULE ---
    def create_identifier_layout(self):
        """Constructs the Scanner UI with Carousel and Navigation Bar."""
        root = MDFloatLayout()
        root.add_widget(Image(source='assets/images/background.jpg', allow_stretch=True, keep_ratio=False))

        self.main_stack = MDBoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50, 50, 50, 30], spacing=15)

        # Top ID Banner
        self.id_banner = MDCard(size_hint=(1, None), height="100dp", md_bg_color=[0.05, 0.38, 0.45, 1], radius=[15,])
        self.status_label = MDLabel(text="SCAN POKÉMON", halign="center", theme_text_color="Custom", text_color=[1,1,1,1], bold=True, font_style="H4")
        self.id_banner.add_widget(self.status_label)

        # Main Camera Viewport
        self.display_card = MDCard(size_hint=(1, 1), md_bg_color=[0,0,0,1], radius=[20,])
        self.main_image = Image(fit_mode="contain") 
        self.display_card.add_widget(self.main_image)

        # Results Data Carousel
        self.results_container = MDCard(size_hint=(1, None), height="350dp", md_bg_color=[1,1,1,0.1], radius=[15,], opacity=0)
        self.main_carousel = Carousel(direction='right', loop=True)
        
        # Build Slides
        self._build_bio_slide()
        self._build_learnset_slide()
        self._build_stats_slide()
        self._build_loc_slide()

        self.results_container.add_widget(self.main_carousel)

        # Navigation Bar Assembly
        self._build_nav_bar()

        self.main_stack.add_widget(self.id_banner)
        self.main_stack.add_widget(self.display_card)
        self.main_stack.add_widget(self.results_container)
        self.main_stack.add_widget(self.nav_bar)
        
        # Generation Dropdown Menu
        menu_items = [{"viewclass": "OneLineListItem", "text": f"GEN {i} ({['KANTO','JOHTO','HOENN'][i-1]})", "on_release": lambda x=f"gen{i}": self.set_gen(x)} for i in range(1,4)]
        self.gen_menu = MDDropdownMenu(items=menu_items, width_mult=4)

        root.add_widget(self.main_stack)
        return root

    # --- UI COMPONENT HELPERS ---
    def _build_bio_slide(self):
        self.bio_slide_container = MDBoxLayout(orientation='vertical', padding=[20, 10, 20, 10])
        self.bio_title = MDLabel(text="DATA", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=[1,1,1,1], size_hint_y=None, height="35dp")
        self.grid_anchor = MDBoxLayout(orientation='horizontal', size_hint=(None, None), width="460dp", height="175dp", pos_hint={'center_x': 0.5})
        self.bio_keys_label = MDLabel(text="", halign="right", font_style="H6", theme_text_color="Custom", text_color=[1,1,1,1], markup=True, size_hint_x=0.45)
        self.bio_values_label = MDLabel(text="", halign="left", font_style="H6", theme_text_color="Custom", text_color=[0,1,1,1], size_hint_x=0.55, padding=[10, 0])
        self.grid_anchor.add_widget(self.bio_keys_label)
        self.grid_anchor.add_widget(self.bio_values_label)
        self.bio_desc_label = MDLabel(text="", halign="center", theme_text_color="Custom", text_color=[1,1,1,1], italic=True, markup=True, font_style="H5", size_hint_y=None, height="100dp")
        self.bio_slide_container.add_widget(self.bio_title); self.bio_slide_container.add_widget(self.grid_anchor); self.bio_slide_container.add_widget(self.bio_desc_label)
        self.main_carousel.add_widget(self.bio_slide_container)

    def _build_learnset_slide(self):
        self.learn_slide_container = MDBoxLayout(orientation='vertical', padding=[10, 5, 10, 5])
        self.learn_title = MDLabel(text="LEARNSET", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=[1,1,1,1], size_hint_y=None, height="40dp")
        self.moves_scroll = ScrollView(size_hint=(1, 1), bar_width="4dp")
        self.scroll_content = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=10)
        self.moves_scroll.add_widget(self.scroll_content)
        self.learn_slide_container.add_widget(self.learn_title); self.learn_slide_container.add_widget(self.moves_scroll)
        self.main_carousel.add_widget(self.learn_slide_container)

    def _build_stats_slide(self):
        self.stats_page_wrapper = MDBoxLayout(orientation='vertical', padding=[20, 10, 20, 10], spacing=10)
        self.stats_title = MDLabel(text="BASE STATS", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=[1,1,1,1], size_hint_y=None, height="50dp")
        self.stats_columns_layout = MDBoxLayout(orientation='horizontal', size_hint=(None, 1), width="450dp", pos_hint={'center_x': 0.5})
        self.stats_names_label = MDLabel(text="", halign="right", font_style="H5", theme_text_color="Custom", text_color=[1,1,1,1], markup=True, size_hint_x=0.4)
        self.stats_bars_label = MDLabel(text="", halign="left", font_style="H5", theme_text_color="Custom", text_color=[0,1,1,1], markup=True, size_hint_x=0.6)
        self.stats_columns_layout.add_widget(self.stats_names_label); self.stats_columns_layout.add_widget(self.stats_bars_label)
        self.stats_page_wrapper.add_widget(self.stats_title); self.stats_page_wrapper.add_widget(self.stats_columns_layout)
        self.main_carousel.add_widget(self.stats_page_wrapper)

    def _build_loc_slide(self):
        self.loc_slide_container = MDBoxLayout(orientation='vertical', padding=[10, 5, 10, 5])
        self.loc_title = MDLabel(text="LOCATIONS", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=[1,1,1,1], size_hint_y=None, height="40dp")
        self.loc_scroll = ScrollView(size_hint=(1, 1), bar_width="4dp")
        self.loc_grid = MDGridLayout(cols=3, adaptive_height=True, padding=[20, 10], spacing=10)
        self.loc_scroll.add_widget(self.loc_grid)
        self.loc_slide_container.add_widget(self.loc_title); self.loc_slide_container.add_widget(self.loc_scroll)
        self.main_carousel.add_widget(self.loc_slide_container)

    def _build_nav_bar(self):
        self.nav_bar = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height="140dp", spacing=40, padding=[50, 10, 50, 10])
        # Buttons: Home, Gen Selector, Action (Scan)
        self.home_container = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.2, 0.2, 0.2, 1])
        self.home_btn = MDIconButton(icon="home", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=lambda x: self.change_screen('menu'))
        self.home_container.add_widget(self.home_btn)

        self.gen_container = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.15, 0.15, 0.15, 1])
        self.gen_btn = MDIconButton(icon="pokeball", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=self.open_gen_menu)
        self.gen_container.add_widget(self.gen_btn)

        self.action_container = MDCard(size_hint=(None, None), size=("100dp", "100dp"), radius=[50,], md_bg_color=[0.05, 0.38, 0.45, 1])
        self.action_btn = MDIconButton(icon="camera-iris", icon_size="64sp", theme_icon_color="Custom", icon_color=[1,1,1,1], pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=self.handle_action)
        self.action_container.add_widget(self.action_btn)

        self.nav_bar.add_widget(self.home_container); self.nav_bar.add_widget(self.gen_container); self.nav_bar.add_widget(self.action_container)

    # --- RUNTIME LOGIC ---
    def update_viewport(self, dt):
        """Updates the Live Viewport texture with the latest camera frame."""
        if self.sm.current == 'identifier' and not self.is_analyzing and self.picam2:
            frame = self.picam2.capture_array()
            if frame is not None:
                if not self.main_image.texture:
                    self.main_image.texture = Texture.create(size=(640, 480), colorfmt='rgb')
                self.main_image.texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                self.main_image.texture.flip_vertical()
                self.main_image.canvas.ask_update()

    def handle_action(self, *args):
        """Toggles between Live View and Analysis mode."""
        if time.time() - self.last_press_time < 1.5: return
        self.last_press_time = time.time()
        if self.is_analyzing: self.enter_live_state()
        else: self.take_photo()

    def take_photo(self, *args):
        """Captures a frame and initiates AI Analysis thread."""
        self.is_analyzing = True
        filename = f"test_images/scan_{int(time.time())}.jpg"
        if self.picam2: self.picam2.capture_file(filename)
        self.main_image.texture = None
        self.main_image.source = filename
        self.action_btn.icon = "refresh"
        self.action_btn.md_bg_color = [0.7, 0.1, 0.1, 1]
        threading.Thread(target=self.run_ai, args=(filename,)).start()

    def run_ai(self, filename):
        """Off-thread inference runner."""
        name, conf = self.ai_brain.predict(filename)
        Clock.schedule_once(lambda dt: self.show_result(name, conf), 0)
        time.sleep(0.1) # Prevent file lock before cleanup
        if os.path.exists(filename): os.remove(filename)

    def show_result(self, name, conf):
        """Updates UI slides with analyzed Pokémon data."""
        if conf > 0.40:
            info = self.ai_brain.get_info(name, self.current_gen)
            self.status_label.text = f"MATCH FOUND: {name.upper()}"
            self.scroll_content.clear_widgets()
            
            # BIO SLIDE
            self.bio_keys_label.text = "[b]SPECIES:\nTYPE:\nHT:\nWT:\nABILITY:\nH. ABILITY:[/b]"
            self.bio_values_label.text = f"{info.get('species','').upper()}\n{info.get('type','').capitalize()}\n{info.get('height','')}\n{info.get('weight','')}\n{info.get('ability','')}\n{info.get('hidden_ability','None')}"
            self.bio_desc_label.text = f"\"{info.get('description', 'No biometric lore available.')}\""
            
            # LEARNSET SLIDE
            self.add_move_section("BY LEVEL UP", info.get('learnset', []))
            self.add_move_section("BY TM / HM", info.get('tm_moves', []))

            # STATS SLIDE
            base_stats = info.get('base_stats', {})
            names_text, bars_text = "", ""
            stat_map = {"HP": "HP", "ATTACK": "ATK", "DEFENSE": "DEF", "SPECIAL-ATTACK": "SPA", "SPECIAL-DEFENSE": "SPD", "SPEED": "SPE"}
            for s_name, s_val in base_stats.items():
                short_name = stat_map.get(s_name.upper(), s_name[:3].upper())
                names_text += f"[b]{short_name}:[/b] {str(s_val).zfill(3)}\n"
                bar_count = max(1, int(s_val / 15)) 
                bars_text += f"{'█' * bar_count}\n"
            self.stats_names_label.text = names_text
            self.stats_bars_label.text = bars_text

            # LOCATIONS SLIDE
            self.loc_grid.clear_widgets()
            loc_data = info.get('locations', [])
            if not loc_data:
                self.loc_grid.add_widget(MDLabel(text="[i]Special Encounter Only[/i]", markup=True, halign="center", theme_text_color="Custom", text_color=[1,1,1,1]))
            else:
                for entry in loc_data:
                    self.loc_grid.add_widget(MDLabel(text=f"[b]{entry['area']}[/b]\n[size=14]{entry['method']} | {entry['chance']}[/size]", markup=True, theme_text_color="Custom", text_color=[1,1,1,1], halign="left", size_hint_y=None, height="60dp"))

            self.results_container.opacity = 1  
            self.main_carousel.index = 0       
            
            # SPRITE LOGIC
            sprite_path = f"assets/sprites/{name.lower()}.png"
            if os.path.exists(sprite_path):
                self.main_image.texture = None
                self.main_image.source = sprite_path
        else:
            self.status_label.text = "UNKNOWN POKÉMON"
            self.results_container.opacity = 0
        
    def add_move_section(self, title, moves_list):
        """Dynamically builds move headers and grids."""
        if not moves_list: return
        self.scroll_content.add_widget(MDLabel(text=f"{title}", halign="center", font_style="Button", theme_text_color="Custom", text_color=[1, 1, 1, 1], size_hint_y=None, height="40dp", markup=True))
        grid = MDGridLayout(cols=3, adaptive_height=True, spacing=[10, 5], padding=[5, 5])
        for item in moves_list:
            lvl = str(item.get('level', '??'))
            display_lvl = "TM" if lvl in ["0", "TM"] else f"L{lvl}"
            grid.add_widget(MDLabel(text=f"[b]{display_lvl}:[/b] {item.get('move', 'Unknown')}\n[size=12]({item.get('type', 'Normal')})[/size]", markup=True, theme_text_color="Custom", text_color=[1, 1, 1, 1], halign="center", size_hint_y=None, height="60dp"))
        self.scroll_content.add_widget(grid)

    def enter_live_state(self, *args):
        """Reset UI for live scanning."""
        self.is_analyzing = False
        self.status_label.text = "SCAN POKÉMON"
        self.results_container.opacity = 0
        self.main_image.source = ''
        self.main_image.texture = None
        self.action_btn.icon = "camera-iris"
        self.action_btn.md_bg_color = [0.05, 0.38, 0.45, 1]

    def open_gen_menu(self, instance):
        self.gen_menu.caller = instance
        self.gen_menu.open()

    def set_gen(self, gen_selection):
        """Sets active generation and updates UI theme."""
        self.current_gen = gen_selection
        self.gen_menu.dismiss()
        color_map = {"gen1": [0.05, 0.38, 0.45, 1], "gen2": [0.7, 0.5, 0.1, 1], "gen3": [0.6, 0.1, 0.1, 1]}
        self.id_banner.md_bg_color = color_map.get(gen_selection, [0.2, 0.2, 0.2, 1])
        self.status_label.text = f"ACTIVE: {gen_selection.replace('gen', 'GENERATION ')}"
        if self.is_analyzing: self.enter_live_state()

    def change_screen(self, name): self.sm.current = name

if __name__ == "__main__":
    PokedexApp().run()