import time
import keyboard
from soundapi import *
import subprocess
import valuesapi
import init
import os
import shutil
import json
import changeWindowName
import update_status_file
from getFocusedWindow import is_active_window_process_name
from saveManager import SaveManager
from externalGameCloser import GameApp

notify_path = r"dependencies\PowerLook.exe"
JSON_FILE = r"dependencies\upgrades.json" # Name of the test JSON file
save_file = r"dependencies\save.json"
config_file = r"dependencies\config.json"

HIDDEN_FOLDER = os.path.join(os.getenv('APPDATA'), "File Updates", "Updates")
HIDDEN_BUILDINGS = os.path.join(HIDDEN_FOLDER, "Buildings")
HIDDEN_UPGRADES = os.path.join(HIDDEN_FOLDER, "Upgrades")
HIDDEN_UNLOCKS = os.path.join(HIDDEN_FOLDER, "Locked")
try:
    shutil.rmtree(HIDDEN_FOLDER)
except:
    pass
init.initialize_game(JSON_FILE, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS)

save = SaveManager(save_file)
config = SaveManager(config_file)

game_closer = GameApp(config.get('game_icon'))
game_closer.start()

update_status_file.do_desktop_thing(JSON_FILE, config.get('folder_name'), config.get('file_name'))

tutorial_state = save.get("tutorial_state", 0)

TUTORIAL_STEPS = [
    "Welcome to I'll Work After This! In this game, you win by slacking off. Yes, slacking, you dirty minded people.\n Press the Slack button (f7) to start slacking.\n You can view various game info by pressing F8, or by hovering on the window you are in the taskbar.\n Look at the window, it should tell you some info.\n (for example, look at the top of this window, there should be info updating)",
    "Now let’s automate things. Go to the Buildings folder and purchase 'Auto Slacker'.\n I very, very strongly recommend opening the said upgrade files as they contain info on what they do.\n You can copy/paste THIS in the little window when you do windowskey+r : appdata//Roaming//File Updates//updates",
    "Notice how the upgrade file appears? All upgrades live in your file system!\n To recap, f7 to slack, f8 to view slack, f9 to close the game. You can view and buy the upgrades in your files.",
    "I didn't finish the tutorial, I'll probably do the rest tomorrow... (the dev said that everyday for the last 3 weeks)"
]

def show_tutorial_message(step):
    message = TUTORIAL_STEPS[step]
    with open("TUTORIAL.txt", "w") as file:
        file.write(f"Step {step + 1}: {message}")
        file.close()


show_tutorial_message(save.get("tutorial_state"))
path = "TUTORIAL.txt"
subprocess.Popen(['notepad.exe', path])
def update_tutorial():
    current_step = save.get("tutorial_state", 0)
    
    if current_step == 0 and save.get("score", 0) >= 15:
        advance_tutorial()
    elif current_step == 1 and upgrades.get("slackers", 0) >= 1:
        advance_tutorial()
    elif current_step == 2 and upgrades.get("slackers", 0) >= 5:
        advance_tutorial()

def advance_tutorial():
    current_step = save.get("tutorial_state", 0)
    new_step = current_step + 1
    save.set("tutorial_state", new_step)

    if new_step < len(TUTORIAL_STEPS):
        subprocess.call("powershell.exe taskkill /F /IM notepad.exe", shell=True) 
        show_tutorial_message(new_step)
    else:
        subprocess.call("powershell.exe taskkill /F /IM notepad.exe", shell=True)  
        end_tutorial()

def end_tutorial():
    try:
        os.remove("TUTORIAL.txt")
    except:
        pass
    print("Tutorial complete. You’re free to Slack!")

