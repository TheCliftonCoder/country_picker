'''
Test case for the JSON parsing logic
'''
import pytest
from country_picker.json_parser import parse_country_names, get_country_names

def test_parse_country_names_basic():
    #Test basic country name parsing
    sample_data = [
        {"name": "United States", "capital": "Washington"},
        {"name": "Canada", "capital": "Ottawa"},
        {"name": "Mexico", "capital": "Mexico City"}
    ]
    
    result = parse_country_names(sample_data)
    expected = ["Canada", "Mexico", "United States"]  #Sorted
    assert result == expected

def test_parse_country_names_with_whitespace():
    #Test that whitespace is stripped
    sample_data = [
        {"name": "  United States  "},
        {"name": "\tCanada\n"}
    ]
    
    result = parse_country_names(sample_data)
    expected = ["Canada", "United States"]
    assert result == expected

def test_parse_country_names_missing_data():
    #Test handling of missing or invalid names
    sample_data = [
        {"name": "Valid Country"},
        {"name": ""},  #Empty string
        {"name": None},  #None value
        {"capital": "No Name"},  #Missing name key
    ]
    
    result = parse_country_names(sample_data)
    expected = ["Valid Country"]
    assert result == expected