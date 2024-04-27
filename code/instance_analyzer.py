import os
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    logs_location = r"C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs"
    # loop over files
    results = {}
    for file in sorted(os.listdir(logs_location)):
            file_path = os.path.join(logs_location, file)
            if os.path.isfile(file_path):
                if "TIMEOUT" in file or "GAMEOVER" in file: # check if file is a game result
                    instance_number = file.split('_')[2]  # Extract instance number from file name
                    if instance_number in results:
                        continue  # Skip this file if its instance has been processed (alphabetically; GAMEOVER has priority over TIMEOUT)
                    with open(file_path, "r") as f:
                        results[instance_number] = json.loads(f.read())
    
    # loop over results; we want to graph out results[key]["team_damage"]["allies"]
    team_damage_allies = []
    for key in results:
        team_damage_allies.append(results[key]["team_damage"]["allies"])
    
    # scatter plot of team_damage_allies with labels
    plt.xlabel("Instance Number")
    plt.ylabel("Team Damage Allies")
    plt.scatter(range(len(team_damage_allies)), team_damage_allies)
    for i, txt in enumerate(team_damage_allies):
        if txt > 0:
            plt.annotate(txt, (i, team_damage_allies[i]))
    plt.show()