import os
import re

folder = "/mnt/20Thdd"
path = "media/kids"
season = 1


def correct_or_not(filename):
    if re.search(correct_pattern, filename):
        return True
    return False


def new_name_of_episode(file_name):
    match = re.search(lacking_pattern, file_name)
    current_epidose_label = match.group()
    current_ep_number = re.search(r"E\d{2}", file_name).group()
    int_ep_number = int(current_ep_number.replace("E", ""))
    upper_ep_number = int(int_ep_number * 2)
    lower = upper_ep_number - 1
    return file_name.replace(current_epidose_label, f"S{str(season).zfill(2)}E{str(lower).zfill(2)}E{str(upper_ep_number).zfill(2)}")


for season in range(1, 5):
    arc = f"Spidey and His Amazing Friends/Season {season}"
    lacking_pattern = r"S\d{2}E\d{2}"
    correct_pattern = r"S\d{2}E\d{2}E\d{2}"

    for file in os.listdir(os.path.join(folder, path, arc)):
        if correct_or_not(file):
            continue
        old_path = os.path.join(folder, path, arc, file)
        new_name = new_name_of_episode(file)
        new_path = os.path.join(folder, path, arc, new_name)
        print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
        os.rename(old_path, new_path)
