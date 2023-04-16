from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QFileDialog
from pytube import YouTube
from moviepy.editor import *
import pyperclip
import os
import configparser
import sys

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create a config parser object
        self.config = configparser.ConfigParser()

        # Check if configuration file exists
        if os.path.exists('config.ini'):
            # If it exists, read the path from the config file
            self.config.read('config.ini')
            self.path = self.config.get('Settings', 'path')
        else:
            # If it doesn't exist, set path to an empty string
            self.path = ''
        
        self.initUI()
        
    def initUI(self):
        # create main window
        self.setWindowTitle("YouTube MP3 Downloader")
        self.setGeometry(100, 100, 575, 300)

        # create download directory frame
        directory_frame = QFrame(self)
        directory_frame.setFrameShape(QFrame.StyledPanel)
        directory_frame.setFrameShadow(QFrame.Raised)

        directory_layout = QHBoxLayout()
        directory_frame.setLayout(directory_layout)

        directory_label = QLabel("Download Directory:", self)
        directory_layout.addWidget(directory_label)

        self.path_entry = QLineEdit(self)
        self.path_entry.setText(self.path)
        self.path_entry.setReadOnly(True)
        directory_layout.addWidget(self.path_entry)

        directory_button = QPushButton("Choose", self)
        directory_button.clicked.connect(self.choose_directory)
        directory_layout.addWidget(directory_button)

        # create URL frame
        url_frame = QFrame(self)
        url_frame.setFrameShape(QFrame.StyledPanel)
        url_frame.setFrameShadow(QFrame.Raised)

        url_layout = QHBoxLayout()
        url_frame.setLayout(url_layout)

        url_label = QLabel("YouTube URL:", self)
        url_layout.addWidget(url_label)

        self.url_entry = QLineEdit(self)
        url_layout.addWidget(self.url_entry)

        paste_button = QPushButton("Paste", self)
        paste_button.clicked.connect(self.paste_clipboard)
        url_layout.addWidget(paste_button)

        # create download button
        download_button = QPushButton("Download MP3", self)
        download_button.clicked.connect(self.download_mp3)

        # create info label
        self.info_label = QLabel(self)

        # create layout for main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(directory_frame)
        main_layout.addWidget(url_frame)
        main_layout.addWidget(download_button)
        main_layout.addWidget(self.info_label)

        # set the layout of the main window
        main_widget = QFrame(self)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def choose_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if path:
            self.path = path
            self.path_entry.setText(self.path)
            # Save the path to the configuration file
            self.config['Settings'] = {'path': self.path}
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

    def paste_clipboard(self):
        clipboard_data = pyperclip.paste()
        self.url_entry.setText(clipboard_data)

    def download_mp3(self):
        url = self.url_entry.text()
        if len(url) > 0: 
            url = url.split("&")[0]
            video = YouTube(url)
            audio_stream = video.streams.filter(mime_type="audio/mp4").first()
            audio_file = audio_stream.download()
            audio_file_name = audio_file.split("\\")[-1]
            audio_file_name = audio_file_name.replace(".mp4", ".mp3")
            audio_file_path = os.path.join(self.path, audio_file_name)
            video_clip = AudioFileClip(audio_file)
            video_clip.write_audiofile(audio_file_path)
            video_clip.close()
            os.remove(audio_file)
            self.info_label.setText("MP3 Downloaded Successfully")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec_())