import requests
import json
import os

def fetch_ultimate_pokedex():
    pokedex = {}
    total_pokemon = 151  # Set to 151 for the full Kanto Dex
    
    print(f"--- Starting Ultimate Pokedex Sync (1-{total_pokemon}) ---")
    print("Note: This takes a few minutes as it fetches individual Move Types...")

    for i in range(1, total_pokemon + 1):
        try:
            # Main Pokemon Data
            r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}", timeout=10).json()
            name = r['name']
            
            # Species Data (for the flavor text/description)
            s_url = r['species']['url']
            s_data = requests.get(s_url, timeout=10).json()
            
            # Find the first English description
            description = "No biometric description available."
            for entry in s_data['flavor_text_entries']:
                if entry['language']['name'] == 'en':
                    description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    break

            # 1. BASE STATS
            stats_dict = {}
            for s in r['stats']:
                stat_name = s['stat']['name'].replace('-', ' ').upper()
                stats_dict[stat_name] = s['base_stat']

            # 2. LEARNSET (Level, Name, Type)
            learnset = []
            # To speed things up, we cache move types we've already looked up
            move_type_cache = {}

            for m in r['moves']:
                for detail in m['version_group_details']:
                    # Filter for Level-Up moves
                    if detail['move_learn_method']['name'] == 'level-up':
                        m_name_raw = m['move']['name']
                        
                        # Get Move Type (Check cache first to save API hits)
                        if m_name_raw not in move_type_cache:
                            m_info = requests.get(m['move']['url'], timeout=10).json()
                            move_type_cache[m_name_raw] = m_info['type']['name'].title()
                        
                        learnset.append({
                            "level": detail['level_learned_at'],
                            "move": m_name_raw.replace('-', ' ').title(),
                            "type": move_type_cache[m_name_raw]
                        })
                        break
            
            # Sort learnset by level
            learnset.sort(key=lambda x: x['level'])

            # 3. CONSOLIDATE DATA
            pokedex[name] = {
                "species": s_data['genera'][7]['genus'].upper() if len(s_data['genera']) > 7 else "UNKNOWN SPECIES",
                "type": "/".join([t['type']['name'].title() for t in r['types']]),
                "height": f"{r['height']/10} m",
                "weight": f"{r['weight']/10} kg",
                "ability": r['abilities'][0]['ability']['name'].replace('-', ' ').title(),
                "hidden_ability": r['abilities'][-1]['ability']['name'].replace('-', ' ').title() if len(r['abilities']) > 1 else "None",
                "description": description,
                "base_stats": stats_dict,
                "learnset": learnset
            }
            
            print(f"[OK] {i}/{total_pokemon}: {name.title()} synced.")

        except Exception as e:
            print(f"[ERROR] Failed on ID {i}: {e}")

    # Save to file
    os.makedirs('assets/data', exist_ok=True)
    with open('assets/data/pokedex_data.json', 'w') as f:
        json.dump(pokedex, f, indent=4)
    
    print("\n--- Sync Complete! ---")
    print(f"File saved to: {os.path.abspath('assets/data/pokedex_data.json')}")

if __name__ == "__main__":
    fetch_ultimate_pokedex()