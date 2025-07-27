from typing import List, Dict, Any
import requests

def fetch_countries_data() -> List[Dict[str, Any]]:
    '''Fetch raw country data from the countries API https://www.apicountries.com/countries'''
    #Make the GET request
    response = requests.get('https://www.apicountries.com/countries')
    #Raise exception 
    response.raise_for_status()
    return response.json()

def parse_country_names(countries_data: List[Dict[str, Any]]) -> List[str]:
    '''Extract and clean country names from raw API data.'''
    country_names = []
    for country in countries_data:
        name = country.get("name")
        if name:  #Check if name exists and is not empty
            country_names.append(name.strip())
    
    return sorted(country_names)  #Sort alphabetically

def get_country_names() -> List[str]:
    ''' Fetches the country data and parses the data into a list that just contains the country names'''
    try:
        data = fetch_countries_data()
        return parse_country_names(data)
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch countries: {e}")