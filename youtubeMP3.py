from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *

def choose_directory():
    path = filedialog.askdirectory()
    directory_label.config(text=path)
    path_entry.delete(0, END)
    path_entry.insert(0, path)

def download_mp3():
    url = url_entry.get()
    url = url.split("&")[0]
    video = YouTube(url)
    audio_stream = video.streams.filter(mime_type="audio/mp4").first()
    audio_file = audio_stream.download()
    video_title = video.title.replace("|","-").replace(":","-").replace("\"","'")
    mp3_file = f"{path_entry.get()}/{video_title}.mp3"
    AudioFileClip(audio_file).write_audiofile(mp3_file)
    os.remove(audio_file)  # remove the downloaded .mp4 file
    info_label.config(text="Download complete!")

root = Tk()
root.title("YouTube MP3 Downloader")

directory_label = Label(root, text="Choose download directory:")
directory_label.pack()

path_entry = Entry(root, width=50)
path_entry.pack()

directory_button = Button(root, text="Choose", command=choose_directory)
directory_button.pack()

url_label = Label(root, text="Paste YouTube URL below:")
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack()

download_button = Button(root, text="Download MP3", command=download_mp3)
download_button.pack()

info_label = Label(root, text="")
info_label.pack()

root.mainloop()
