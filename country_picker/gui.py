import sys

from PySide6.QtCore import Qt
from .json_parser import get_country_names
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Country Picker")

        layout = QVBoxLayout()
        
        #Define the label and combo box vars
        self.myComboBox = QComboBox()
        self.myLabel = QLabel()
        #Connect signal and slot for handling combo box drop down selection
        self.myComboBox.currentTextChanged.connect(self.handle_country_text_changed)
        #Add widgets to layout
        layout.addWidget(self.myComboBox)
        layout.addWidget(self.myLabel)

        #dummy widget to apply layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #Get the countries and populate the combo box drop down
        self.get_countries()
    
    def get_countries(self):
        try:
            country_names = get_country_names()
            self.myComboBox.clear()
            self.myComboBox.addItems(country_names)
            
        except Exception as e:
            print(f"Error loading countries: {e}")
            self.myComboBox.clear()
            self.myComboBox.addItems(["Error loading countries"])
            self.myLabel.setText("Failed to load countries. Check your internet connection.")

    def handle_country_text_changed(self, country):
        self.myLabel.setText(country)
