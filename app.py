import sys

from PySide6.QtCore import Qt
import requests
import json
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QComboBox
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Country Picker")

        layout = QVBoxLayout()
        my_list = ["this", "is", "my", "list"]
        self.myComboBox = QComboBox()
        self.myLabel = QLabel("HELLLLLOOOOO")
        self.myComboBox.addItems(my_list)
        self.myComboBox.currentTextChanged.connect(self.handle_country_text_changed)
        layout.addWidget(self.myComboBox)
        layout.addWidget(self.myLabel)

        #dummy widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Make the GET request
        response = requests.get('https://www.apicountries.com/countries')

        # Get the JSON data
        countries_data = response.json()
        country_names = []
        for country in countries_data:
            name = country.get("name")
            country_names.append(name.strip())

        #with open('countries_parsed.txt', 'w', encoding='utf-8') as file:
            #file.write('\n'.join(country_names))
        
        #country names loaded emit signal for callback to populate combobox
        self.myComboBox.clear()
        self.myComboBox.addItems(country_names)


        '''with open('countries_raw.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)

        with open('countries.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=2, ensure_ascii=False)
        '''
        #after the window has launched populate the QCombo box with hard coded data 
        #then work out how to populate the combobox using an api call

    def handle_country_text_changed(self, country):
        self.myLabel.setText(country)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()