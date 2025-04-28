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
import Overlay
notify_path = r"dependencies\PowerLook.exe"
JSON_FILE = r"dependencies\upgrades.json" # Name of the test JSON file
save_file = r"dependencies\save.json"
config_file = r"dependencies\config.json"

localization_folder = r"localization"
localization = {}

ov = Overlay.Overlay()
ov.start()

for file in os.listdir(localization_folder):
    localization[file.split(".")[0]] = file

HIDDEN_FOLDER = os.path.join(os.getenv('APPDATA'), "File Updates", "Updates")
HIDDEN_BUILDINGS = os.path.join(HIDDEN_FOLDER, "Buildings")
HIDDEN_UPGRADES = os.path.join(HIDDEN_FOLDER, "Upgrades")
HIDDEN_UNLOCKS = os.path.join(HIDDEN_FOLDER, "Locked")
try:
    shutil.rmtree(HIDDEN_FOLDER)
except:
    pass


save = SaveManager(save_file)
config = SaveManager(config_file)

game_closer = GameApp(config.get('game_icon'), localization, save.get('lang'))
game_closer.start()

update_status_file.do_desktop_thing(JSON_FILE, config.get('folder_name'), config.get('file_name'))




# openTabs.open("thefuturelinktomyvid")

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
upgrades['compound_disinterest'] = save.get('compound_disinterest')
upgrades['consultant'] = save.get('consultant')
upgrades['john'] = save.get('john')
upgrades['avoid'] = save.get('avoid')
upgrades['stop'] = save.get('stop')
upgrades["email"] = save.get("email", 0)
upgrades["overdose"] = save.get("overdose", 0)
upgrades["pro"] = save.get("pro", 0)
upgrades["efort"] = save.get("efort", 0)
upgrades["music"] = save.get("music", 0)
upgrades["jojo?"] = save.get("jojo?", 0)

