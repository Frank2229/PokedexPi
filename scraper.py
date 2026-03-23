import requests
import json
import time

# 1. CONFIGURATION: Version Mapping
# We define the "Latest ID" for each gen so the scraper knows how far to look back.
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
    all_data = {"gen1": {}, "gen2": {}, "gen3": {}}
    
    for gen_id, config in GEN_CONFIG.items():
        print(f"\n--- STARTING DEEP SCRAPE: {gen_id.upper()} ---")
        
        for i in range(1, config["max_id"] + 1):
            try:
                p_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
                
                # FIXED LINE BELOW: status_code instead of status_status
                if p_response.status_code != 200: 
                    continue
                
                p_data = p_response.json()
                name = p_data['name']
                
                # --- A. VERIFY DATA EXISTS FOR THIS GEN ---
                # We check if the Pokemon actually has move data for this version group.
                # If not, it means they weren't in that game's code.
                has_gen_data = False
                for m in p_data['moves']:
                    for detail in m['version_group_details']:
                        if detail['version_group']['name'] == config["version_group"]:
                            has_gen_data = True
                            break
                    if has_gen_data: break
                
                if not has_gen_data:
                    continue # Skip if not in this generation

                print(f"[{gen_id.upper()}] Adding {name.capitalize()}...")
                
                s_data = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{i}").json()

                # --- B. BASE STATS ---
                stats = {s['stat']['name'].upper(): s['base_stat'] for s in p_data['stats']}

                # --- C. MOVES (Gen-Specific) ---
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

                # --- D. CATCH LOCATIONS (Gen-Specific) ---
                loc_url = p_data['location_area_encounters']
                loc_data = requests.get(loc_url).json()
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

                # --- E. DESCRIPTION (Gen-Specific) ---
                target_v = config["loc_versions"][0]
                desc = "No biometric lore found."
                for entry in s_data['flavor_text_entries']:
                    if entry['language']['name'] == 'en' and entry['version']['name'] == target_v:
                        desc = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                        break

                # --- F. COMPILE ---
                all_data[gen_id][name] = {
                    "species": s_data['genera'][7]['genus'].upper(),
                    "type": "/".join([t['type']['name'].capitalize() for t in p_data['types']]),
                    "height": f"{p_data['height']/10} m",
                    "weight": f"{p_data['weight']/10} kg",
                    "ability": p_data['abilities'][0]['ability']['name'].replace('-', ' ').title(),
                    "description": desc,
                    "base_stats": stats,
                    "learnset": sorted(learnset, key=lambda x: x['level']),
                    "tm_moves": tm_moves,
                    "locations": locations[:10]
                }

            except Exception as e:
                print(f"Error on {i} in {gen_id}: {e}")
                continue

    # 3. SAVE NESTED JSON
    with open('pokedex_data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("\nSUCCESS: Deep-Scrape complete. Every Pokemon now has data for every Gen they appeared in!")

if __name__ == "__main__":
    get_multi_gen_dex()