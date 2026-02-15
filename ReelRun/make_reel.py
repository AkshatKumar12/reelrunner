from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re
import os
import random

# -----------------------
# PICK RANDOM VIDEO
# -----------------------

clips_folder = "clips"

videos = [
    os.path.join(clips_folder, f)
    for f in os.listdir(clips_folder)
    if f.endswith(".mp4")
]

if not videos:
    raise ValueError("No videos found in clips folder")

chosen_video = random.choice(videos)
print("Using video:", chosen_video)

video = VideoFileClip(chosen_video)
# Resize & crop to 9:16
video = video.resize(height=1280)

if video.w > 720:
    x_center = video.w / 2
    video = video.crop(
        x_center=x_center,
        width=720,
        height=1280
    )

# -----------------------
# LOAD AUDIO
# -----------------------

audio = AudioFileClip("voice.mp3")
video = video.loop(duration=audio.duration).set_audio(audio)

# -----------------------
# COLOR RULES
# -----------------------

danger_words = {
    "danger","death","kill","warning",
    "risk","scary","fear","dead"
}

def get_color(word):
    if re.search(r"\d", word):
        return "#4CFF00"
    if word.lower() in danger_words:
        return "#FF3B3B"
    return "#FFD93D"

# -----------------------
# TEXT IMAGE
# -----------------------

def text_img(text):

    W,H = 520,150
    img = Image.new("RGBA",(W,H),(0,0,0,0))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf",52)

    color = get_color(text)

    draw.rounded_rectangle(
        [(0,0),(W,H)],
        radius=40,
        fill=(0,0,0,180)
    )

    bbox = draw.textbbox((0,0),text,font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]

    x=(W-w)//2
    y=(H-h)//2

    for dx in range(-4,5):
        for dy in range(-4,5):
            draw.text((x+dx,y+dy),text,font=font,fill="black")

    draw.text((x,y),text,font=font,fill=color)

    return np.array(img)

# -----------------------
# WORD CLIP
# -----------------------

def word_clip(word,start,end):

    img = text_img(word.upper())
    dur = end-start

    return (
        ImageClip(img)
        .set_start(start)
        .set_duration(dur)

        # CENTER POSITION
        .set_position(("center", 0.5), relative=True)

        .resize(lambda t: 1 + 0.35*np.exp(-6*t))
        .fadein(0.05)
        .fadeout(0.05)
    )



# -----------------------
# LOAD TIMESTAMPS
# -----------------------

lines = open("timestamps.txt",encoding="utf-8").read().splitlines()

subs=[]

for line in lines:
    s,e,w=line.split("|")
    s,e=float(s),float(e)
    subs.append(word_clip(w,s,e))

# -----------------------
# FINAL
# -----------------------

final=CompositeVideoClip([video]+subs)

final.write_videofile(
    "whisper_reel_v2.mp4",
    fps=24,
    codec="libx264",
    preset="ultrafast",
    audio_codec="aac"
)

print("✅ Done! Random background reel ready.")