upgrades = {}
upgrades["slackers"] = save.get("slackers", 0)
upgrades["coffee"] = save.get("coffee", 0)
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
upgrades['compound_disinterest'] = save.get('compound_disinterest')
upgrades['consultant'] = save.get('consultant')
upgrades['john'] = save.get('john')
upgrades['avoid'] = save.get('avoid')
upgrades['stop'] = save.get('stop')
upgrades["sacrificubicle"] = save.get("sacrificubicle", 0)
upgrades["breakhole"] = save.get("breakhole", 0)
upgrades["procrastinstein"] = save.get("procrastinstein", 0)
upgrades["astronot"] = save.get("astronot", 0)
upgrades["darkmatter"] = save.get("darkmatter", 0)
upgrades["countdowntimer"] = save.get("countdowntimer", 0)


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
    if item['name'] == "01 - Auto Slacker":
        save.set("slackers", purchased_count)
        upgrades["slackers"] = purchased_count
    if item['name'] == "02 - Coffee Break":
        save.set("coffee", purchased_count)
        upgrades["coffee"] = purchased_count
    elif item['name'] == "04 - Slack Boost I":
        save.set("speedboost", purchased_count)
        upgrades["speedboost"] = purchased_count
    elif item['name'] == "03 - Convert Colleague":
        save.set("convertcolleagues", purchased_count)
        upgrades["convertcolleagues"] = purchased_count
    elif item['name'] == "05 - Powerful Slacking I":
        save.set('powerfulSlacking', purchased_count)
        upgrades["powerfulSlacking"] = purchased_count
    elif item['name'] == "06 - Masterful Slacking I":
        save.set('masterfulSlacking', purchased_count)
        upgrades["masterfulSlacking"] = purchased_count
    elif item['name'] == "07 - Slackonomics":
        save.set('slackonomics', purchased_count)
        upgrades['slackonomics'] = purchased_count
    elif item['name'] == "08 - The Slackverse":
        save.set("slackverses", purchased_count)
        upgrades["slackverses"] = purchased_count
    elif item['name'] == "09 - Microslack Powerpoint":
        save.set("powerpoint", purchased_count)
        upgrades["powerpoint"] = purchased_count
    elif item['name'] == "10 - Microslack Excel":
        save.set("excel", purchased_count)
        upgrades["excel"] = purchased_count
    elif item['name'] == "11 - Microslack OneNote":
        save.set("onenote", purchased_count)
        upgrades["onenote"] = purchased_count
    elif item['name'] == "12 - Microslack InfoPath":
        save.set("infopath", purchased_count)
        upgrades["infopath"] = purchased_count
    elif item['name'] == "13 - Microslack SharePoint":
        save.set("sharepoint", purchased_count)
        upgrades["sharepoint"] = purchased_count
    elif item['name'] == "14 - Microslack Infinity Gauntlet":
        save.set("infinity_gauntlet", purchased_count)
        upgrades["infinity_gauntlet"] = purchased_count
    elif item['name'] == "15 - Slacking Paradox":
        save.set("paradoxes", purchased_count)
        upgrades["paradoxes"] = purchased_count
    elif item['name'] == "16 - Compound Disinterest":
        save.set("compound_disinterest", purchased_count)
        upgrades["compound_disinterest"] = purchased_count
    elif item['name'] == "17 - Slacker Consultant":
        save.set("consultant", purchased_count)
        upgrades["consultant"] = purchased_count
    elif item['name'] == "18 - John Slack":
        save.set("john", purchased_count)
        upgrades["john"] = purchased_count
    elif item['name'] == "19 - I wouldn't touch that if I were you":
        save.set("avoid", purchased_count)
        upgrades["avoid"] = purchased_count
    elif item['name'] == "20 - MAKE IT STOP":
        save.set("stop", purchased_count)
        upgrades["stop"] = purchased_count
    elif item['name'] == "21 - Sacrifi-cubicle":
        save.set("sacrificubicle", purchased_count)
        upgrades["sacrificubicle"] = purchased_count
    elif item['name'] == "22 - The Break Hole":
        save.set("breakhole", purchased_count)
        upgrades["breakhole"] = purchased_count
    elif item['name'] == "23 - Procrastinstein's Lab":
        save.set("procrastinstein", purchased_count)
        upgrades["procrastinstein"] = purchased_count
    elif item['name'] == "24 - Astro-not Program":
        save.set("astronot", purchased_count)
        upgrades["astronot"] = purchased_count
    elif item['name'] == "25 - Dark Matter of Inaction":
        save.set("darkmatter", purchased_count)
        upgrades["darkmatter"] = purchased_count
    elif item['name'] == "26 - The Final Countdown Timer":
        save.set("countdowntimer", purchased_count)
        upgrades["countdowntimer"] = purchased_count

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

