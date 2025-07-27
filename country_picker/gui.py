import sys

from PySide6.QtCore import Qt, QThread, Signal
from .json_parser import get_country_names
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QComboBox
)

class CountryLoaderThread(QThread):
    """Background thread for loading countries"""
    
    #Signals to be picked up by the main thread
    countries_loaded = Signal(list)  #Emits list of country names
    error_occurred = Signal(str)     #Emits error message
    
    def run(self):
        try:
            country_names = get_country_names()
            self.countries_loaded.emit(country_names)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.country_thread = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Country Picker")

        layout = QVBoxLayout()
        
        #Define the label and combo box vars
        self.myComboBox = QComboBox()
        self.myLabel = QLabel()
        self.myLoadingLabel = QLabel()
        #Connect signal and slot for handling combo box drop down selection
        self.myComboBox.currentTextChanged.connect(self.handle_country_text_changed)
        #Add widgets to layout
        layout.addWidget(self.myComboBox)
        layout.addWidget(self.myLabel)
        layout.addWidget(self.myLoadingLabel)

        #Dummy widget to apply layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #Get the countries and populate the combo box drop down
        self.get_countries()
    
    def get_countries(self):
        #Display loading message
        self.myLoadingLabel.setText("Countries Loading")

        #Clear combo box and show loading message
        self.myComboBox.clear()
        self.myComboBox.addItems(["Loading countries..."])
        self.myLabel.setText("Downloading country data...")
        
        #Create background thread
        self.country_thread = CountryLoaderThread()

        #Connect background thread signals to handlers in the main thread
        self.country_thread.countries_loaded.connect(self.handle_countries_loaded)
        self.country_thread.error_occurred.connect(self.handle_country_download_error)

        #Start the thread
        self.country_thread.start()

    def handle_countries_loaded(self, country_names):
        self.myComboBox.clear()
        self.myComboBox.addItems(country_names)
        self.myLoadingLabel.setText(f"Loaded {len(country_names)} countries. Select one:")

    def handle_country_download_error(self, error_message):
        self.myComboBox.clear()
        self.myComboBox.addItems(["Error loading countries"])
        self.myLoadingLabel.setText(f"Error: {error_message}")

    def handle_country_text_changed(self, country):
        self.myLabel.setText(f"Selected: {country}")
