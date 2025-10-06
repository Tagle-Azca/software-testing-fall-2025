# -*- coding: utf-8 -*-
"""
Source code for mock up testing examples.
"""
import subprocess
import time
import requests
from unittest.mock import Mock, patch, mock_open


def fetch_data_from_api(url):
    """Fetches data from an external API using the requests library."""
    response = requests.get(url, timeout=10)
    return response.json()


def test_fetch_data_from_api():
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    
    with patch('requests.get', return_value=mock_response):
        result = fetch_data_from_api("http://example.com/api")
        assert result == {"key": "value"}
    
    mock_response.json.return_value = {"data": [1, 2, 3]}
    with patch('requests.get', return_value=mock_response):
        result = fetch_data_from_api("http://api.test.com")
        assert result == {"data": [1, 2, 3]}
    
    mock_response.json.return_value = {}
    with patch('requests.get', return_value=mock_response):
        result = fetch_data_from_api("http://empty.com")
        assert result == {}


def read_data_from_file(filename):
    """Read data from a file."""
    try:
        with open(filename, encoding="utf-8") as file:
            data = file.read()
        return data
    except FileNotFoundError as e:
        raise e


def test_read_data_from_file():
    with patch('builtins.open', mock_open(read_data="test content")):
        result = read_data_from_file("test.txt")
        assert result == "test content"
    
    with patch('builtins.open', mock_open(read_data="line1\nline2\nline3")):
        result = read_data_from_file("data.txt")
        assert result == "line1\nline2\nline3"
    
    with patch('builtins.open', mock_open(read_data="")):
        result = read_data_from_file("empty.txt")
        assert result == ""
    
    with patch('builtins.open', side_effect=FileNotFoundError):
        try:
            read_data_from_file("nonexistent.txt")
            assert False
        except FileNotFoundError:
            assert True


def execute_command(command):
    """Execute a command in a subprocess."""
    try:
        result = subprocess.run(command, capture_output=True, check=False, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise e


def test_execute_command():
    mock_result = Mock()
    mock_result.stdout = "command output"
    
    with patch('subprocess.run', return_value=mock_result):
        result = execute_command(["echo", "hello"])
        assert result == "command output"
    
    mock_result.stdout = ""
    with patch('subprocess.run', return_value=mock_result):
        result = execute_command(["ls"])
        assert result == ""
    
    mock_result.stdout = "error message"
    with patch('subprocess.run', return_value=mock_result):
        result = execute_command(["invalid"])
        assert result == "error message"
    
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "cmd")):
        try:
            execute_command(["fail"])
            assert False
        except subprocess.CalledProcessError:
            assert True


def perform_action_based_on_time():
    """Perform an action based on the current time."""
    current_time = time.time()
    if current_time < 10:
        return "Action A"
    return "Action B"


def test_perform_action_based_on_time():
    with patch('time.time', return_value=5):
        result = perform_action_based_on_time()
        assert result == "Action A"
    
    with patch('time.time', return_value=9.9):
        result = perform_action_based_on_time()
        assert result == "Action A"
    
    with patch('time.time', return_value=10):
        result = perform_action_based_on_time()
        assert result == "Action B"
    
    with patch('time.time', return_value=1000):
        result = perform_action_based_on_time()
        assert result == "Action B"
    
    with patch('time.time', return_value=0):
        result = perform_action_based_on_time()
        assert result == "Action A"