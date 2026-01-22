import os
import re

print("Starting bleach_season_fix script")
folder = "/mnt/20Thdd"
path = "media/anime"
season = 1
lacking_pattern = r"S\d{2}"
correct_pattern = r"S\d{2}"
lowercase_lacking = r"s\d{2}"
lowercase_correct_pattern = r"s\d{2}"


def correct_or_not(filename, season):
    desired_label = f"S{str(season).zfill(2)}"

    if desired_label in filename:
        return True
    return False


def new_name_of_episode(file_name, season):
    for pattern, replacement in zip([lacking_pattern, lowercase_lacking], ["E", "e"]):
        try:
            match = re.search(pattern, file_name)
            current_epidose_label = match.group()
        except AttributeError:
            print("uppercase search failed, trying lowercase")
            continue
        desired_label = f"S{str(season).zfill(2)}"
        return file_name.replace(current_epidose_label, desired_label)

    raise ValueError(f"No matching pattern found in filename: {file_name}")


arc_template = "/Season {}"
for series in ["Bleach"]:
    for season in [17]:
        arc = series + arc_template.format(season)
        if not os.path.exists(os.path.join(folder, path, arc)):
            print(f"Path does not exist: {os.path.join(folder, path, arc)}")
            continue
        print(os.path.join(folder, path, arc))
        for file in os.listdir(os.path.join(folder, path, arc)):
            try:
                if correct_or_not(file, season):
                    continue
                old_path = os.path.join(folder, path, arc, file)
                new_name = new_name_of_episode(file, season)
                new_path = os.path.join(folder, path, arc, new_name)
                print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                raise e
