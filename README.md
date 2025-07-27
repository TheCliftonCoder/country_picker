# Country Picker

A GUI application for selecting countries with data fetched from an external API.

## Features
- Fetches country data from API in background thread
- Displays how many countries were successfully loaded
- Provides a dropdown menu of countries 
- Displays selected country

## Requirements

- Python 3.8 or higher
- Internet connection (for fetching country data)

## Installation & Setup

**Clone or download the project:**

git clone https://github.com/TheCliftonCoder/country_picker.git

**Create conda environment:**

conda create -n country_picker python=3.9

conda activate country_picker

**Install dependencies:**

conda install pyside6 requests


Alternatively a requirements .txt is provided for installation through pip.

## Usage

python -m country_picker

## Run tests

pytest

