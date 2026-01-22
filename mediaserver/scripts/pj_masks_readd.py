import os
import re
import secrets
import string
import time

folder = "/mnt/20Thdd"
path = "media/kids"
season = 1
lacking_pattern = r"S\d{2}E\d{2}"
correct_pattern = r"S\d{2}E\d{2}E\d{2}"
lowercase_lacking = r"s\d{2}e\d{2}"
lowercase_correct_pattern = r"s\d{2}e\d{2}e\d{2}"


def correct_or_not(filename):
    if re.search(correct_pattern, filename):
        return True
    elif re.search(lowercase_correct_pattern, filename):
        return True
    return False


def generate_random_string(length=40):
    """Generate a random string of specified length."""
    alphabet = string.ascii_letters + string.digits  # + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def new_name_of_episode_temp(file_name):
    """add by two"""
    for pattern, replacement in zip([correct_pattern, lowercase_correct_pattern], ["E", "e"]):
        try:
            match = re.search(pattern, file_name)
            current_epidose_label = match.group()
            current_ep_number = re.findall(r"E\d{2}", file_name)[1]
            int_ep_number = int(current_ep_number.replace(replacement, ""))
        except AttributeError:
            print("uppercase search failed, trying lowercase")
            continue
        upper_ep_number = int(int_ep_number + 2)
        lower = upper_ep_number - 1
        final_name = file_name.replace(current_epidose_label, f"S{str(season).zfill(2)}E{str(lower).zfill(2)}E{str(upper_ep_number).zfill(2)}")
    try:
        name, ext = os.path.splitext(file_name)
        file_name = name.upper() + ext
        match = re.search(correct_pattern, file_name)
        current_epidose_label = match.group()
        current_ep_number = re.searfindallch(r"E\d{2}", file_name)[1]
        int_ep_number = int(current_ep_number.replace("E", ""))
        upper_ep_number = int(int_ep_number + 2)
        lower = upper_ep_number - 1
        final_name = file_name.replace(current_epidose_label, f"S{str(season).zfill(2)}E{str(lower).zfill(2)}E{str(upper_ep_number).zfill(2)}")
    except AttributeError:
        print("forced uppercase search failed, giving up")
    try:
        random_string = generate_random_string() + ext
        return random_string, final_name
    except UnboundLocalError:
        raise ValueError(f"No matching pattern found in filename: {file_name}")


arc_template = "/Season {}"
for series in ["PJ Masks"]:
    for season in [4]:
        temp_names = {}
        old_to_temp = {}
        arc = series + arc_template.format(season)
        if not os.path.exists(os.path.join(folder, path, arc)):
            continue

        for file in os.listdir(os.path.join(folder, path, arc)):
            try:
                if not correct_or_not(file):
                    continue
                old_path = os.path.join(folder, path, arc, file)
                temp_name, new_name = new_name_of_episode_temp(file)
                old_to_temp[file] = temp_name
                temp_names[temp_name] = new_name
                new_path = os.path.join(folder, path, arc, temp_name)
                print(f"Renaming:\n{file}\nto\n{new_name}\n")
                # os.rename(old_path, new_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                raise e
        assert len(old_to_temp) == len(temp_names), "Mismatch in temporary names mapping."

        for old_name, temp_name in old_to_temp.items():
            os.rename(os.path.join(folder, path, arc, old_name), os.path.join(folder, path, arc, temp_name))
        time.sleep(30)  # wait to ensure all renames are processed
        for temp_name, final_name in temp_names.items():
            os.rename(os.path.join(folder, path, arc, temp_name), os.path.join(folder, path, arc, final_name))
