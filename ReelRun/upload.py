from instagrapi import Client
import time

cl = Client()
cl.login("username", "password")

time.sleep(5)

cl.video_upload(
    "whisper_reel.mp4",
    caption="Daily upload"
)

print("Done")
