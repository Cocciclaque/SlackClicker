import time
import keyboard
from soundapi import *
import subprocess
import valuesapi
import init
import os
import json
import update_status_file
from getFocusedWindow import is_active_window_process_name
from saveManager import SaveManager

notify_path = r"dependencies\PowerLook.exe"
JSON_FILE = r"dependencies\upgrades.json" # Name of the test JSON file
save_file = r"dependencies\save.json"
config_file = r"dependencies\config.json"

HIDDEN_FOLDER = os.path.join(os.getenv('APPDATA'), "File Updates", "Updates")
init.initialize_game(JSON_FILE, HIDDEN_FOLDER)

save = SaveManager(save_file)
config = SaveManager(config_file)

update_status_file.do_desktop_thing(JSON_FILE, config.get('folder_name'), config.get('file_name'))

upgrades = {}
upgrades["slackers"] = save.get("slackers", 0)
upgrades["speedboost"] = save.get("speedboost", 0)
upgrades["convertcolleagues"] = save.get("convertcolleagues", 0)
upgrades["powerfulSlacking"] = save.get("powerfulSlacking", 0)
upgrades["masterfulSlacking"] = save.get("masterfulSlacking", 0)
upgrades["slackonomics"] = save.get("slackonomics")
upgrades["slackverses"] = save.get("slackverses")
upgrades["powerpoint"] = save.get("powerpoint")
upgrades["excel"] = save.get("excel")
upgrades["onenote"] = save.get("onenote")
upgrades["infopath"] = save.get("infopath")
upgrades["sharepoint"] = save.get("sharepoint")
upgrades["infinity_gauntlet"] = save.get("infinity_gauntlet")
upgrades["paradoxes"] = save.get('paradoxes')
# Folder where upgrades are stored (hidden folder)
HIDDEN_FOLDER = os.path.join(os.getenv('APPDATA'), "File Updates", "Updates")

# Function to load upgrades from the JSON file
def load_upgrades():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading the JSON file: {e}")
        return {"items": []}

# Function to save upgrades to the JSON file
def save_upgrades(upgrades):
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(upgrades, file, indent=4)
    except Exception as e:
        print(f"Error saving the JSON file: {e}")

def savePurchase(item):
    purchased_count = item['purchased']
    if item['name'] == "Auto Slacker":
        save.set("slackers", purchased_count)
        upgrades["slackers"] = purchased_count
    elif item['name'] == "Slack Boost I":
        save.set("speedboost", purchased_count)
        upgrades["speedboost"] = purchased_count
    elif item['name'] == "Convert Colleague":
        save.set("convertcolleagues", purchased_count)
        upgrades["convertcolleagues"] = purchased_count
    elif item['name'] == "Powerful Slacking I":
        save.set('powerfulSlacking', purchased_count)
        upgrades["powerfulSlacking"] = purchased_count
    elif item['name'] == "Masterful Slacking I":
        save.set('masterfulSlacking', purchased_count)
        upgrades["masterfulSlacking"] = purchased_count
    elif item['name'] == "Slackonomics":
        save.set('slackonomics', purchased_count)
        upgrades['slackonomics'] = purchased_count
    elif item['name'] == "The Slackverse":
        save.set("slackverses", purchased_count)
        upgrades["slackverses"] = purchased_count
    elif item['name'] == "Microslack Powerpoint":
        save.set("powerpoint", purchased_count)
        upgrades["powerpoint"] = purchased_count
    elif item['name'] == "Microslack Excel":
        save.set("excel", purchased_count)
        upgrades["excel"] = purchased_count
    elif item['name'] == "Microslack OneNote":
        save.set("onenote", purchased_count)
        upgrades["onenote"] = purchased_count
    elif item['name'] == "Microslack InfoPath":
        save.set("infopath", purchased_count)
        upgrades["infopath"] = purchased_count
    elif item['name'] == "Microslack SharePoint":
        save.set("sharepoint", purchased_count)
        upgrades["sharepoint"] = purchased_count
    elif item['name'] == "Microslack Infinity Gauntlet":
        save.set("infinity_gauntlet", purchased_count)
        upgrades["infinity_gauntlet"] = purchased_count
    elif item['name'] == "Slacking Paradox":
        save.set("paradoxes", purchased_count)
        upgrades["paradoxes"] = purchased_count


# Function to recreate the upgrade file
def create_upgrade_file(item):
    try:
        file_name = f"{item['name']} {item['purchased']+1} - {item['price']}.txt"
        file_path = os.path.join(HIDDEN_FOLDER, file_name)

        # Ensure the directory exists
        os.makedirs(HIDDEN_FOLDER, exist_ok=True)

        with open(file_path, 'w') as file:
            file.write(f"Name: {item['name']}\n")
            file.write(f"Price: {item['price']}\n")
            file.write(f"Lore: {item['lore']}\n")
            file.write(f"Purchased: {item['purchased']} times\n")
        print(f"Recreated upgrade file: {file_path}")
    except Exception as e:
        print(f"Error creating the upgrade file: {e}")

