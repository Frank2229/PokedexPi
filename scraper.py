"""
PokedexPi Deep Scraper
Utility script to pull cross-generational data from PokeAPI.
Generates a nested JSON structure organized by Generation ID.
"""

import requests
import json
import time

# --- 1. CONFIGURATION ---
# Defines the scope of each generation and which game versions to prioritize for data.
GEN_CONFIG = {
    "gen1": {
        "max_id": 151, 
        "version_group": "red-blue", 
        "loc_versions": ['red', 'blue', 'yellow']
    },
    "gen2": {
        "max_id": 251, 
        "version_group": "gold-silver", 
        "loc_versions": ['gold', 'silver', 'crystal']
    },
    "gen3": {
        "max_id": 386, 
        "version_group": "ruby-sapphire", 
        "loc_versions": ['ruby', 'sapphire', 'emerald']
    }
}

def get_multi_gen_dex():
    """
    Performs a deep scrape of PokeAPI. 
    Checks every Pokemon up to Gen 3 against every generation's data
    to ensure movepools and descriptions are accurate to that era.
    """
    all_data = {"gen1": {}, "gen2": {}, "gen3": {}}
    
    # Session object for better performance over many requests
    session = requests.Session()
    
    for gen_id, config in GEN_CONFIG.items():
        print(f"\n{'='*40}")
        print(f" STARTING DEEP SCRAPE: {gen_id.upper()}")
        print(f"{'='*40}")
        
        # Scrape from ID 1 up to the limit of the current generation
        for i in range(1, config["max_id"] + 1):
            try:
                # Fetch Base Pokemon Data
                p_url = f"https://pokeapi.co/api/v2/pokemon/{i}"
                p_response = session.get(p_url)
                
                if p_response.status_code != 200: 
                    continue
                
                p_data = p_response.json()
                name = p_data['name']
                
                # --- A. GENERATION VALIDATION ---
                # Check if this Pokemon exists in the code for the targeted version group
                has_gen_data = False
                for m in p_data['moves']:
                    for detail in m['version_group_details']:
                        if detail['version_group']['name'] == config["version_group"]:
                            has_gen_data = True
                            break
                    if has_gen_data: break
                
                if not has_gen_data:
                    continue # Skip if the Pokemon didn't exist or wasn't in this Gen

                print(f"[{gen_id.upper()}] Adding {name.capitalize()}...")

                # Fetch Species Data (Flavor Text and Genus)
                s_url = f"https://pokeapi.co/api/v2/pokemon-species/{i}"
                s_data = session.get(s_url).json()

                # --- B. BASE STATS ---
                stats = {s['stat']['name'].upper(): s['base_stat'] for s in p_data['stats']}

                # --- C. MOVESET (Level-up & TMs) ---
                learnset = []
                tm_moves = []
                for m_entry in p_data['moves']:
                    for detail in m_entry['version_group_details']:
                        if detail['version_group']['name'] == config["version_group"]:
                            m_name = m_entry['move']['name'].replace('-', ' ').title()
                            method = detail['move_learn_method']['name']
                            
                            move_info = {"move": m_name, "type": "Normal"}
                            
                            if method == 'level-up':
                                move_info["level"] = detail['level_learned_at']
                                learnset.append(move_info)
                            elif method == 'machine':
                                move_info["level"] = "TM"
                                tm_moves.append(move_info)
                            break

                # --- D. CATCH LOCATIONS ---
                loc_url = p_data['location_area_encounters']
                loc_data = session.get(loc_url).json()
                locations = []
                for entry in loc_data:
                    for vd in entry['version_details']:
                        if vd['version']['name'] in config["loc_versions"]:
                            locations.append({
                                "area": entry['location_area']['name'].replace('-', ' ').title(),
                                "method": vd['encounter_details'][0]['method']['name'].title(),
                                "chance": f"{vd['encounter_details'][0]['chance']}%"
                            })
                            break

                # --- E. POKEDEX DESCRIPTION ---
                # Use the primary version of that generation for the description
                target_v = config["loc_versions"][0]
                desc = "No biometric lore found."
                for entry in s_data['flavor_text_entries']:
                    if entry['language']['name'] == 'en' and entry['version']['name'] == target_v:
                        # Clean up control characters and newlines
                        desc = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                        break

                # --- F. DATA COMPILATION ---
                all_data[gen_id][name] = {
                    "species": s_data['genera'][7]['genus'].upper(),
                    "type": "/".join([t['type']['name'].capitalize() for t in p_data['types']]),
                    "height": f"{p_data['height']/10} m",
                    "weight": f"{p_data['weight']/10} kg",
                    "ability": p_data['abilities'][0]['ability']['name'].replace('-', ' ').title(),
                    "description": desc,
                    "base_stats": stats,
                    "learnset": sorted(learnset, key=lambda x: x['level'] if isinstance(x['level'], int) else 999),
                    "tm_moves": tm_moves,
                    "locations": locations[:10]
                }

                # Slight delay to respect PokeAPI rate limits
                time.sleep(0.05)

            except Exception as e:
                print(f"FAILED {i} in {gen_id}: {e}")
                continue

    # --- 3. FINAL FILE EXPORT ---
    output_file = 'assets/data/pokedex_data.json'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=4)
        
    print(f"\n{'*'*50}")
    print(f" SUCCESS: Deep-Scrape complete!")
    print(f" File saved to: {output_file}")
    print(f"{'*'*50}")

if __name__ == "__main__":
    import os
    get_multi_gen_dex()