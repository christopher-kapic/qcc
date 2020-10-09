# Tasks to do:
# Get emotions for each frame
# Get phoneme for each frame
# Draw each frame
# Combine frames
# Voice change

import sys
from moviepy import editor as e
import speech_recognition as sr
import requests
import subprocess
import os
import shutil
from deepface import DeepFace
import numpy as np
from PIL import Image
import json

# making a new clean frames directory
# I'm doing this early because I've had problems with it being run right before I save the frames.
try:
    shutil.rmtree("./frames")
    os.mkdir("frames")
except:
    os.mkdir("frames")

# Making audio file from video
video = e.VideoFileClip(sys.argv[1])
audio = video.audio
audio.write_audiofile(sys.argv[1] + ".wav")
fps = video.reader.fps

# Getting transcript from audio file
r = sr.Recognizer()
audio_source = sr.AudioFile(sys.argv[1] + ".wav")
with audio_source as source:
    _audio = r.record(source)
# print(r.recognize_google(_audio))
script = r.recognize_google(_audio)
with open(sys.argv[1] + ".txt", "w") as t:
    t.write(script)

# Getting phonemes JSON
# Currently you must start up the web app before running the python script.
params = (("async", "false"),)
files = {
    "audio": (sys.argv[1] + ".wav", open(sys.argv[1] + ".wav", "rb")),
    "transcript": (sys.argv[1] + ".txt", open(sys.argv[1] + ".txt", "rb")),
}
response_ = requests.post(
    "http://localhost:8765/transcriptions", params=params, files=files
)


response = response_.json()
# Saving every frame of the video to a folder "./frames"
video.write_images_sequence("frames/frame%06d.jpeg")

# definitely should add "M, P, B" mouth in the future.
def phoneme_to_mouth_phoneme(phoneme):
    if phoneme == "hh_B":
        return "ah_mouth"
    elif phoneme == "":
        return "f_mouth"
    elif phoneme == "tempa":
        return "o_mouth"
    elif phoneme == "tempb":
        return "oo_mouth"
    elif phoneme == "tempc":
        return "t_mouth"
    elif phoneme == "tempd":
        return "y_mouth"
    elif phoneme == "MPB":
        # return "m_mouth"
        return "standard_mouth"
    else:
        return "standard_mouth"
    # need to add more cases


def emotion_to_eyebros(emo):
    if emo == "happy":
        return "standard_eyebrows"
    elif emo == "angry":
        return "angry_eyebrows"
    elif emo == "disgust":
        return "confused_eyebrows"
    elif emo == "fear":
        return "sad_eyebrows"
    elif emo == "surprise":
        return "confused_eyebrows"
    else:
        return "standard_eyebrows"


def get_paste_area(center, width, height):
    return (
        int(round(center[0] - (width / 2))),
        int(round(center[1] - (height / 2))),
        int(round(center[0] + (width / 2))),
        int(round(center[1] + (height / 2))),
    )


def get_emotion(img):
    img_array = np.array(img)
    return DeepFace.analyze(img_array, actions=["emotion"])["dominant_emotion"]


for n in range(video.reader.nframes - 1):
    # print("./frames/frame{:06d}".format(n))
    img1 = Image.open(os.getcwd() + "/frames/frame{:06d}.jpeg".format(n))
    emo = get_emotion(img1)
    # emo = "happy"
    mouth_phoneme = phoneme_to_mouth_phoneme("none")
    frame_time = n / fps
    for word in response["words"]:
        if frame_time < word["start"]:
            mouth_phoneme = phoneme_to_mouth_phoneme("none")
        elif frame_time >= word["start"] and frame_time <= word["end"]:
            tracker = word["start"]
            for phoneme in word["phones"]:
                if frame_time >= tracker and frame_time < tracker + phoneme["duration"]:
                    mouth_phoneme = phoneme_to_mouth_phoneme(phoneme["phone"])
                    break
                elif (
                    frame_time >= tracker + phoneme["duration"]
                    and frame_time < word["end"]
                ):
                    tracker += phoneme["duration"]
                else:
                    mouth_phomeme = phoneme_to_mouth_phoneme("none")
        else:
            mouth_phoneme = phoneme_to_mouth_phoneme("none")
            break
    img0 = Image.open(os.getcwd() + "/frames/frame{:06d}.jpeg".format(n))
    width, height = img0.size
    img0_center = (width / 2, height / 2)
    img00 = Image.open(
        os.getcwd() + "/avatars/{}/{}.png".format(sys.argv[2], "background")
    )
    width00, height00 = img00.size
    img01 = Image.open(
        os.getcwd() + "/avatars/{}/{}.png".format(sys.argv[2], "character")
    )
    width01, height01 = img01.size
    img02 = Image.open(
        os.getcwd() + "/avatars/{}/{}.png".format(sys.argv[2], mouth_phoneme)
    )
    width02, height02 = img02.size
    img03 = Image.open(
        os.getcwd() + "/avatars/{}/{}.png".format(sys.argv[2], emotion_to_eyebros(emo))
    )
    width03, height03 = img03.size
    img04 = Image.open(
        os.getcwd() + "/avatars/{}/{}.png".format(sys.argv[2], "foreground")
    )
    width04, height04 = img04.size

    img0.paste(img00, get_paste_area(img0_center, width00, height00), img00)
    img0.paste(img01, get_paste_area(img0_center, width01, height01), img01)
    img0.paste(img02, get_paste_area(img0_center, width02, height02), img02)
    img0.paste(img03, get_paste_area(img0_center, width03, height03), img03)
    img0.paste(img04, get_paste_area(img0_center, width04, height04), img04)

    img0.save(os.getcwd() + "/frames/frame{:06d}.jpeg".format(n),)
    img0.close()
    img00.close()
    img01.close()
    img02.close()
    img03.close()
    img04.close()


def get_frame_files(n):
    lis = []
    for i in range(n - 1):
        lis.append(os.getcwd() + "/frames/frame{:06d}.jpeg".format(i))
    return lis


audio_ = e.AudioFileClip(sys.argv[1] + ".wav")
clip = e.ImageSequenceClip(get_frame_files(video.reader.nframes), fps=fps)
clip.set_audio(audio)
# clip.write_videofile(sys.argv[1] + "_final.mp4")
clip.write_videofile("fnl.mp4", audio=audio_)

video.close()
clip.close()