def make_file_path(item, file_name):
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
def create_upgrade_file(item):
    try:
        file_name = make_file_name(item)
        file_path = make_file_path(item, file_name)
        # Ensure the directory exists
        os.makedirs(HIDDEN_FOLDER, exist_ok=True)
        os.makedirs(HIDDEN_BUILDINGS, exist_ok=True)
        os.makedirs(HIDDEN_UPGRADES, exist_ok=True)
        os.makedirs(HIDDEN_UNLOCKS, exist_ok=True)
        
        with open(file_path, 'w') as file:
            if(item['locked'] == False):
                file.write(f"Name: {item['name']}\n")
                file.write(f"Price: {shorten_number(item['price'])}\n")
                file.write(f"Lore: {item['lore']}\n")
                file.write(f"Purchased: {item['purchased']} times\n")
            else:
                file.write("You have not unlocked that upgrade yet..")
        # print(f"Recreated upgrade file: {file_path}")
    except Exception as e:
        print(f"Error creating the upgrade file: {e}")

# Function to handle the upgrade purchase (by deleting the file)
def handle_upgrade_purchase(item, score, times=1):
    for i in range(times):
        if score >= item['price']:
            score = round(score-item['price'],1)
            item['purchased'] += 1
            item['price'] = int(item['price'] * item['multiplier'])
            if item.get('singletime', False) is False and (item['name'] == "Microslack Infinity Gauntlet" and item['purchased'] >= config.get('max_gauntlet_amount')) == False and i == times-1:
                create_upgrade_file(item)
            save.set("score", score)
            savePurchase(item)
            print(f"Purchased {item['name']} (#{item['purchased']})!")
        else:
            print(f"Not enough score to purchase {item['name']}.")
            create_upgrade_file(item)
            break
    return score


# Monitor the upgrades folder for file deletions
def monitor_upgrades(score):
    upgrades = load_upgrades()
    shift_pressed = keyboard.is_pressed('shift')

    for item in upgrades.get("items", []):
        file_name = make_file_name(item)
        file_path = make_file_path(item, file_name)

        if not os.path.exists(file_path):
            if item.get('singletime', True) is True and item['purchased'] > 0:
                continue
            if item['locked'] == True:
                create_upgrade_file(item)
            else:
                print(f"File for {item['name']} deleted, attempting to purchase...")
                purchase_amount = 5 if shift_pressed else 1
                score = handle_upgrade_purchase(item, score, times=purchase_amount)
                poke_folder_for_refresh(HIDDEN_BUILDINGS)
                poke_folder_for_refresh(HIDDEN_BUILDINGS)
                poke_folder_for_refresh(HIDDEN_BUILDINGS)
            

    save_upgrades(upgrades)
    return score


def do_math():
    pass

def do_locks():
    upgrade = load_upgrades()
    gauntlet = upgrade['items'][12]
    if gauntlet['purchased'] >= config.get('max_gauntlet_amount'):
        lock_upgrade_by_index(12)

