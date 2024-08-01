import sys
from PyQt5.QtWidgets import QApplication
from gui import YTDLP_GUI

def main():
    app = QApplication(sys.argv)
    ex = YTDLP_GUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
