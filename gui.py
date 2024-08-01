import os
import json
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QFileDialog, QMessageBox, QProgressBar,
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from downloader import DownloadThread
from settings import SETTINGS_FILE, save_settings, load_settings

class YTDLP_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.initUI()
        load_settings(self)  # Load settings on initialization

    def initUI(self):
        self.setWindowTitle('Mocha')
        self.setWindowIcon(QIcon('icons/coffee_icon.png'))
        self.setGeometry(100, 100, 400, 415)
        self.setFixedSize(400, 415)  # Set the window size and make it non-resizable

        self.setStyleSheet("""
            QWidget {
                background-color: #3E2723;
                color: #D7CCC8;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 20px;
            }
            QLabel {
                font-size: 20px;
                margin-bottom: 10px;
            }
            QLineEdit, QComboBox {
                background-color: #5D4037;
                border: 1px solid #4E342E;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
                color: #D7CCC8;
            }
            QPushButton {
                background-color: #8D6E63;
                border: 1px solid #6D4C41;
                border-radius: 5px;
                color: #D7CCC8;
                font-size: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #6D4C41;
                color: white;
            }
            QProgressBar {
                border: 1px solid #4E342E;
                border-radius: 5px;
                background-color: #5D4037;
                text-align: center;
                color: #D7CCC8;
                font-size: 20px;
            }
            QProgressBar::chunk {
                background-color: #D7CCC8;
                border-radius: 5px;
            }
            QRadioButton {
                margin-right: 10px;
                font-size: 20px;
            }
            
            
        """)

        # Create a central widget and set it as the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set background image for central widget
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('images/coffee_background.jpg')))
        central_widget.setAutoFillBackground(True)
        central_widget.setPalette(palette)

        main_layout = QVBoxLayout(central_widget)

        # URL Input
        self.url_label = QLabel('Video URL:')
        self.url_input = QLineEdit(self)

        # Output Type
        self.output_type_label = QLabel('Output Type:')
        self.video_radio = QRadioButton('Video')
        self.audio_radio = QRadioButton('Audio')
        self.output_type_group = QButtonGroup()
        self.output_type_group.addButton(self.video_radio)
        self.output_type_group.addButton(self.audio_radio)
        self.video_radio.setChecked(True)  # Default to video

        type_layout = QHBoxLayout()
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.audio_radio)

        # Output Location
        self.location_label = QLabel('Save Location:')
        self.location_input = QLineEdit(self)
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_location)

        location_layout = QHBoxLayout()
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(self.browse_button)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # Download Button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.start_download)

        # Cancel Button
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setVisible(False)

        # Add widgets to layout
        main_layout.addWidget(self.url_label)
        main_layout.addWidget(self.url_input)
        main_layout.addWidget(self.output_type_label)
        main_layout.addLayout(type_layout)
        main_layout.addWidget(self.location_label)
        main_layout.addLayout(location_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.download_button)
        main_layout.addWidget(self.cancel_button)
        main_layout.addStretch()  # Add a stretch at the end to push widgets up

    def browse_location(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.location_input.setText(directory)

    def start_download(self):
        url = self.url_input.text()
        location = self.location_input.text()
        output_type = 'video' if self.video_radio.isChecked() else 'audio'

        if not url or not location:
            QMessageBox.warning(self, 'Error', 'URL and Save Location cannot be empty.')
            return

        self.download_button.setVisible(False)
        self.cancel_button.setVisible(True)

        self.download_thread = DownloadThread(url, location, output_type)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def cancel_download(self):
        if self.download_thread:
            self.download_thread.terminate()
            self.download_thread = None
            self.download_button.setVisible(True)
            self.cancel_button.setVisible(False)
            self.progress_bar.setValue(0)
            QMessageBox.information(self, 'Cancelled', 'Download cancelled.')

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self, success, message):
        self.download_thread = None
        self.download_button.setVisible(True)
        self.cancel_button.setVisible(False)
        if success:
            QMessageBox.information(self, 'Success', 'Download completed successfully.')
        else:
            QMessageBox.critical(self, 'Error', message)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d['_percent_str']
            percent = float(p.strip('%'))
            self.update_progress(int(percent))
        elif d['status'] == 'finished':
            self.update_progress(100)

    def show_settings(self):
        QMessageBox.information(self, 'Settings', 'Settings functionality not implemented yet.')

    def show_help(self):
        QMessageBox.information(self, 'Help', 'Help functionality not implemented yet.')
