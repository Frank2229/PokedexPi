PokedexPi: AI-Powered Handheld Encyclopedia

PokedexPi is a physical, handheld device built on the Raspberry Pi 5 that uses Computer Vision and Deep Learning to identify Pokémon in real-time. Inspired by the original anime and games, it features a multi-generational database, live camera analysis, and a high-tech modular UI.

Features

    AI Species Identification: Uses a custom-trained ResNet-18 Deep Learning model to recognize 149 Pokémon species via the Raspberry Pi Camera Module 3.

    Multi-Gen Support: Seamlessly switch between Gen 1 (Kanto), Gen 2 (Johto), and Gen 3 (Hoenn).

    Era-Accurate Data: Deep-scraped data ensures that movepools, locations, and Pokédex descriptions change dynamically based on the selected generation.

    Modular Interface: A central "Hub" menu providing access to the Identifier, IV Calculator, and Regional Maps.

    Hardware Optimized: Custom UI built with KivyMD, optimized for the 720x1280 capacitive touch display.

Hardware Requirements

    Computer: Raspberry Pi 5 (4GB or 8GB recommended).

    Camera: Raspberry Pi Camera Module 3 (IMX708).

    Display: 7" LDI Touchscreen (720x1280 resolution).

    OS: Raspberry Pi OS (64-bit) with Wayland/X11 support.

Installation & Setup
1. Clone the Repository
Bash

git clone https://github.com/yourusername/PokedexPi.git
cd PokedexPi

2. Environment Setup

I recommend using a virtual environment to manage dependencies:
Bash

python -m venv pokedex_env
source pokedex_env/bin/activate
pip install -r requirements.txt

3. Data Scraping

To generate the latest cross-generational database, run the deep scraper:
Bash

python scraper.py

4. Running the App

Bash

python main.py

How It Works

The AI Brain

The core of the identification system is a Convolutional Neural Network (CNN). Images captured by the camera are pre-processed (resized to 224x224 and normalized) before being passed through the ResNet-18 layers. The model outputs a confidence score; if the score exceeds 40%, the Pokedex retrieves the corresponding biometric data from the local JSON "Lore" file.

The Deep Scraper

The scraper.py utility interfaces with PokeAPI. Unlike standard scrapers, it performs a "Deep Search"—iterating through every generation for every Pokémon to capture how their data evolved over the GameBoy Advance and Color eras.

Project Structure

    main.py: The primary KivyMD application and UI logic.

    scraper.py: Advanced data extraction utility for PokeAPI.

    assets/:

        data/: Contains the master pokedex_data.json.

        sprites/: PNG sprites for UI display.

        icons/: UI elements like the Pokeball and Logo.

    models/: Pre-trained PyTorch model weights (.pth).

Contributing

Contributions are welcome! Whether it's adding Gen 4 support, improving the IV Calculator, or optimizing the model for the Pi's NPU, feel free to fork and submit a PR.

License

This project is for educational and fan purposes only. Pokémon and all related names are trademarks of Nintendo, Creatures Inc., and GAME FREAK.
