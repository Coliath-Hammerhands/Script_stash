import os
import re

folder = "/mnt/20Thdd"
path = "media/anime"
season = 2
arc = f"Baki the Grappler/Season {season}"
pattern = r"\[.*?\]|[^\[\]]+"
# chapter_chunk=2
episode_number = 1


def parse_episode(filename):
    ext = os.path.splitext(filename)[1]
    name = filename.replace(ext, "").strip()
    matches = re.findall(pattern, name)
    cleaned_matches = [item.replace("[", "").replace("]", "").strip() for item in matches if item.strip()]
    # print(cleaned_matches)
    assert cleaned_matches[0] == "Anime-Ancestors", f"It was {cleaned_matches[0]}"
    return f"{cleaned_matches[episode_number]}{ext}"


def pull_ep_number(episode_str):
    ext = os.path.splitext(episode_str)[1]
    strings = [x for x in episode_str.replace(ext, "").strip().split("_") if not x.isdigit()]
    number = [x for x in episode_str.replace(ext, "").strip().split("_") if x.isdigit()][0]
    # name = episode_str.replace(ext, "").strip()
    # return f"E{int(number)} {(' '.join(strings).strip())}{ext}"
    return f"S{str(season).zfill(2)}E{int(number)} {(' '.join(strings)).strip()}{ext}"
    # return name.split(" ")[0], int(name.split(" ")[1]), ext


for file in os.listdir(os.path.join(folder, path, arc)):
    if "[Anime-Ancestors]" not in file:
        continue
    old_path = os.path.join(folder, path, arc, file)
    new_name = parse_episode(file)
    new_path = os.path.join(folder, path, arc, new_name)
    print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
    os.rename(old_path, new_path)

for file in os.listdir(os.path.join(folder, path, arc)):
    if f"S{str(season).zfill(2)}" not in file:
        old_path = os.path.join(folder, path, arc, file)
        # new_name = parse_episode(file)
        new_path = os.path.join(folder, path, arc, f"S{str(season).zfill(2)}" + file)  # old_path.replace(f"S{str(season).zfill(2)}", "")
        os.rename(old_path, new_path)
for file in os.listdir(os.path.join(folder, path, arc)):
    if "[Anime-Ancestors]" in file:
        continue
    if file[0] != "_":
        continue
    old_path = os.path.join(folder, path, arc, file)
    new_name = pull_ep_number(file)
    # new_name = correct_numbering(name, ep, ext, min_number)
    new_path = os.path.join(folder, path, arc, new_name)
    print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
    os.rename(old_path, new_path)

#### Renumber


def pull_up_with_season(episode_str):
    name, ext = os.path.splitext(episode_str)
    pattern = r"S\d{2}E\d{2}"
    if re.search(pattern, episode_str):
        pass
    else:
        pattern = r"S\d{2}E\d{1}"
    match = re.search(pattern, episode_str)
    # name = episode_str.replace(ext, "").strip()
    return int(match.group().split("E")[1]), name.replace(match.group(), "").strip(), ext


min_number = min([pull_up_with_season(f)[0] for f in os.listdir(os.path.join(folder, path, arc)) if "[CBT]" not in f])


def correct_numbering(name, number_str, ext, min_number):
    number = int(number_str) + 1 - min_number
    return name + " " + str(number).zfill(2) + ext


if min_number != 1:
    print(f"Minimum episode number is {min_number}, correcting numbering to start from 1.\n")
    for file in os.listdir(os.path.join(folder, path, arc)):
        if "[CBT]" in file:
            continue
        old_path = os.path.join(folder, path, arc, file)
        episode_number, name, ext = pull_up_with_season(file)
        episdoe_number_corrected = int(episode_number) + 1 - min_number
        # name, ep, ext = pull_ep_number(file)
        # new_name = correct_numbering(name, ep, ext, min_number)
        new_name = f"S{str(season).zfill(2)}E{str(episdoe_number_corrected).zfill(2)} {name}{ext}"
        new_path = os.path.join(folder, path, arc, new_name)
        print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
        os.rename(old_path, new_path)
