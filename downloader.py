import os
import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, url, location, output_type):
        super().__init__()
        self.url = url
        self.location = location
        self.output_type = output_type

    def run(self):
        ydl_opts = {
            'outtmpl': os.path.join(self.location, f'%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
        }

        if self.output_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished.emit(True, 'Download completed successfully.')
        except yt_dlp.utils.DownloadError as e:
            self.finished.emit(False, f'An error occurred: {str(e)}.')
        except Exception as e:
            self.finished.emit(False, f'An unexpected error occurred: {str(e)}')

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d['_percent_str']
            percent = float(p.strip('%'))
            self.progress.emit(int(percent))
        elif d['status'] == 'finished':
            self.progress.emit(100)
