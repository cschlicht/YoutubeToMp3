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

# create main window
root = Tk()
root.title("YouTube MP3 Downloader")
root.geometry('575x300')

# create download directory frame
directory_frame = Frame(root, bd=2, relief="groove")
directory_frame.pack(side=TOP, fill=X, padx=10, pady=10)

directory_label = Label(directory_frame, text="Download Directory: ")
directory_label.pack(side=LEFT, padx=10, pady=10)

path_entry = Entry(directory_frame, width=50)
path_entry.pack(side=LEFT, padx=10, pady=10)
path_entry.insert(0, path)

directory_button = Button(directory_frame, text="Choose", command=choose_directory, padx=10, pady=10)
directory_button.pack(side=LEFT, padx=10, pady=10)

# create URL frame
url_frame = Frame(root, bd=2, relief="groove")
url_frame.pack(side=TOP, fill=X, padx=10, pady=10)

url_label = Label(url_frame, text="YouTube URL: ")
url_label.pack(side=LEFT, padx=10, pady=10)

url_entry = Entry(url_frame, width=50)
url_entry.pack(side=LEFT, padx=10, pady=10, anchor='center')

paste_button = Button(url_frame, text="Paste", command=paste_clipboard, padx=10, pady=10)
paste_button.pack(side=LEFT, padx=10, pady=10)

# create download button
download_button = Button(root, text="Download MP3", command=download_mp3, padx=10, pady=10)
download_button.pack(side=TOP, padx=10, pady=10)

# create info label
info_label = Label(root, text="", padx=10, pady=10)
info_label.pack(side=BOTTOM)

root.mainloop()
