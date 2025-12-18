import os
import re

folder = "/mnt/20Thdd"
path = "media/One Pace"
arc = "[909-1002] Wano"
pattern = r"\[.*?\]|[^\[\]]+"
chapter_chunk = 1
episode_number = 2


def parse_episode(filename):
    ext = os.path.splitext(filename)[1]
    name = filename.replace(ext, "").strip()
    matches = re.findall(pattern, name)
    cleaned_matches = [item.replace("[", "").replace("]", "").strip() for item in matches if item.strip()]
    # print(cleaned_matches)
    assert cleaned_matches[0] == "One Pace", f"It was {cleaned_matches[0]}"
    return f"[{cleaned_matches[chapter_chunk]}] {cleaned_matches[episode_number]}{ext}"


for file in os.listdir(os.path.join(folder, path, arc)):
    if "[One Pace]" not in file:
        continue
    old_path = os.path.join(folder, path, arc, file)
    new_name = parse_episode(file)
    new_path = os.path.join(folder, path, arc, new_name)
    print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
    os.rename(old_path, new_path)

for file in os.listdir(os.path.join(folder, path, arc)):
    if file[0] != "[":
        old_path = os.path.join(folder, path, arc, file)
        temp = file.split(" ")
        temp[0] = "[" + temp[0] + "]"
        new_name = " ".join(temp)
        new_path = os.path.join(folder, path, arc, new_name)
        print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
        os.rename(old_path, new_path)
