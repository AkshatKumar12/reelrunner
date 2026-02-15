import os
from moviepy.editor import VideoFileClip

# -----------------------
# SETTINGS
# -----------------------

input_video = "long.mp4"   # your video file
output_folder = "clips"
chunk_duration = 45  # seconds

# -----------------------
# CREATE FOLDER
# -----------------------

os.makedirs(output_folder, exist_ok=True)

# -----------------------
# LOAD VIDEO
# -----------------------

video = VideoFileClip(input_video).without_audio()
total_duration = int(video.duration)

print(f"Total duration: {total_duration}s")

# -----------------------
# SPLIT LOOP
# -----------------------

start = 0
clip_num = 1

while start < total_duration:
    end = min(start + chunk_duration, total_duration)

    subclip = video.subclip(start, end)

    output_path = os.path.join(
        output_folder,
        f"clip_{clip_num}.mp4"
    )

    subclip.write_videofile(
        output_path,
        codec="libx264",
        audio=False
    )

    print(f"Saved: {output_path}")

    start += chunk_duration
    clip_num += 1

print("\n✅ Done! All clips saved.")
