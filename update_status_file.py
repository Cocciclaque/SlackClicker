import os
import json
from pathlib import Path
from datetime import datetime

def do_desktop_thing(JSON_FILE, folder_name, file_name):
    desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    folder_name = folder_name  # Looks spooky & low-profile
    folder_path:Path = desktop / folder_name
    built = True
    if os.path.isdir(folder_path) == False:
        try:
            folder_path.mkdir(exist_ok=True)
        except:
            built = False
    # Status file
    if built:
        status_file = folder_path / file_name

        # Simulated inventory (you can replace this with a real read)
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        upgrades = data["items"]
        log_lines = [f"# Watchdog Status Log — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
        log_lines.append(">>> Acquired SlackTech Modules:")

        # Go through upgrades
        for upgrade in upgrades:
            if upgrade["purchased"] > 0:
                status = f"[x{upgrade['purchased']}]" if not upgrade["singletime"] else "[✓]"
                name = upgrade["name"]
                lore_line = upgrade["lore"].split("\n")[0]  # Just the first line
                log_lines.append(f" • {status} {name} — {lore_line}")

        # Add footer flavor
        log_lines.append("\n---")
        log_lines.append("system.alert: Composure degraded. Slack potential: HIGH.")
        log_lines.append("end.of.file // code=0x1A")

        # Write to file
        with open(status_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
