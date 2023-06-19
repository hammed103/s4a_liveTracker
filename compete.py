
import requests
import pygsheets
from time import sleep
gc = pygsheets.authorize(
    service_file="./my-project-1515950162194-ea018b910e23.json"
)

# Open the Excel sheet by its name
sh = gc.open("Competitors")
# Find the title row

wks = sh.worksheet_by_title("TAZZY")

late =wks.get_row(1)

late = [i for i in late if i != ""][2:]
print(late[0])
for idx,j in enumerate(late) :

  # Define the URL to send the POST request to
  url = 'http://tracker.purpledorm.io:8000/api/upload-audio'

  # Define the JSON body
  data = {
      "aid": f"{j}",
      "sheetName":"TAZZY"
  }
  # Send the POST request with the JSON body
  response = requests.post(url, json=data)

  # Check the response
  if (response.status_code == 200) | (response.status_code == 201) :
      print("POST request successful")
  else:
      
      print("POST request failed with status code:", response.status_code)
      
  print(idx)  
  sleep(5)
print('11:11')
wks = sh.worksheet_by_title("11:11")

late =wks.get_row(1)

late = [i for i in late if i != ""][2:]
for idx,j in enumerate(late) :

  # Define the URL to send the POST request to
  url = 'http://tracker.purpledorm.io:8000/api/upload-audio'

  # Define the JSON body
  data = {
      "aid": f"{j}",
      "sheetName":"11:11"
  }

  # Send the POST request with the JSON body
  response = requests.post(url, json=data)

  # Check the response
  if (response.status_code == 200) | (response.status_code == 201) :
      print("POST request successful")
  else:
      
      print("POST request failed with status code:", response.status_code)
      

  print(idx)
  sleep(5)
