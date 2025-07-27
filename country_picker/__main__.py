from PySide6.QtWidgets import QApplication
from .gui import MainWindow
import sys

def main() -> None:
    '''Entry point for the application'''
    app = QApplication(sys.argv)
    app.setApplicationName("Country Picker")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main() 