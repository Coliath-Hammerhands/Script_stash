import os
import re
import secrets
import string
import time

folder = "/mnt/20Thdd"
path = "media/kids"
season = 2
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


def modify_episode_format(file_name):
    # Split the file name into parts
    parts = file_name.split(".")
    name, ext = os.path.splitext(file_name)
    pattern = r"(\w+)\.(S|E)\d+(?:[E\d]+)*\.([A-Z][\w-]+\.\d+p\.NF\.WEB-DL\.DDP5\.1\.x264-LAZY)"
    # Search for a match in the file name
    match = re.search(pattern, file_name)

    if match:
        # Extract the modified episode numbers from the match
        s_number = int(match.group(2).strip("S")) if "S" in match.group(2) else None
        e_number = int(match.group(3)) if "E" not in match.group(3) else match.group(3).replace("E", "")

        # Modify the episode numbers based on their values
        if s_number is not None and e_number >= 37:
            new_e_number = str(e_number + 1)
            modified_file_name = file_name.replace(f"{match.group(2)}{match.group(3)}", f"{match.group(1)}.E{e_number}E{new_e_number}")
        elif s_number is not None and e_number < 37:
            modified_file_name = file_name
        else:
            return file_name
    # # Check if the episode number is less than 37
    # if int(parts[2].split("E")[1]) < 37:
    #     return "pass", file_name

    # Modify the episode numbers
    modified_parts = parts[:]
    if len(modified_parts) >= 4 and len(modified_parts[3].split("E")) == 2:
        s_number, e_number = int(modified_parts[3].split("E")[0]), int(modified_parts[3].split("E")[1])
        modified_s_number, modified_e_number = str(s_number + 1), str(e_number + 1)
    else:
        random_string = generate_random_string() + ext
        return random_string, file_name

    # Replace the original episode numbers with the modified ones
    modified_file_name = ".".join([modified_parts[0], modified_parts[1], modified_s_number, modified_e_number, modified_parts[-3]])

    print(f"Modified file name: {modified_file_name}")
    random_string = generate_random_string() + ext
    return random_string, modified_file_name


def adjust_episodes(filename):
    # Pattern to find 'S' followed by season digits, then one or more 'E' followed by episode digits
    # Example matches: "S02E37", "S02E38E39"
    pattern = r"(S\d+)((?:E\d+)+)"
    name, ext = os.path.splitext(filename)
    random_string = generate_random_string() + ext

    def replacement(match):
        season_part = match.group(1)  # e.g., "S02"
        episodes_part = match.group(2)  # e.g., "E37" or "E38E39"

        # Extract all episode numbers as integers
        nums = [int(n) for n in re.findall(r"\d+", episodes_part)]

        # Rule 1: If any episode is less than 37, leave it alone
        if any(n < 37 for n in nums):
            # return "pass"
            return match.group(0)

        # Rule 2: If the episode is exactly 37, make it E37E38
        if nums == [37]:
            return f"{season_part}E37E38"

        # Rule 3: If episodes are > 37, add 1 to each
        if all(n > 37 for n in nums) or (len(nums) > 1 and 37 in nums):
            # Reconstruct the string by incrementing each number found
            new_episodes = re.sub(r"\d+", lambda m: f"{int(m.group()) + 1:02d}", episodes_part)
            return f"{season_part}{new_episodes}"

        return match.group(0)

    return random_string, re.sub(pattern, replacement, filename)


arc_template = "/Season {}"
for series in ["PJ Masks"]:
    for season in [2]:
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
                temp_name, new_name = adjust_episodes(file)
                if new_name == file:
                    continue
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
