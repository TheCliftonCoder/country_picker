
"""
GUI module for the Country Picker application.

This module contains the main window and background thread classes for
displaying and managing country selection interface.
"""

import sys
from typing import List, Optional

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
    """Background thread for loading country data from API"""
    
    #Signals to be picked up by the main thread
    countries_loaded = Signal(list)  #Emits list of country names
    error_occurred = Signal(str)     #Emits error message
    
    def run(self)-> None:
        '''Execute the thread's main work - fetch countries from API.'''
        try:
            country_names = get_country_names()
            self.countries_loaded.emit(country_names)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    '''
    Main application window for the Country Picker.
    Provides a GUI interface with a dropdown for selecting countries and
    labels for displaying status and selection information. Handles country
    data loading in a background thread to keep the UI responsive.
    '''
    def __init__(self) -> None:
        '''
        Initialize the main window.
        '''
        super().__init__()
        self.country_thread = None
        self.setup_ui()

    def setup_ui(self) -> None:
        '''
        Sets up the main window layout with a country selection dropdown,
        status labels, and connects signal handlers.
        '''

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
    
    def get_countries(self) -> None:
        ''' 
        Initiate country data loading in a background thread.
        
        Sets up loading UI state and starts a background thread to fetch
        country data from the API. Updates the UI to show loading status
        and connects thread signals to appropriate handlers.
        '''
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

    def handle_countries_loaded(self, country_names: List[str]) -> None:
        '''
        Handle successful country data loading.
        
        Called when the background thread successfully loads country data.
        Updates the UI to display the loaded countries in the dropdown
        and shows a success message.
        '''
        self.myComboBox.clear()
        self.myComboBox.addItems(country_names)
        self.myLoadingLabel.setText(f"Loaded {len(country_names)} countries.")

    def handle_country_download_error(self, error_message: str) -> None:
        '''
        Handle country data loading errors.
        
        Called when the background thread encounters an error while loading
        country data. Updates the UI to show an error state and display
        the error message to the user.
        '''
        self.myComboBox.clear()
        self.myComboBox.addItems(["Error loading countries"])
        self.myLoadingLabel.setText(f"Error: {error_message}")

    def handle_country_text_changed(self, country: str) -> None:
        '''
        Handle country selection changes in the dropdown.
        
        Called whenever the user selects a different country from the
        dropdown menu. Updates the selection label to show the currently
        selected country.
        '''
        if country and country not in ["Loading countries...", "Error loading countries"]:
            self.myLabel.setText(f"Selected: {country}")
