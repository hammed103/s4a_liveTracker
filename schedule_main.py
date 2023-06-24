import requests

url = "http://tracker.purpledorm.io:8000/api/refreshMain"

response = requests.get(url)

if response.status_code == 200:
    print("GET request successful")
    # Process the response data here if needed
else:
    print("GET request failed with status code:", response.status_code)