# Function to handle the upgrade purchase (by deleting the file)
def handle_upgrade_purchase(item, score):
    if score >= item['price']:
        # Deduct the price from score
        score -= item['price']

        # Increase the purchased count
        item['purchased'] += 1

        # Update the price with the multiplier
        item['price'] = int(item['price'] * item['multiplier'])

        # If it's not a singletime upgrade, recreate the file
        if item.get('singletime', False) is False and (item['name'] == "Microslack Infinity Gauntlet" and item['purchased'] >= config.get('max_gauntlet_amount')) == False:
            print(item['name'] == "Microsoft Infinity Gauntlet")
            create_upgrade_file(item)
        print(f"Purchased {item['name']}!")
        save.set("score", score)
        savePurchase(item)
    else:
        create_upgrade_file(item)
        print(f"Not enough score to purchase {item['name']}.")
    
    return score  # Return the updated score

# Monitor the upgrades folder for file deletions
def monitor_upgrades(score):
    upgrades = load_upgrades()

    for item in upgrades.get("items", []):
        file_name = f"{item['name']} {item['purchased']+1} - {item['price']}.txt"
        file_path = os.path.join(HIDDEN_FOLDER, file_name)

        # If the file does not exist and it's not a singletime upgrade, trigger the purchase
        if not os.path.exists(file_path) and item.get('locked', False) is False:
            # If the file is deleted, try to buy the upgrade

            if item.get('singletime', True) is True and item['purchased'] > 0:
                pass
            else:
                print(f"File for {item['name']} deleted, attempting to purchase again...")
                score = handle_upgrade_purchase(item, score)
                
    save_upgrades(upgrades)
    return score  # Return the updated score

def do_math():
    pass

def do_locks():
    upgrade = load_upgrades()
    gauntlet = upgrade['items'][12]
    if gauntlet['purchased'] >= config.get('max_gauntlet_amount'):
        lock_upgrade_by_index(12)


def do_unlocks():
    upgrade = load_upgrades()
    powerful1 = upgrade['items'][3]
    masterful1 = upgrade['items'][4]
    slackonomics = upgrade['items'][5]
    gauntlet = [(upgrade['items'][7], 7)]
    gauntlet.append((upgrade['items'][8], 8))
    gauntlet.append((upgrade['items'][9], 9))
    gauntlet.append((upgrade['items'][10], 10))
    gauntlet.append((upgrade['items'][11], 11))
    gauntlet.append((upgrade['items'][12], 12))
    paradox = upgrade['items'][13]
    if upgrades['slackers'] >= config.get('required_slackers') and powerful1['locked'] == True:
        unlock_upgrade_by_index(3)
        create_upgrade_file(powerful1)
    if upgrades['slackers'] >= config.get('required_slackers') and masterful1['locked'] == True:
        unlock_upgrade_by_index(4)
        create_upgrade_file(masterful1)
    if upgrades['powerfulSlacking'] >= 1 and upgrades['masterfulSlacking'] >= 1 and slackonomics['locked'] == True:
        unlock_upgrade_by_index(5)
        create_upgrade_file(slackonomics)
    if upgrades['convertcolleagues'] >= config.get('required_colleagues') and gauntlet[0][0]['locked'] == True:
        for stone in gauntlet:
            unlock_upgrade_by_index(stone[1])
            create_upgrade_file(stone[0])
    if upgrades['excel'] >= 1 and upgrades['powerpoint'] >= 1 and upgrades['infopath'] >= 1 and upgrades['sharepoint'] >= 1 and upgrades['onenote'] >= 1 and gauntlet[5][0]['locked'] == True and gauntlet[5][0]['purchased'] < config.get('max_gauntlet_amount'):
        unlock_upgrade_by_index(12)
        create_upgrade_file(gauntlet[5][0])
    if upgrades['slackverses'] >= config.get('required_slackverses') and paradox['locked'] == True:
        unlock_upgrade_by_index(13)
        create_upgrade_file(paradox)
    
def trigger_slackers(score):
    return score + config.get('slacker_power')*upgrades['slackers']*1+(upgrades['powerfulSlacking']*config.get('powerfulSlacking_modifier'))

def trigger_colleagues(score):
    return score + config.get('colleague_power')*upgrades['convertcolleagues']

def trigger_slackverses(score):
    return score + config.get('slackverse_power')*upgrades['slackverses']

