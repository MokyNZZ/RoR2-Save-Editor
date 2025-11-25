import xml.etree.ElementTree as ET
import string
import datetime
from pathlib import Path
import shutil
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_console()

Drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

FoundFiles = []
FoundNames = []
FoundParseError = []

for Drive in Drives:
    BasePath = Path(Drive) / "Program Files (x86)" / "Steam" / "userdata"

    if not BasePath.exists():
        continue

    for UserFolder in BasePath.iterdir():
        if not UserFolder.is_dir() or not UserFolder.name.isdigit():
            continue

        TargetPath = UserFolder / "632360" / "remote" / "UserProfiles"
        if not TargetPath.exists():
            continue

        for XmlFile in TargetPath.glob("*.xml"):
            FoundFiles.append(XmlFile)

if not FoundFiles:
    print("No profiles found.")
    quit()
else:  # Create Backups
    BACKUP_DIR = Path("./Backups")
    # Create timestamped folder
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-4]
    backup_path = BACKUP_DIR / time_str
    backup_path.mkdir(parents=True, exist_ok=True)

    # Copy files into the new backup folder
    for file in FoundFiles:
        shutil.copy2(file, backup_path)

    # --- Keep only last 10 backups ---
    # Get all backup folders
    backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()])

    # If more than 10, delete the oldest
    while len(backups) > 10:
        old = backups.pop(0)  # remove oldest
        shutil.rmtree(old)

for File in FoundFiles:
    try:
        Tree = ET.parse(File)
        root = Tree.getroot()

        for NameTag in root.iter("name"):
            NameText = NameTag.text.strip() if NameTag.text else ""
            if NameText:
                FoundNames.append((NameText, File))

    except ET.ParseError:
        FoundParseError.append(File)
    except Exception as e:
        print(f"Error reading {File}: {e}")

def ProfileSelector():
    while True:
        clear_console()
        if FoundParseError:
            print("Failed to parse:")
            for f in FoundParseError:
                print(f" - {f}")
            print("\n")

        print("Select a profile:\n")
        for i, (name, file_path) in enumerate(FoundNames, start=1):
            print(f"{i}. {name} (from {file_path})")

        choice = input("\nEnter the number of the profile you want to edit: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(FoundNames):
                selected_name, selected_file = FoundNames[choice - 1]
                break
            else:
                print("Invalid selection.")
        else:
            print("Invalid input.")

    clear_console()

    while True:
        print(f"You selected: {selected_name} from {selected_file}")

        try:
            tree = ET.parse(selected_file)
            root = tree.getroot()
        except ET.ParseError:
            print("Selected file cannot be parsed.")
            return
        action = input("\nWhat do you want to do?\n"
              "1. Go back to the profile selector\n"
              "2. Edit lunar coins\n"
              "3. Edit artifact of rebirth item\n\n").strip()

        if action.isdigit():
            action = int(action)

            if action == 1:
                ProfileSelector()
                return

            elif action == 2:  # Edit Lunar Coins
                clear_console()
                for coin_tag in root.iter("coins"):
                    coin_text = coin_tag.text.strip() if coin_tag.text else "0"
                    print(f"{selected_name} currently has {coin_text} lunar coins")
                new_value = input("Enter new lunar coins value: ").strip()
                if new_value.isdigit():
                    for coin_tag in root.iter("coins"):
                        coin_tag.text = str(int(new_value))
                    tree.write(selected_file, encoding="utf-8", xml_declaration=True)
                    print(f"Lunar coins updated to {new_value}!")
                else:
                    print("Invalid input. Must be a number.")

            elif action == 3:  # Edit Artifact of Rebirth
                clear_console()
                for rebirth_tag in root.iter("RebirthItem"):
                    current = rebirth_tag.text.strip() if rebirth_tag.text else "(empty)"
                    print(f"Current RebirthItem: {current}")
                new_item = input("Enter new RebirthItem value: ").strip()
                if new_item:
                    new_item = f"ItemIndex.{new_item}"
                    for rebirth_tag in root.iter("RebirthItem"):
                        rebirth_tag.text = new_item
                    tree.write(selected_file, encoding="utf-8", xml_declaration=True)
                    print(f"RebirthItem updated to {new_item}!")

            else:
                print("Invalid selection.")
        else:
            print("Invalid input.")

        clear_console()

ProfileSelector()
