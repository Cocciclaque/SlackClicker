import json
import os
import subprocess

# Path where you want to create the hidden folder (in a hidden location)


# Make sure the hidden folder exists
def create_hidden_folder(HIDDEN_FOLDER):
    try:
        # Check if folder already exists
        print(f"Target folder path: {HIDDEN_FOLDER}")  # Debug print
        if not os.path.exists(HIDDEN_FOLDER):
            os.makedirs(HIDDEN_FOLDER)
            print(f"Created folder at: {HIDDEN_FOLDER}")
        else:
            print(f"Folder already exists at: {HIDDEN_FOLDER}")
        
        # Make folder hidden by changing its attribute (Windows only)
        subprocess.run(['attrib', '+h', HIDDEN_FOLDER], check=True)
        print(f"Folder is now hidden: {HIDDEN_FOLDER}")

    except Exception as e:
        print(f"Error while creating hidden folder: {e}")

# Read the JSON file containing upgrade data
def load_upgrades_from_json(JSON_FILE):
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading the JSON file: {e}")
        return {"items": []}

# Save the updated JSON file (after purchase)
def save_upgrades_to_json(upgrades, JSON_FILE):
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(upgrades, file, indent=4)
            print("Upgrades saved successfully.")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

# Function to create files based on JSON data
def create_upgrade_files(upgrades, HIDDEN_FOLDER):
    try:
        for item in upgrades.get("items", []):
            file_name = f"{item['name']} {item['purchased']+1} - {item['price']}.txt"
            file_path = os.path.join(HIDDEN_FOLDER, file_name)

            # Creating the file with some lore text
            if item.get('locked', False) is False and (item.get('singletime', True) is True and item['purchased'] > 0) is False:
                with open(file_path, 'w') as file:
                    file.write(f"Name: {item['name']}\n")
                    file.write(f"Price: {item['price']}\n")
                    file.write(f"Lore: {item['lore']}\n")

                print(f"Created upgrade file: {file_path}")

    except Exception as e:
        print(f"Error creating upgrade files: {e}")

# Initialize the game: create folder, load json, create upgrade files
def initialize_game(JSON_FILE, HIDDEN_FOLDER):
    try:
        create_hidden_folder(HIDDEN_FOLDER)  # Ensure hidden folder is created
        upgrades = load_upgrades_from_json(JSON_FILE)  # Load upgrade data from JSON
        create_upgrade_files(upgrades, HIDDEN_FOLDER)  # Create the upgrade files based on the data
    except Exception as e:
        print(f"Error initializing game: {e}")

