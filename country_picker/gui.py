import sys

from PySide6.QtCore import Qt
import requests
import json
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
        #Get the countries and populate the combo box drop down
        self.get_countries()
        #Add widgets to layout
        layout.addWidget(self.myComboBox)
        layout.addWidget(self.myLabel)

        #dummy widget to apply layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def get_countries(self):
        #Make the GET request
        response = requests.get('https://www.apicountries.com/countries')

        #Get the JSON data
        countries_data = response.json()

        #Strip names into a list
        country_names = []
        for country in countries_data:
            name = country.get("name")
            country_names.append(name.strip())

        #Populate the combo box with the country names list
        self.myComboBox.clear()
        self.myComboBox.addItems(country_names)


    def handle_country_text_changed(self, country):
        self.myLabel.setText(country)