def trigger_microsoft_upgrades():
    powerBool = True if save.get('powerpoint') >= 1 and is_active_window_process_name('POWERPNT.EXE') else False
    excelBool = True if save.get('excel') >= 1 and is_active_window_process_name('EXCEL.EXE') else False
    onenoteBool = True if save.get('onenote') >= 1 and is_active_window_process_name('ApplicationFrameHost.exe') else False ##Idk Why but that's the name of the exe don't ask me
    infopathBool = True if save.get('infopath') >= 1 and is_active_window_process_name('infopath.exe') else False ##props to whoever gets this working
    sharepointBool = True if save.get('sharepoint') >= 1 and is_active_window_process_name("Microsoft.Sharepoint.exe") else False
    
    baseMult = config.get('base_microsoft_modifier') if powerBool or excelBool or onenoteBool or sharepointBool else 1
    infopathMult = config.get('infopath_microsoft_modifier') if infopathBool else 1

    return baseMult*infopathMult

def trigger_gauntlet(score):
    return score + config.get('gauntlet_power')*upgrades['infinity_gauntlet']*(upgrades['slackers']+upgrades['convertcolleagues']+upgrades['slackverses'])

def trigger_paradox(score):
    return score + config.get('paradox_power')*upgrades['paradoxes']

def unlock_upgrade_by_index(index):
    upgrades = load_upgrades()
    upgrades['items'][index]['locked'] = False
    save_upgrades(upgrades)

def lock_upgrade_by_index(index):
    upgrades = load_upgrades()
    upgrades['items'][index]['locked'] = True
    save_upgrades(upgrades)

def lock_all():
    upgrades = load_upgrades()
    upgrades['items'][3]['locked'] = True
    save_upgrades(upgrades)

def trigger_score(score, mult):
    new_score = score
    new_score = trigger_slackers(new_score)
    new_score = trigger_colleagues(new_score)
    new_score = trigger_slackverses(new_score)
    new_score = trigger_gauntlet(new_score)
    new_score = trigger_paradox(new_score)

    new_score = score + (new_score - score) * mult
    return round(new_score, 1)

def run_program_with_params(score, mult):
    valuesapi.show_notification("Slack Clicker", f"Your current score is {score}! Your SPS is {trigger_score(0, mult)} !")

def mainloop():
    score = save.get("score", 0)
    
    start_mult = save.get("speedboost", 0)*config.get('speedboost_modifier')
    slacking_mult = 0
    start = 0
    general_mult = 0

    running = True

    last_time = time.time()
    delay = config.get('timer_base_delay')  # Delay for the volume logic

    combo_z_was_pressed = False
    combo_m_was_pressed = False
    combo_s_was_pressed = False

    while running:
        current_time = time.time()
        elapsed_time = current_time - last_time

        # --- Combo: Ctrl + Alt + Shift + Z ---
        combo_z_now = (
            keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('alt') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('z')
        )
        if combo_z_now and not combo_z_was_pressed:
            run_program_with_params(score, general_mult)
            combo_z_was_pressed = True
        elif not combo_z_now:
            combo_z_was_pressed = False

        # --- Combo: Ctrl + Alt + Shift + M (add 0.2 to start) ---
        combo_m_now = (
            keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('alt') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('m')
        )
        if combo_m_now and not combo_m_was_pressed:
            start += config.get('base_manual_tick_value')
            score += config.get('base_slack_power')*(1+slacking_mult)
            combo_m_was_pressed = True
        elif not combo_m_now:
            combo_m_was_pressed = False

        combo_quit_now = (
            keyboard.is_pressed(config.get('closing_key'))
        )
        if combo_quit_now:
            running = False

        # --- Combo: Ctrl + Alt + Shift + S (open Task Manager) ---
        combo_s_now = (
            keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('alt') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('s')
        )
        if combo_s_now and not combo_s_was_pressed:
            subprocess.Popen("start taskmgr", shell=True)
            combo_s_was_pressed = True
        elif not combo_s_now:
            combo_s_was_pressed = False

        # --- Volume + score logic ---
        if elapsed_time >= delay:
            start += config.get('base_auto_tick_value')+start_mult
            if start >= 1:
                set_volume(0)
                start = 0
                score = trigger_score(score, general_mult)
                do_math()
                save.set("score", score)
                start_mult = save.get("speedboost", 0)*config.get('base_manual_tick_value')
                slacking_mult = save.get("masterfulSlacking")
                general_mult = 1+(save.get("slackonomics", 0)*config.get("slackonomics_modifier"))*trigger_microsoft_upgrades()
            set_volume(start)
            last_time = current_time

        do_unlocks()
        do_locks()
        # Check and handle upgrades if any file is deleted
        score = monitor_upgrades(score)

        time.sleep(0.01)  # Small delay to save CPU

# Start the main loop
mainloop()
