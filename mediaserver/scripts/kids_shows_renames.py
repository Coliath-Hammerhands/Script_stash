import os
import re
from moviepy.editor import VideoFileClip
import numpy as np

folder = "/mnt/20Thdd"
path = "media/kids"
season = 1
lacking_pattern = r"S\d{2}E\d{2}"
correct_pattern = r"S\d{2}E\d{2}E\d{2}"
lowercase_lacking = r"s\d{2}e\d{2}"
lowercase_correct_pattern = r"s\d{2}e\d{2}e\d{2}"
cuttoff = int(np.floor(60 * 13.5))


def get_video_duration_moviepy(file_path):
    """
    Gets the duration of a video file using moviepy.
    Returns duration in seconds (float).
    """
    try:
        with VideoFileClip(file_path) as video:
            duration = video.duration
        return duration
    except Exception as e:
        print(f"Error processing file with moviepy: {e}")
        return None


def correct_or_not(filename):
    if re.search(correct_pattern, filename):
        return True
    elif re.search(lowercase_correct_pattern, filename):
        return True
    return False


def new_name_of_episode(file_name):
    for pattern, replacement in zip([lacking_pattern, lowercase_lacking], ["E", "e"]):
        try:
            match = re.search(pattern, file_name)
            current_epidose_label = match.group()
            current_ep_number = re.search(r"E\d{2}", file_name).group()
            int_ep_number = int(current_ep_number.replace(replacement, ""))
        except AttributeError:
            print("uppercase search failed, trying lowercase")
            continue
        upper_ep_number = int(int_ep_number * 2)
        lower = upper_ep_number - 1
        return file_name.replace(current_epidose_label, f"S{str(season).zfill(2)}E{str(lower).zfill(2)}E{str(upper_ep_number).zfill(2)}")
    try:
        name, ext = os.path.splitext(file_name)
        file_name = name.upper() + ext
        match = re.search(lacking_pattern, file_name)
        current_epidose_label = match.group()
        current_ep_number = re.search(r"E\d{2}", file_name).group()
        int_ep_number = int(current_ep_number.replace("E", ""))
        upper_ep_number = int(int_ep_number * 2)
        lower = upper_ep_number - 1
        return file_name.replace(current_epidose_label, f"S{str(season).zfill(2)}E{str(lower).zfill(2)}E{str(upper_ep_number).zfill(2)}")
    except AttributeError:
        print("forced uppercase search failed, giving up")
    raise ValueError(f"No matching pattern found in filename: {file_name}")


arc_template = "/Season {}"
for series in ["Mickey Mouse - Mixed-Up Adventures", "Iron Man and His Awesome Friends", "Mickey Mouse Funhouse"]:
    season_range = list(range(1, 8))
    if series in ("Big City Greens"):
        season_range = [1]
    for season in season_range:
        arc = series + arc_template.format(season)
        if not os.path.exists(os.path.join(folder, path, arc)):
            continue

        for file in os.listdir(os.path.join(folder, path, arc)):
            try:
                if correct_or_not(file):
                    continue

                old_path = os.path.join(folder, path, arc, file)
                length_seconds = get_video_duration_moviepy(old_path)
                if length_seconds is None:
                    print(f"Could not get duration for file {file}, skipping.")
                    raise ValueError("Could not get duration")
                elif length_seconds < cuttoff:
                    print(f"File {file} is shorter than cutoff ({length_seconds} < {cuttoff}), skipping.")
                    continue
                new_name = new_name_of_episode(file)
                new_path = os.path.join(folder, path, arc, new_name)
                print(f"Renaming:\n{old_path}\nto\n{new_path}\n")
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                raise e