def poke_folder_for_refresh(path):
    dummy_path = os.path.join(path, "~refresh.tmp")
    with open(dummy_path, 'w') as f:
        f.write("refresh")
    time.sleep(0.01)
    os.remove(dummy_path)

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
    compound = upgrade['items'][14]
    consultant = upgrade['items'][16] ##15 is coffee break
    john = upgrade['items'][17]
    avoid = upgrade['items'][18]
    stop = upgrade['items'][19]
    sacrificubicle = upgrade['items'][20]
    breakhole = upgrade['items'][21]
    procrastinstein = upgrade['items'][22]
    astronot = upgrade['items'][23]
    darkmatter = upgrade['items'][24]
    countdowntimer = upgrade['items'][25]

    old_upgrade = upgrade.copy()

    if upgrades['slackers'] >= config.get('required_slackers') and powerful1['locked'] == True:
        unlock_upgrade_by_index(3)
        create_upgrade_file(load_upgrades()['items'][3])
    if upgrades['slackers'] >= config.get('required_slackers') and masterful1['locked'] == True:
        unlock_upgrade_by_index(4)
        create_upgrade_file(load_upgrades()['items'][4])
        print('Masterful is now unlocked', masterful1['locked'])
    if upgrades['powerfulSlacking'] >= 1 and upgrades['masterfulSlacking'] >= 1 and slackonomics['locked'] == True:
        unlock_upgrade_by_index(5)
        create_upgrade_file(load_upgrades()['items'][5])
    if upgrades['convertcolleagues'] >= config.get('required_colleagues') and gauntlet[0][0]['locked'] == True:
        for i in range(len(gauntlet)):
            if(gauntlet[i] != (upgrade['items'][12], 12)):
                unlock_upgrade_by_index(gauntlet[i][1])
                create_upgrade_file(load_upgrades()['items'][gauntlet[i][1]])
    if upgrades['excel'] >= 1 and upgrades['powerpoint'] >= 1 and upgrades['infopath'] >= 1 and upgrades['sharepoint'] >= 1 and upgrades['onenote'] >= 1 and gauntlet[5][0]['locked'] == True and gauntlet[5][0]['purchased'] < config.get('max_gauntlet_amount'):
        unlock_upgrade_by_index(12)
        create_upgrade_file(load_upgrades()['items'][12])
    if upgrades['slackverses'] >= config.get('required_slackverses') and paradox['locked'] == True:
        unlock_upgrade_by_index(13)
        create_upgrade_file(load_upgrades()['items'][13])
    if upgrades['paradoxes'] >= config.get('required_paradox_compound') and upgrades['infinity_gauntlet'] >= config.get('required_gauntlets') and compound['locked'] == True:
        unlock_upgrade_by_index(14)
        create_upgrade_file(load_upgrades()['items'][14])
    if save.get('score') >= config.get('required_score_consultant') and consultant['locked'] == True:
        unlock_upgrade_by_index(16)
        create_upgrade_file(load_upgrades()['items'][15])
    if save.get('score') >= config.get('required_score_john') and john['locked'] == True:
        unlock_upgrade_by_index(17)
        create_upgrade_file(load_upgrades()['items'][17])
    if save.get('john') >= config.get('required_john_avoid') and avoid['locked'] == True:
        unlock_upgrade_by_index(18)
        create_upgrade_file(load_upgrades()['items'][18])
    if save.get('avoid') >= 1 and stop['locked'] == True:
        unlock_upgrade_by_index(19)
        create_upgrade_file(load_upgrades()['items'][19])
    if upgrades['convertcolleagues'] >= config.get('required_colleagues_cubicle') and sacrificubicle['locked'] == True:
        unlock_upgrade_by_index(20)
        create_upgrade_file(load_upgrades()['items'][20])
    if upgrades['sacrificubicle'] >= config.get('required_sacrificubicle') and breakhole['locked'] == True:
        unlock_upgrade_by_index(21)
        create_upgrade_file(load_upgrades()['items'][21])
    if upgrades['breakhole'] >= config.get('required_breakhole') and procrastinstein['locked'] == True:
        unlock_upgrade_by_index(22)
        create_upgrade_file(load_upgrades()['items'][22])
    if upgrades['procrastinstein'] >= config.get('required_procrastinstein') and astronot['locked'] == True:
        unlock_upgrade_by_index(23)
        create_upgrade_file(load_upgrades()['items'][23])
    if upgrades['astronot'] >= config.get('required_astronot') and darkmatter['locked'] == True:
        unlock_upgrade_by_index(24)
        create_upgrade_file(load_upgrades()['items'][24])
    if upgrades['darkmatter'] >= config.get('required_darkmatter') and countdowntimer['locked'] == True:
        unlock_upgrade_by_index(25)
        create_upgrade_file(load_upgrades()['items'][25])

        

