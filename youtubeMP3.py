from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import pyperclip
import os
import configparser

# Create a config parser object
config = configparser.ConfigParser()

# Check if configuration file exists
if os.path.exists('config.ini'):
    # If it exists, read the path from the config file
    config.read('config.ini')
    path = config.get('Settings', 'path')
else:
    # If it doesn't exist, set path to an empty string
    path = ''

def choose_directory():
    global path
    path = filedialog.askdirectory()
    directory_label.config(text=path)
    path_entry.delete(0, END)
    path_entry.insert(0, path)
    # Save the path to the configuration file
    config['Settings'] = {'path': path}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def paste_clipboard():
    clipboard_data = pyperclip.paste()
    url_entry.delete(0, END)
    url_entry.insert(0, clipboard_data)

def download_mp3():
    url = url_entry.get()
    url = url.split("&")[0]
    video = YouTube(url)
    audio_stream = video.streams.filter(mime_type="audio/mp4").first()
    audio_file = audio_stream.download()
    video_title = video.title.replace("|","-").replace(":","-").replace("\"","'")
    mp3_file = f"{path}/{video_title}.mp3"
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
path_entry.insert(0, path)

directory_button = Button(directory_frame, text="Choose", command=choose_directory, padx=padx, pady=pady)
directory_button.pack(side=LEFT)

url_label = Label(root, text="Paste YouTube URL below:", padx=padx, pady=pady)
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack(padx=padx, pady=pady, anchor='center')

paste_button = Button(root, text="Paste", command=paste_clipboard, padx=padx, pady=pady)
paste_button.pack(padx=padx, pady=pady)

download_button = Button(root, text="Download MP3", command=download_mp3, padx=padx, pady=pady)
download_button.pack(padx=padx, pady=pady)

info_label = Label(root, text="", padx=padx, pady=pady)
info_label.pack()

root.mainloop()
