import os
import re

folder = "/mnt/20Thdd"
path = "media/anime"
arc = "Gintama/Season 4"
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