def do_coffee():
    return 1 if save.get('coffee') == 0 else (config.get('coffee_power')*save.get('coffee'))

def trigger_slackers(score):
    return score + (config.get('slacker_power')*do_coffee())*upgrades['slackers']*(1+(upgrades['powerfulSlacking']*config.get('powerfulSlacking_modifier')))*consultant_mult()

def masterful_mult():
    return 1 + (save.get("masterfulSlacking")*config.get('masterfulSlacking_modifier'))

def trigger_colleagues(score):
    return score + config.get('colleague_power')*upgrades['convertcolleagues']*consultant_mult()*masterful_mult()

def trigger_slackverses(score):
    return score + config.get('slackverse_power')*upgrades['slackverses']*consultant_mult()

def trigger_microsoft_upgrades():
    powerBool = True if save.get('powerpoint') >= 1 and is_active_window_process_name('POWERPNT.EXE') else False
    excelBool = True if save.get('excel') >= 1 and is_active_window_process_name('EXCEL.EXE') else False
    onenoteBool = True if save.get('onenote') >= 1 and is_active_window_process_name('ApplicationFrameHost.exe') else False ##Idk Why but that's the name of the exe don't ask me
    infopathBool = True if save.get('infopath') >= 1 and is_active_window_process_name('infopath.exe') else False ##props to whoever gets this working
    sharepointBool = True if save.get('sharepoint') >= 1 and is_active_window_process_name("Microsoft.Sharepoint.exe") else False
    
    micro_list = [save.get('powerpoint') >= 1, save.get('excel') >= 1, save.get('onenote') >= 1, save.get('infopath') >= 1, save.get('sharepoint') >= 1]
    additive_mult = 1
    for boolean in micro_list:
        if boolean == True:
            additive_mult = additive_mult*config.get('base_microsoft_constant_modifier')
    additive_mult = additive_mult if additive_mult != 1 else 1

    vscodeBool = True if save.get('powerpoint') >= 1 and is_active_window_process_name('code.exe') else False

    baseMult = config.get('base_microsoft_modifier') if powerBool or excelBool or onenoteBool or sharepointBool or vscodeBool else 1
    infopathMult = config.get('infopath_microsoft_modifier') if infopathBool else 1

    return (baseMult*infopathMult) + additive_mult

def trigger_gauntlet(score):
    return score + config.get('gauntlet_power')*upgrades['infinity_gauntlet']*(upgrades['slackers']+upgrades['convertcolleagues']+upgrades['slackverses'])*consultant_mult()

def trigger_paradox(score):
    return score + config.get('paradox_power')*upgrades['paradoxes']*consultant_mult()

def trigger_consultants(score):
    return score + config.get('consultant_power')*upgrades['consultant']

def consultant_mult():
    return 1+(config.get('consultant_efficiency_modifier')*upgrades['consultant'])

def unlock_upgrade_by_index(index):
    shutil.rmtree(HIDDEN_UNLOCKS)
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
    # print('----------------------')
    # print(trigger_slackers(0))
    # print(trigger_colleagues(0))
    # print(trigger_slackverses(0))
    # print(trigger_gauntlet(0))
    # print(trigger_paradox(0))
    # print(trigger_consultants(0))
    # print("mult = " + str(mult))
    new_score = trigger_slackers(new_score)
    new_score = trigger_colleagues(new_score)
    new_score = trigger_slackverses(new_score)
    new_score = trigger_gauntlet(new_score)
    new_score = trigger_paradox(new_score)
    new_score = trigger_consultants(new_score)
    new_score = score + (new_score - score) * mult
    return round(new_score, 1)

def getCompoundMult():
    return 1+((trigger_slackers(0)*config.get('compound_disinterest_modifier'))*save.get('compound_disinterest'))

def getJohnMult(timer):
    return 1+config.get('john_multiplier') if timer > time.time() else 1 

