import platform
import os
import shutil
from pathlib import Path

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()


# Find install location

def find_profiles():
    system = platform.system()
    profiles = []

    if system == "Linux": # I use arch btw
        print("Linux")
        userdata = Path.home() / ".local/share/Steam/userdata"

    if system == "Windows":
        print("Windows")
        userdata = Path("C:\\Program Files (x86)\\Steam\\userdata")

    
    for user in userdata.iterdir():
        if user.is_dir():
            user = Path(user) / "632360/remote/UserProfiles"
            print("File not Found")

            try:
                for profile in user.iterdir():
                    if profile.suffix == ".xml":
                        profiles.append(profile)
            except FileNotFoundError:
                pass

                        

    return profiles

print(Path.home())

print(find_profiles())

# Show user profiles
# Choose to edit coins, or starter item
# Close