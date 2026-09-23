import platform
import os
import shutil
from pathlib import Path

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()


# Find install location

def find_profiles() -> List:
    system = platform.system()
    profiles = []

    if system == "Linux": # I use arch btw
        print("Linux")
        userdata = Path.home() / ".local/share/Steam/userdata"

        for user in userdata.iterdir():
            if user.is_dir():
                user = Path(user) / "632360/remote/UserProfiles"

                for profile in user.iterdir():
                    if profile.suffix == ".xml":
                        print(profile)

    return profiles


print(find_profiles())

# Show user profiles
# Choose to edit coins, or starter item
# Close