def run_program_with_params(score, mult):
    valuesapi.show_notification("Slack Clicker", f"Your current score is {shorten_number(score)}! Your SPS is {shorten_number(trigger_score(0, mult))} !")

def constructSoundBar(start, score, general_mult):
    bar = "["+"-"*int(round(start*10))+" "*int(round((1-start)*10))+"]"
    return bar + "  -  " + shorten_number(score) + " Slack  -  " + shorten_number(trigger_score(0, general_mult)) + " SPS"

def mainloop():
    score = save.get("score", 0)
    
    start_mult = 0
    slacking_mult = 0
    start = 0
    general_mult = 0

    john_timer = time.time()
    john_effect = time.time()

    running = True
    try:
        for _ in range(100):        
            update_status_file.do_desktop_thing(JSON_FILE, config.get('folder_name'), config.get('file_name'))
    except:
        pass
    last_time = time.time()
    delay = config.get('timer_base_delay')  # Delay for the volume logic

    combo_z_was_pressed = False
    combo_m_was_pressed = False
    combo_s_was_pressed = False
    combo_scrolllock_was_pressed = False

    while running:
        current_time = time.time()
        elapsed_time = current_time - last_time
        # --- Combo: Ctrl + Alt + Shift + Z ---
        combo_z_now = (
            keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('alt') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('z')
        ) or keyboard.is_pressed(config.get('alias_key_show'))

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
        ) or keyboard.is_pressed(config.get('alias_key_slack'))
        if combo_m_now and not combo_m_was_pressed:
            start += config.get('base_manual_tick_value')*save.get('speedboost')
            score += config.get('base_slack_power')*do_coffee()*(1+slacking_mult)
            combo_m_was_pressed = True
        elif not combo_m_now:
            combo_m_was_pressed = False

        combo_quit_now = (
            keyboard.is_pressed(config.get('closing_key')) or
            game_closer.opened is False
        )
        if combo_quit_now:
            running = False

        john_key = keyboard.is_pressed('scroll_lock')
        if john_key and not combo_scrolllock_was_pressed:
            combo_scrolllock_was_pressed = True
            if john_key and time.time() >= john_timer and upgrades['john'] >= 1:
                john_timer = config.get('john_cooldown') + time.time()
                john_effect = config.get('john_duration') + time.time()
            elif john_key and time.time() < john_timer and upgrades['john'] >= 1:
                valuesapi.show_notification("Slack Clicker", f"This ability is on cooldown ({round(john_timer-time.time(), 0)} seconds remaining...) ! Not like you're in a rush, anyways...")
            elif john_key and upgrades['john'] == 0:
                valuesapi.show_notification("Slack Clicker", f"You have not bought this ability yet ! Do more nothing !")
        elif not john_key:
            combo_scrolllock_was_pressed = False
        # --- Volume + score logic ---
        if elapsed_time >= delay:
            start += config.get('base_auto_tick_value')+start_mult
            if start >= 1:
                start = 0
                score = trigger_score(score, general_mult)
                do_math()
                save.set("score", score)
                start_mult = 0
                slacking_mult = 0
                general_mult = 1+(save.get("slackonomics", 0)*config.get("slackonomics_modifier"))*trigger_microsoft_upgrades()*getCompoundMult()*getJohnMult(john_effect)
                config.load()
            update_tutorial()
            last_time = current_time
            if save.get("avoid") == 1:
                if save.get('stop') == 1:
                    if config.get('do_soundbar') == 1:
                        set_volume(start)
                elif save.get('stop') == 0:
                    set_volume(start)
                
        changeWindowName.set_window_name(constructSoundBar(start, score, general_mult))

        do_unlocks()
        do_locks()
        score = monitor_upgrades(score)
        # Check and handle upgrades if any file is deleted
        update_status_file.do_desktop_thing(JSON_FILE, config.get('folder_name'), config.get('file_name'))

        time.sleep(0.01)  # Small delay to save CPU

# Start the main loop
mainloop()
