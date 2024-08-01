import sys
from PyQt5.QtWidgets import QApplication
from gui import YTDLP_GUI
from settings import save_settings, load_settings

def main():
    app = QApplication(sys.argv)
    ex = YTDLP_GUI()

    # Load settings when the application starts
    load_settings(ex)

    # Ensure settings are saved when the application closes
    app.aboutToQuit.connect(lambda: save_settings(ex))

    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
