import requests

def fetch_data(url: str) -> str:
    """Fetches data from a given URL."""
    response = requests.get(url)
    return response.text

def main():
    """Entry point for command-line usage."""
    print("This is the command-line entry point!")
