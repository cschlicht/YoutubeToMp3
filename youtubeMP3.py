from tkinter import *
from pytube import YouTube
from moviepy.editor import *
import os

def download_mp3():
    url = url_entry.get()
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download()
    mp3_file = os.path.splitext(audio_file)[0] + ".mp3"
    AudioFileClip(audio_file).write_audiofile(mp3_file)
    os.remove(audio_file)
    info_label.config(text="Download complete!")

root = Tk()
root.title("YouTube MP3 Downloader")

url_label = Label(root, text="Paste YouTube URL below:")
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack()

download_button = Button(root, text="Download MP3", command=download_mp3)
download_button.pack()

info_label = Label(root, text="")
info_label.pack()

root.mainloop()
