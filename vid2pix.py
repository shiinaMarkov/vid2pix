import cv2
import os
from pathlib import Path, PureWindowsPath
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as img

import numpy as np

FRAME_OUTPUT_PATH = Path("frames")
VIDEO_PATH = Path("badapple.mp4")

# Current settings for arcade pacman

RESIZE_W = 224
RESIZE_H = 288

TILE_W = 28
TILE_H = 36

def write_frame_txt(frame_name, img_arr):
    with open(frame_name, 'w') as my_list_file:
        for row in img_arr:
             #writing to file line by line
            row_str = ' '.join(map(str, row))
            my_list_file.write(row_str + "\n")

def binarize_arr(arr):
    for i in range(0,len(arr)):
        for j in range(0,len(arr[i])):
            if arr[i][j] <= 127:
                arr[i][j] = 0
            else:
                arr[i][j] = 255
    return arr            


def convert_np_arr(npdata):
    td_arr = npdata[:,:,0]
    return td_arr


def remove_files(frames_path):
    file_list = os.listdir(frames_path)

    for files in file_list:
        if files.endswith(".png") or files.endswith(".txt"):
            os.remove(os.path.join(frames_path, files))

def extract_frames(video_path, frames_path):
    cap = cv2.VideoCapture(video_path)
    count = 0

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            print('Read %d frame: ' % count, ret)
            frame_name = str(Path(frames_path + "/frame" + str(count)))
            frame_res = cv2.resize(frame,(TILE_W,TILE_H))

            img_arr = convert_np_arr(frame_res)
            bin_arr = binarize_arr(img_arr)
            write_frame_txt(frame_name + ".txt", bin_arr)

            #cv2.imwrite(os.path.join(frames_path, "frame{:d}.png".format(count)), frame_res)  # save frame as JPEG file

            count += 1
        else:
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Remove all files in FRAME_OUTPUT_PATH: " + str(FRAME_OUTPUT_PATH))
    remove_files(str(FRAME_OUTPUT_PATH))
    
    print("Extracting video frames from: " + str(VIDEO_PATH))
    extract_frames(str(VIDEO_PATH), str(FRAME_OUTPUT_PATH))


if __name__=="__main__":
    main()
