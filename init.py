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

def shorten_number(num):
    suffixes = [
        "", "k", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No",  # Thousand to Nonillion
        "Dc", "UDc", "DDc", "TDc", "QaDc", "QiDc", "SxDc", "SpDc", "OcDc", "NoDc",  # up to Novemdecillion
        "Vg"  # Vigintillion (you can go further if needed)
    ]

    if num < 1000:
        return str(num)

    magnitude = 0
    while abs(num) >= 1000 and magnitude < len(suffixes) - 1:
        num /= 1000.0
        magnitude += 1

    return f"{num:.1f}{suffixes[magnitude]}"


def make_file_path(item, file_name, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS):
    return_path = ""
    if item['locked'] == False:
        if item['singletime'] == False:
            return_path = os.path.join(HIDDEN_BUILDINGS, file_name)
        elif item['singletime'] == True:
            return_path = os.path.join(HIDDEN_UPGRADES, file_name)
    elif item['locked'] == True:
        return_path = os.path.join(HIDDEN_UNLOCKS, file_name)
    return return_path

def make_file_name(item):
    return_name = ""
    if item['locked'] == False:
        return_name = f"{item['name']} {item['purchased']+1} - {shorten_number(item['price'])}.txt"
    elif item['locked'] == True:
        return_name = f"{item['name'].split("-")[0]} - {item['requirements']}.txt "
    return return_name

# Function to recreate the upgrade file
def create_upgrade_files(item, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS):
    try:
        file_name = make_file_name(item)
        file_path = make_file_path(item, file_name, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS)

        # Ensure the directory exists
        os.makedirs(HIDDEN_FOLDER, exist_ok=True)
        os.makedirs(HIDDEN_BUILDINGS, exist_ok=True)
        os.makedirs(HIDDEN_UPGRADES, exist_ok=True)
        os.makedirs(HIDDEN_UNLOCKS, exist_ok=True)
        if(item['locked'] == False and (item['singletime'] == True and item['purchased'] >= 1 ) == False):
            with open(file_path, 'w') as file:
                file.write(f"Name: {item['name']}\n")
                file.write(f"Price: {shorten_number(item['price'])}\n")
                file.write(f"Lore: {item['lore']}\n")
                file.write(f"Purchased: {item['purchased']} times\n")
            print(f"Recreated upgrade file: {file_path}")
    except Exception as e:
        print(f"Error creating the upgrade file: {e}")

# Initialize the game: create folder, load json, create upgrade files
def initialize_game(JSON_FILE, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS):
    try:
        create_hidden_folder(HIDDEN_FOLDER)  # Ensure hidden folder is created
        upgrades = load_upgrades_from_json(JSON_FILE)  # Load upgrade data from JSON
        for item in upgrades.get("items", []):
            create_upgrade_files(item, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS)  # Create the upgrade files based on the data
    except Exception as e:
        print(f"Error initializing game: {e}")