#-----------Tier Upgrades-----
upgrades["coffee"] = save.get("coffee", 0)
upgrades["should_come"] = save.get("should_come", 0)
upgrades["moreuniverse"] = save.get("moreuniverse", 0)
upgrades["philosophers"] = save.get("philosophers", 0)
upgrades["wisdom"] = save.get("wisdom", 0)
upgrades["overclocking"] = save.get("overclocking", 0)
upgrades["crisis"] = save.get("crisis", 0)
upgrades["upset"] = save.get("upset", 0)
upgrades["unemployement"] = save.get("unemployement", 0)
upgrades["grow"] = save.get("grow", 0)
upgrades["reference"] = save.get("reference", 0)

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
    if lang.get(str(item['id'])) == lang.get('0'):
        save.set("slackers", purchased_count)
        upgrades["slackers"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('2'):
        save.set("speedboost", purchased_count)
        upgrades["speedboost"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('1'):
        save.set("convertcolleagues", purchased_count)
        upgrades["convertcolleagues"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('3'):
        save.set('powerfulSlacking', purchased_count)
        upgrades["powerfulSlacking"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('4'):
        save.set('masterfulSlacking', purchased_count)
        upgrades["masterfulSlacking"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('5'):
        save.set('slackonomics', purchased_count)
        upgrades['slackonomics'] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('6'):
        save.set("slackverses", purchased_count)
        upgrades["slackverses"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('7'):
        save.set("powerpoint", purchased_count)
        upgrades["powerpoint"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('8'):
        save.set("excel", purchased_count)
        upgrades["excel"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('9'):
        save.set("onenote", purchased_count)
        upgrades["onenote"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('10'):
        save.set("infopath", purchased_count)
        upgrades["infopath"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('11'):
        save.set("sharepoint", purchased_count)
        upgrades["sharepoint"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('12'):
        save.set("infinity_gauntlet", purchased_count)
        upgrades["infinity_gauntlet"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('13'):
        save.set("paradoxes", purchased_count)
        upgrades["paradoxes"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('14'):
        save.set("compound_disinterest", purchased_count)
        upgrades["compound_disinterest"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('16'):
        save.set("consultant", purchased_count)
        upgrades["consultant"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('17'):
        save.set("john", purchased_count)
        upgrades["john"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('18'):
        save.set("avoid", purchased_count)
        upgrades["avoid"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('19'):
        save.set("stop", purchased_count)
        upgrades["stop"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('20'):
        save.set("email", purchased_count)
        upgrades["email"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('21'):
        save.set("overdose", purchased_count)
        upgrades["overdose"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('22'):
        save.set("pro", purchased_count)
        upgrades["pro"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('23'):
        save.set("efort", purchased_count)
        upgrades["efort"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('24'):
        save.set("music", purchased_count)
        upgrades["music"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('25'):
        save.set("jojo?", purchased_count)
        upgrades["jojo?"] = purchased_count
##------------------------------------Buildings Multis------------------------------------------
    if lang.get(str(item['id'])) == lang.get('15'):
        save.set("coffee", purchased_count)
        upgrades["coffee"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('26'):
        save.set("should_come", purchased_count)
        upgrades["should_come"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('27'):
        save.set("moreuniverse", purchased_count)
        upgrades["moreuniverse"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('28'):
        save.set("philosophers", purchased_count)
        upgrades["philosophers"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('29'):
        save.set("wisdom", purchased_count)
        upgrades["wisdom"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('30'):
        save.set("overclocking", purchased_count)
        upgrades["overclocking"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('31'):
        save.set("crisis", purchased_count)
        upgrades["crisis"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('32'):
        save.set("upset", purchased_count)
        upgrades["upset"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('33'):
        save.set("unemployement", purchased_count)
        upgrades["unemployement"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('34'):
        save.set("grow", purchased_count)
        upgrades["grow"] = purchased_count
    elif lang.get(str(item['id'])) == lang.get('35'):
        save.set("reference", purchased_count)
        upgrades["reference"] = purchased_count

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
        return_name = f"{lang.get(str(item['id']))} {item['purchased']+1} - {shorten_number(item['price'])}.txt"
    elif item['locked'] == True:
        return_name = f"{lang.get(str(item['id'])).split("-")[0]} - {lang.get(("requirements_"+str(item['id'])))}.txt "
    return return_name

# Function to recreate the upgrade file
def create_upgrade_file(item):
    global lang
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
                file.write(f"{lang.get('name')}: {lang.get(str(item['id']))}\n")
                file.write(f"{lang.get('price')}: {shorten_number(item['price'])}\n")
                file.write(f"{lang.get('lore')}: {lang.get(("lore_"+str(item['id'])))}\n")
                file.write(f"{lang.get('purchased_0')}: {item['purchased']} {lang.get('purchased_1')}\n")
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
            if item.get('singletime', False) is False and (lang.get(str(item['id'])) == "Microslack Infinity Gauntlet" and item['purchased'] >= config.get('max_gauntlet_amount')) == False and i == times-1:
                create_upgrade_file(item)
            save.set("score", score)
            savePurchase(item)
            print(f"Purchased {lang.get(str(item['id']))} (#{item['purchased']})!")
        else:
            print(f"Not enough score to purchase {lang.get(str(item['id']))}.")
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
                print(f"File for {lang.get(str(item['id']))} deleted, attempting to purchase...")
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
    email = upgrade['items'][20]
    overdose = upgrade['items'][21]
    pro = upgrade['items'][22]
    efort = upgrade['items'][23]
    music = upgrade['items'][24]
    jojo = upgrade['items'][25]

    ##-----------------------------UPGRADES---------------------------------------

    coll_tier = upgrade['items'][26]
    universe_tier = upgrade['items'][27]
    paradox_tier = upgrade['items'][28]
    consultant_tier = upgrade['items'][29]
    bot_tier = upgrade['items'][30]
    overdose_tier = upgrade['items'][31]
    upset_tier = upgrade['items'][32]
    efort_tier = upgrade['items'][33]
    music_tier = upgrade['items'][34]
    jojo_tier = upgrade['items'][35]

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
        create_upgrade_file(load_upgrades()['items'][16])
    if save.get('score') >= config.get('required_score_john') and john['locked'] == True:
        unlock_upgrade_by_index(17)
        create_upgrade_file(load_upgrades()['items'][17])
    if save.get('john') >= config.get('required_john_avoid') and avoid['locked'] == True:
        unlock_upgrade_by_index(18)
        create_upgrade_file(load_upgrades()['items'][18])
    if save.get('avoid') >= 1 and stop['locked'] == True:
        unlock_upgrade_by_index(19)
        create_upgrade_file(load_upgrades()['items'][19])
    if save.get('score') >= config.get('required_money_new_tier_buildings') and email['locked'] == True:
        unlock_upgrade_by_index(20)
        create_upgrade_file(load_upgrades()['items'][20])
        unlock_upgrade_by_index(21)
        create_upgrade_file(load_upgrades()['items'][21])
        unlock_upgrade_by_index(22)
        create_upgrade_file(load_upgrades()['items'][22])
        unlock_upgrade_by_index(23)
        create_upgrade_file(load_upgrades()['items'][23])
        unlock_upgrade_by_index(24)
        create_upgrade_file(load_upgrades()['items'][24])
        unlock_upgrade_by_index(25)
        create_upgrade_file(load_upgrades()['items'][25])

#-------------------------------------TIER UPGRADES---------------------------------

    if upgrades['convertcolleagues'] >= config.get('generic_required_tier_upgrade') and coll_tier['locked'] == True:
        unlock_upgrade_by_index(26)
        create_upgrade_file(load_upgrades()['items'][26])
    if upgrades['slackverses'] >= config.get('generic_required_tier_upgrade') and universe_tier['locked'] == True:
        unlock_upgrade_by_index(27)
        create_upgrade_file(load_upgrades()['items'][27])
    if upgrades['paradoxes'] >= config.get('generic_required_tier_upgrade') and paradox_tier['locked'] == True:
        unlock_upgrade_by_index(28)
        create_upgrade_file(load_upgrades()['items'][28])
    if upgrades['consultant'] >= config.get('generic_required_tier_upgrade') and consultant_tier['locked'] == True:
        unlock_upgrade_by_index(29)
        create_upgrade_file(load_upgrades()['items'][29])
    if upgrades['email'] >= config.get('generic_required_tier_upgrade') and bot_tier['locked'] == True:
        unlock_upgrade_by_index(30)
        create_upgrade_file(load_upgrades()['items'][30])
    if upgrades['overdose'] >= config.get('generic_required_tier_upgrade') and overdose_tier['locked'] == True:
        unlock_upgrade_by_index(31)
        create_upgrade_file(load_upgrades()['items'][31])
    if upgrades['pro'] >= config.get('generic_required_tier_upgrade') and upset_tier['locked'] == True:
        unlock_upgrade_by_index(32)
        create_upgrade_file(load_upgrades()['items'][32])
    if upgrades['efort'] >= config.get('generic_required_tier_upgrade') and efort_tier['locked'] == True:
        unlock_upgrade_by_index(33)
        create_upgrade_file(load_upgrades()['items'][33])
    if upgrades['music'] >= config.get('generic_required_tier_upgrade') and music_tier['locked'] == True:
        unlock_upgrade_by_index(34)
        create_upgrade_file(load_upgrades()['items'][34])
    if upgrades['jojo?'] >= config.get('generic_required_tier_upgrade') and jojo_tier['locked'] == True:
        unlock_upgrade_by_index(35)
        create_upgrade_file(load_upgrades()['items'][35])


        

def do_coffee():
    return 2**save.get('coffee')

def trigger_slackers(score):
    return score + (config.get('slacker_power')*do_coffee())*upgrades['slackers']*(1+(upgrades['powerfulSlacking']*config.get('powerfulSlacking_modifier')))*consultant_mult()

def masterful_mult():
    return 1 + (save.get("masterfulSlacking")*config.get('masterfulSlacking_modifier'))

def trigger_colleagues(score):
    return score + config.get('colleague_power')*upgrades['convertcolleagues']*consultant_mult()*masterful_mult()*colleagues_mult()

def colleagues_mult():
    return 2**save.get('should_come')

def trigger_slackverses(score):
    return score + config.get('slackverse_power')*upgrades['slackverses']*consultant_mult()*slackverses_mult()

def slackverses_mult():
    return 2**save.get('moreuniverse')

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
    return score + config.get('paradox_power')*upgrades['paradoxes']*consultant_mult()*paradox_mult()

def paradox_mult():
    return 2**save.get('philosophers')

def trigger_consultants(score):
    return score + config.get('consultant_power')*upgrades['consultant']*consultant_mult()*consultants_mult()

def consultants_mult():
    return 2**save.get('wisdom')

def consultant_mult():
    return 1+(config.get('consultant_efficiency_modifier')*upgrades['consultant'])

def trigger_email(score):
    return score + config.get('email_power')*upgrades['email']*email_mult()*consultant_mult()

def email_mult():
    return 2**save.get('overclocking')

def trigger_overdose(score):
    return score + config.get('overdose_power')*upgrades['overdose']*overdose_mult()*consultant_mult()

def overdose_mult():
    return 2**save.get('crisis')
    
def trigger_pro(score):
    return score + config.get('pro_power')*upgrades['pro']*pro_mult()*consultant_mult()

def pro_mult():
    return 2**save.get('upset')
    
def trigger_efort(score):
    return score + config.get('efort_power')*upgrades['efort']*efort_mult()*consultant_mult()

def efort_mult():
    return 2**save.get('unemployement')

def trigger_music(score):
    return score + config.get('music_power')*upgrades['music']*music_mult()*consultant_mult()

def music_mult():
    return 2**save.get('grow')
    
def trigger_jojo(score):
    return score + config.get('jojo_power')*upgrades['jojo?']*jojo_mult()*consultant_mult()

def jojo_mult():
    return 2**save.get('reference')
    
def unlock_upgrade_by_index(index):
    shutil.rmtree(HIDDEN_UNLOCKS)
    upgrades = load_upgrades()
    upgrades['items'][index]['locked'] = False
    valuesapi.show_notification("I'll Work After This", f"You unlocked {upgrades['items'][index]['name']} !")
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
    new_score = trigger_email(new_score)
    new_score = trigger_overdose(new_score)
    new_score = trigger_pro(new_score)
    new_score = trigger_efort(new_score)
    new_score = trigger_music(new_score)
    new_score = trigger_jojo(new_score)
    new_score = score + (new_score - score) * mult
    return round(new_score, 1)

def getCompoundMult():
    return 1+((trigger_slackers(0)*config.get('compound_disinterest_modifier'))*save.get('compound_disinterest'))

def getJohnMult(timer):
    return 1+config.get('john_multiplier') if timer > time.time() else 1 

def run_program_with_params(score, mult):
    global lang
    valuesapi.show_notification("I'll Work After This", f"{lang.get('current_score')} {shorten_number(score)}{lang.get('current_SPS')} {shorten_number(trigger_score(0, mult))}{lang.get('end_notification')}")

def constructSoundBar(start, score, general_mult):
    global lamg
    bar = "["+"-"*int(round(start*10))+" "*int(round((1-start)*10))+"]"
    return bar + "  -  " + shorten_number(score) + f" {lang.get('slack')}  -  " + shorten_number(trigger_score(0, general_mult)) + " SPS"

def new_language():
    shutil.rmtree(HIDDEN_FOLDER)
    init.initialize_game(JSON_FILE, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS, lang)

def mainloop():
    global lang
    score = save.get("score", 0)
    
    init.initialize_game(JSON_FILE, HIDDEN_FOLDER, HIDDEN_BUILDINGS, HIDDEN_UPGRADES, HIDDEN_UNLOCKS, lang)
    do_unlocks()

    time.sleep(2)

    visibility = game_closer.get_visibility()
    current_lang = game_closer.get_localization()
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
        visibility = game_closer.get_visibility()
        lang.save_file = os.path.join(localization_folder, game_closer.get_localization()+".json")
        lang.load()
        save.set('lang', game_closer.get_localization())
        if current_lang != save.get('lang'):
            new_language()
        current_lang = game_closer.get_localization()
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
                valuesapi.show_notification("I'll Work After This", f"{lang.get('ability_cooldown_0')}{round(john_timer-time.time(), 0)} {lang.get('ability_cooldown_1')}")
            elif john_key and upgrades['john'] == 0:
                valuesapi.show_notification("I'll Work After This", f"{lang.get('ability_not_unlocked')}")
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
lang = SaveManager(os.path.join(localization_folder, game_closer.get_localization()+".json"))
mainloop()
