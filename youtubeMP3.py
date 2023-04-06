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

# set padding for all widgets
padx = 10
pady = 10

directory_frame = Frame(root, padx=padx, pady=pady, bd=1, relief="solid")
directory_frame.pack(fill=X)

directory_label = Label(directory_frame, text="Choose download directory:", padx=padx, pady=pady)
directory_label.pack(side=LEFT)

path_entry = Entry(directory_frame, width=50)
path_entry.pack(side=LEFT, padx=padx, pady=pady)

directory_button = Button(directory_frame, text="Choose", command=choose_directory, padx=padx, pady=pady)
directory_button.pack(side=LEFT)

url_label = Label(root, text="Paste YouTube URL below:", padx=padx, pady=pady)
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack(padx=padx, pady=pady)

download_button = Button(root, text="Download MP3", command=download_mp3, padx=padx, pady=pady)
download_button.pack(padx=padx, pady=pady)

info_label = Label(root, text="", padx=padx, pady=pady)
info_label.pack()

root.mainloop()
