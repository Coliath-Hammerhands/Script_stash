import os
import re
import time

folder = "/mnt/20Thdd"
path = "media/anime"
season = 1
arc = f"Gintama/Season {season}"
pattern = r"\[.*?\]|[^\[\]]+"
# chapter_chunk=2
episode_number = 1


def parse_episode(filename):
    ext = os.path.splitext(filename)[1]
    name = filename.replace(ext, "").strip()
    matches = re.findall(pattern, name)
    cleaned_matches = [item.replace("[", "").replace("]", "").strip() for item in matches if item.strip()]
    # print(cleaned_matches)
    assert cleaned_matches[0] == "CBT", f"It was {cleaned_matches[0]}"
    return f"{cleaned_matches[episode_number]}{ext}"


def pull_ep_number(episode_str):
    ext = os.path.splitext(episode_str)[1]
    name = episode_str.replace(ext, "").strip()
    return name.split(" ")[0], int(name.split(" ")[1]), ext


def correct_numbering(name, number_str, ext, min_number):
    number = int(number_str) + 1 - min_number
    return name + " " + str(number).zfill(2) + ext


for file in os.listdir(os.path.join(folder, path, arc)):
    if "[CBT]" not in file:
        continue
    old_path = os.path.join(folder, path, arc, file)
    new_name = parse_episode(file)
    new_path = os.path.join(folder, path, arc, new_name)
    print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
    os.rename(old_path, new_path)

min_number = min([pull_ep_number(f.split(".")[0])[1] for f in os.listdir(os.path.join(folder, path, arc)) if "[CBT]" not in f])


if min_number != 1:
    print(f"Minimum episode number is {min_number}, correcting numbering to start from 1.\n")
    for file in os.listdir(os.path.join(folder, path, arc)):
        if "[CBT]" in file:
            continue
        old_path = os.path.join(folder, path, arc, file)
        name, ep, ext = pull_ep_number(file)
        new_name = correct_numbering(name, ep, ext, min_number)
        new_path = os.path.join(folder, path, arc, new_name)
        print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
        os.rename(old_path, new_path)

pattern1 = r"Gintama \d{2}"
pattern2 = r"Gintama \d{3}"
good_pattern = r"Gintama S\d{2}\d{2}"
good_pattern2 = r"Gintama S\d{2}\d{3}"


def correct_or_not(filename):
    if re.search(good_pattern, filename):
        return True
    elif re.search(good_pattern2, filename):
        return True
    return False


def new_name_of_episode(file_name, season):
    for pattern in [pattern2, pattern1]:
        try:
            match = re.search(pattern, file_name)
            current_epidose_label = match.group()
            assert current_epidose_label != "00", "Episode label cannot be 00"
        except AttributeError:
            print("uppercase search failed, trying lowercase")
            continue
        ext = os.path.splitext(file_name)[1]
        splitup = current_epidose_label.split(" ")
        desired_label = splitup[0] + f" S{str(season).zfill(2)}" + splitup[1] + ext
        return desired_label

    raise ValueError(f"No matching pattern found in filename: {file_name}")


for season in [1, 2, 3, 4, 5, 6]:
    arc = f"Gintama/Season {season}"
    if not os.path.exists(os.path.join(folder, path, arc)):
        continue
    print(os.path.join(folder, path, arc))
    for file in os.listdir(os.path.join(folder, path, arc)):
        try:
            if correct_or_not(file):
                continue
            old_path = os.path.join(folder, path, arc, file)
            new_name = new_name_of_episode(file, season)
            new_path = os.path.join(folder, path, arc, new_name)
            print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
            os.rename(old_path, new_path)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            # raise e

pattern1 = r"S\d{2}\d{2}"
pattern2 = r"S\d{2}\d{3}"
good_pattern = r"S\d{2}E\d{2}"
good_pattern2 = r"S\d{2}E\d{3}"


def correct_or_not(filename):
    if re.search(good_pattern, filename):
        return True
    elif re.search(good_pattern2, filename):
        return True
    return False


def new_name_of_episode(file_name, season):
    for pattern in [pattern2, pattern1]:
        try:
            match = re.search(pattern, file_name)
            current_epidose_label = match.group()
        except AttributeError:
            print("uppercase search failed, trying lowercase")
            continue
        # ext = os.path.splitext(file_name)[1]
        # splitup = current_epidose_label.split(" ")
        desired_label = f" S{str(season).zfill(2)}" + "E" + current_epidose_label[-2:]
        return file_name.replace(current_epidose_label, desired_label)

    raise ValueError(f"No matching pattern found in filename: {file_name}")


for season in [1, 2, 3, 4, 5, 6]:
    arc = f"Gintama/Season {season}"
    if not os.path.exists(os.path.join(folder, path, arc)):
        continue
    print(os.path.join(folder, path, arc))
    for file in os.listdir(os.path.join(folder, path, arc)):
        try:
            if correct_or_not(file):
                continue
            old_path = os.path.join(folder, path, arc, file)
            new_name = new_name_of_episode(file, season)
            new_path = os.path.join(folder, path, arc, new_name)
            print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
            # os.rename(old_path, new_path)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            # raise e
