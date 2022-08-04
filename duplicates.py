# =================================
# ======= import libraries ========
# =================================

import os
import cv2
import hashlib
from tqdm import tqdm
import argparse

# =================================
# =========== arguments ===========
# =================================

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="directory path", type=str)
parser.add_argument("-ho", "--hash-only", help="use only hash method (default: False)", default=False, action="store_true")
parser.add_argument( "-s", "--save", help="save duplicated files names (default: False)", default=False, action="store_true")
args = parser.parse_args()

# =================================
# ========= calculations ==========
# =================================

def size(file_path):
    # get file size in KB
    return os.stat(file_path).st_size // 1024

def duration(file_path):
    # capture the video
    video = cv2.VideoCapture(file_path)
    # get fps video capture properties
    fps = video.get(cv2.CAP_PROP_FPS)
    # get frame count video capture properties
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    # calculate video duration seconds
    duration_seconds = frame_count / fps if fps else 0
    # return duration seconds
    return duration_seconds

# =================================
# ========== comparison ===========
# =================================

def compare_size(file_path1, file_path2):
    # compare if the two files have the same size in KB
    return size(file_path1) == size(file_path2)


def compare_duration(file_path1, file_path2):
    # compare if the two files have the same duration
    return duration(file_path1) == duration(file_path2)

# =================================
# ========== duplication ==========
# =================================

def extension(file_name):
    # get file extension
    return file_name.split(".")[-1].lower()

def duplicates(path, hash_only=False):
    duplicate_list = []
    unique_list = []
    unique = dict()
    # specify valid extensions for the size and duration algorithm
    valid_ext = [] if hash_only else ["mp4", "mkv", "mp3"]
    # start detecting duplicated files
    for current_file in tqdm(os.listdir(path), desc="detecting duplicates: "):
        # get current file path
        current_file_path = os.path.join(path, current_file)
        # check for file time to specify the algorithm
        # if the current file is a video on audio file, we check for its size and duration
        if extension(current_file) in valid_ext:
            # filters directory files to be just videos or audios
            videos = [
                video for video in os.listdir(path) if extension(video) in valid_ext
            ]
            # loop over the filtered files
            for video in videos:
                # get target video path
                file_path = os.path.join(path, video)
                # check if the current video is not the target
                if current_file_path != file_path:
                    # check if the target video is already detected
                    if file_path not in duplicate_list and file_path not in unique_list:
                        # check if the two videos have the same size in KB
                        if compare_size(current_file_path, file_path):
                            # check if the two videos have the same duration
                            if compare_duration(current_file_path, file_path):
                                # add the target video to the list after passing all the conditions
                                unique_list.append(current_file_path)
                                duplicate_list.append(file_path)
        # if the current file is not a video on audio file, we use hash method to detect the duplicates
        else:
            # get file hash
            file_hash = hashlib.md5(open(current_file_path, "rb").read()).hexdigest()
            # append the current file if it has unique hash
            if file_hash not in unique:
                unique[file_hash] = current_file_path
            # the file is duplicated because it does not have unique hash
            else:
                duplicate_list.append(current_file_path)
    # return duplicates list
    return duplicate_list

# =================================
# =========== deletion ============
# =================================

def remove(duplicate_list):
    # loop over all duplicated videos and delete them
    for file_path in tqdm(duplicate_list, desc="deleting duplicates: "):
        # check if the target file is exists to avoid exception error
        if os.path.exists(file_path):
            # delete the target file
            os.remove(file_path)

# =================================
# ============= main ==============
# =================================

if __name__ == "__main__":
    # check if the user passed the directory path
    if args.dir:
        # get duplicated files
        duplicate_list = duplicates(args.dir, args.hash_only)
        # check for duplicates
        if len(duplicate_list) > 0:
            # save list
            if args.save:
                with open("./duplicated files.txt", "+w") as file:
                    [file.write(file_name + "\n") for file_name in duplicate_list]
            # ask user to delete the duplicated files
            input(f"\n{len(duplicate_list)} duplicates were detected, press anything to delete them all")
            # remove duplicates
            remove(duplicate_list)
        else:
            print("no duplicates were detected")
        print("DONE!")
    else:
        print("please run the script properly. for more info: https://github.com/0aub/duplicates-cleaner")
