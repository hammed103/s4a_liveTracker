from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response

#####################################
import json
import os
import requests
import base64
import io
from urllib.parse import urlparse
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import pygsheets
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter

from datetime import date, timedelta


# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wirewebdriver
from selenium.webdriver.chrome.service import Service

# Find the login input box by its ID and enter the login credentials
from selenium.webdriver.common.by import By

service = Service(executable_path="chromedriver")

options = {
    "verify_ssl": True  # Verify SSL certificates but beware of errors with self-signed certificates
}

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#chrome_profile_path = "/Default"
chrome_options.add_argument("--user-data-dir=Default")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# extract artist id
def extract_artist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("artist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


# extract playlist id
def extract_playlist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("playlist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


# column name to numbers
def colnum_to_colname(colnum):
    colname = ""
    while colnum > 0:
        colnum, remainder = divmod(colnum - 1, 26)
        colname = chr(65 + remainder) + colname
    return colname


# soup from html
def soup_from_html(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    return soup



def login(driver):
    try:
        username_input = driver.find_element(By.ID, "login-username")
        username_input.send_keys("x@1111.io")
        sleep(1)
        username_input = driver.find_element(By.ID, "login-password")
        username_input.send_keys("Speedbumps123@@_121!_!3")
        sleep(2)
        driver.find_element(By.ID, "login-button").click()
        print("password entered ...")
        sleep(8)

    except:
        pass
    # Iterate over the requests made by the browser
    sleep(8)
    for request in driver.requests:
        
        if request.headers:
            #print("l")
            if "authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                if auth_header != "":
                    break
    try:
      print("Authorization Header:", auth_header)
    except:
       auth_header = "Bearer BQAfYIl5ZI2sewqgpi8ap4rP_GUe5FE4yeOcsC0ukzBbgEYg5uHEGLKNh7zDjg5ewokWUy-pioowLp4LWN-zRtqVC8mq_IE0jfmlJZB1ktlIoYH_TapzbsdgIbUfDecTvjkC-Ty5ugrj-GeipHCmXhq7ZtHeA6_Xr9trTErSRApdnq2_HGppokqMFPvfUQp_65cnRJ97JZsx75gVB4wP2_8l"

    return auth_header


def reload_auth(driver):
    for request in driver.requests:
        if request.headers:
            if "authorization" in request.headers:
                lam = request.headers["Authorization"]
                if lam != "":
                    auth_header = lam

    print("Authorization Header:", auth_header)

    return auth_header


def vio(playlist_id):
    client_id = "53fb1dbe5f42480ba654fcc3c7e168d6"
    client_secret = "5c1da4cce90f410e88966cdfc0785e3a"

    auth_str = client_id + ":" + client_secret
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    auth_options = {
        "url": "https://accounts.spotify.com/api/token",
        "headers": {"Authorization": "Basic " + b64_auth_str},
        "data": {"grant_type": "client_credentials"},
    }

    response = requests.post(**auth_options)
    if response.status_code == 200:
        token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}  # Replace with actual token

    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers
    )

    if response.status_code == 200:
        playlist_data = response.json()
        # Do something with the playlist data
    else:
        print(f"Error: {response.status_code}")

    cnt = (playlist_data["followers"]["total"], playlist_data["name"])

    return {
        "id": playlist_id,
        "name": playlist_data["name"],
        "total": playlist_data["followers"]["total"],
    }


from datetime import datetime

def get_day_of_week(date_string):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Return the day of the week
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    return days[date_obj.weekday()]


def header(auth_header):
    headers = {
        "authority": "generic.wg.spotify.com",
        "accept": "application/json",
        "accept-language": "en-US",
        "app-platform": "Browser",
        "authorization": f"{auth_header}",
        "content-type": "application/json",
        "origin": "https://artists.spotify.com",
        "referer": "https://artists.spotify.com/",
        "sec-ch-ua": '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "spotify-app-version": "1.0.0.48e3603",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "x-cloud-trace-context": "00000000000000002a87751b4619e7dc/1588903106916990606;o=1",
    }

    return headers


art = [
    #("4JoVRTzdITLFtxPx72MaQ5", "SPED UP DRILL GATES"),
   # ("4anRsJeihT0h3v3YO2q8wQ", "DRILL GATES"),
    ("3EYY5FwDkHEYLw5V86SAtl", "SICK LEGEND"),
    ("0aUMVkR8QV0LSdv9VZOATn", "TEKKNO"),
    ("4YYOTpMoikKdYWWuTWjbqo", "HYPERTECHNO"),
    ("3nZ3AabGubephVrPTp8rRz", "TECHNO N TEQUILLA"),
    ("2MDj296KJIfgWDNBtHzeFi", "11:11 Music Group"),
    ("6pOqcPiFkbjIKUBF86cfuM", "TWO PUNKS IN LOVE"),
    ("4rlJtMEpxuem6xZ9DPycFD", "RAINY JASPER"),
    ("3vDFmwP5PXRqcAEd9acoNs", "AMBIENT JASPER"),
    #("4KGcll2G3f04WMGTT19eyz", "90210"),
    ("45u4hhyZlr11XAFqO74eTZ", "DEADBOY"),
]

# Get today's date
today = date.today()


import pandas as pd
countries = [
    ("","Worldwide"),
    ("WS", "Samoa"),
    ("PG", "Papua New Guinea"),
    ("TL", "Timor-Leste"),
    ("SB", "Solomon Islands"),
    ("NR", "Nauru"),
    ("KI", "Kiribati"),
    ("TO", "Tonga"),
    ("NZ", "New Zealand"),
    ("FJ", "Fiji"),
    ("VU", "Vanuatu"),
    ("PW", "Palau"),
    ("TV", "Tuvalu"),
    ("AU", "Australia"),
    ("FM", "Micronesia"),
    ("MH", "Marshall Islands"),
    ("MO", "Mongolia"),
    ("MN", "Mongolia"),
    ("TW", "Taiwan"),
    ("JP", "Japan"),
    ("KR", "South Korea"),
    ("HK", "Hong Kong"),
    ("VN", "Vietnam"),
    ("MY", "Malaysia"),
    ("KH", "Cambodia"),
    ("LA", "Laos"),
    ("PH", "Philippines"),
    ("BN", "Brunei"),
    ("SG", "Singapore"),
    ("TH", "Thailand"),
    ("ID", "Indonesia"),
    ("BR", "Brazil"),
    ("MX", "Mexico"),
    ("CR", "Costa Rica"),
    ("SV", "El Salvador"),
    ("PA", "Panama"),
    ("HN", "Honduras"),
    ("BZ", "Belize"),
    ("NI", "Nicaragua"),
    ("GT", "Guatemala"),
    ("DO", "Dominican Republic"),
    ("DM", "Dominica"),
    ("KN", "Saint Kitts and Nevis"),
    ("JM", "Jamaica"),
    ("GY", "Guyana"),
    ("BS", "Bahamas"),
    ("VC", "Saint Vincent and the Grenadines"),
    ("TT", "Trinidad and Tobago"),
    ("GD", "Grenada"),
    ("SR", "Suriname"),
    ("LC", "Saint Lucia"),
    ("AG", "Antigua and Barbuda"),
    ("HT", "Haiti"),
    ("BB", "Barbados"),
    ("CW", "Curacao"),
    ("CL", "Chile"),
    ("AR", "Argentina"),
    ("UY", "Uruguay"),
    ("PY", "Paraguay"),
    ("CO", "Colombia"),
    ("EC", "Ecuador"),
    ("PE", "Peru"),
    ("BO", "Bolivia"),
    ("VE", "Venezuela"),
    ("BT", "Bhutan"),
    ("NP", "Nepal"),
    ("IN", "India"),
    ("MV", "Maldives"),
    ("BD", "Bangladesh"),
    ("LK", "Sri Lanka"),
    ("PK", "Pakistan"),
    ("BF", "Burkina Faso"),
    ("LR", "Liberia"),
    ("CD", "Democratic Republic of the Congo"),
    ("GN", "Guinea"),
    ("SL", "Sierra Leone"),
    ("ZW", "Zimbabwe"),
    ("UG", "Uganda"),
    ("CI", "Ivory Coast"),
    ("GM", "Gambia"),
    ("SZ", "Eswatini"),
    ("MZ", "Mozambique"),
    ("ZA", "South Africa"),
    ("BJ", "Benin"),
    ("GW", "Guinea-Bissau"),
    ("TZ", "Tanzania"),
    ("CM", "Cameroon"),
    ("MR", "Mauritania"),
    ("GQ", "Equatorial Guinea"),
    ("TD", "Chad"),
    ("BI", "Burundi"),
    ("AO", "Angola"),
    ("RW", "Rwanda"),
    ("MU", "Mauritius"),
    ("NA", "Namibia"),
    ("GH", "Ghana"),
    ("GA", "Gabon"),
    ("KE", "Kenya"),
    ("SN", "Senegal"),
    ("SC", "Seychelles"),
    ("CV", "Cape Verde"),
    ("ZM", "Zambia"),
    ("NE", "Niger"),
    ("BW", "Botswana"),
    ("ML", "Mali"),
    ("ST", "Sao Tome and Principe"),
    ("KM", "Comoros"),
    ("NG", "Nigeria"),
    ("CG", "Republic of the Congo"),
    ("LS", "Lesotho"),
    ("MG", "Madagascar"),
    ("TG", "Togo"),
    ("ET", "Ethiopia"),
    ("MW", "Malawi"),
    ("LY", "Libya"),
    ("MA", "Morocco"),
    ("LB", "Lebanon"),
    ("QA", "Qatar"),
    ("KW", "Kuwait"),
    ("DZ", "Algeria"),
    ("OM", "Oman"),
    ("IQ", "Iraq"),
    ("DJ", "Djibouti"),
    ("TN", "Tunisia"),
    ("JO", "Jordan"),
    ("AE", "United Arab Emirates"),
    ("EG", "Egypt"),
    ("PS", "Palestine"),
    ("SA", "Saudi Arabia"),
    ("BH", "Bahrain"),
    ("CA", "Canada"),
    ("US", "United States"),
    ("DK", "Denmark"),
    ("FI", "Finland"),
    ("IS", "Iceland"),
    ("NO", "Norway"),
    ("SE", "Sweden"),
    ("PL", "Poland"),
    ("LT", "Lithuania"),
    ("UA", "Ukraine"),
    ("BG", "Bulgaria"),
    ("EE", "Estonia"),
    ("RO", "Romania"),
    ("SK", "Slovakia"),
    ("HR", "Croatia"),
    ("HU", "Hungary"),
    ("ME", "Montenegro"),
    ("CZ", "Czech Republic"),
    ("SI", "Slovenia"),
    ("XK", "Kosovo"),
    ("AL", "Albania"),
    ("MK", "North Macedonia"),
    ("LV", "Latvia"),
    ("RS", "Serbia"),
    ("BA", "Bosnia and Herzegovina"),
    ("GB", "United Kingdom"),
    ("IE", "Ireland"),
    ("ES", "Spain"),
    ("CY", "Cyprus"),
    ("SM", "San Marino"),
    ("IL", "Israel"),
    ("GR", "Greece"),
    ("MT", "Malta"),
    ("AD", "Andorra"),
    ("PT", "Portugal"),
    ("TR", "Turkey"),
    ("IT", "Italy"),
    ("LU", "Luxembourg"),
    ("FR", "France"),
    ("MC", "Monaco"),
    ("NL", "Netherlands"),
    ("BE", "Belgium"),
    ("DE", "Germany"),
    ("LI", "Liechtenstein"),
    ("AT", "Austria"),
    ("CH", "Switzerland"),
    ("GE", "Georgia"),
    ("UZ", "Uzbekistan"),
    ("BY", "Belarus"),
    ("TJ", "Tajikistan"),
    ("KG", "Kyrgyzstan"),
    ("AM", "Armenia"),
    ("KZ", "Kazakhstan"),
    ("MD", "Moldova"),
    ("AZ", "Azerbaijan")
]




def retro(auth_header,ttname,id,driver):
  
  canalz = []

  headers = {
      'authority': 'generic.wg.spotify.com',
      'accept': 'application/json',
      'accept-language': 'en-US',
      'app-platform': 'Browser',
      'authorization': f'{auth_header}',
      'content-type': 'application/json',
      'grpc-timeout': '10S',
      'origin': 'https://artists.spotify.com',
      'referer': 'https://artists.spotify.com/',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'spotify-app-version': '1.0.0.9ac0ee2',
      'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0',
  }



  for code, name in countries :
    #print(code)
    params = {
        'country': f'{code}',
        'from_date': str(date.today() - timedelta(28)) ,
        'to_date': str(date.today() ),
    }
    try:

      response = requests.get(
      f'https://generic.wg.spotify.com/audience-engagement-view/v1/artist/{id}/stats',
      params=params,
      headers=headers,
      )
      dt = response.json()
      dt["streams"]
    except:
      print(dt)
      print("try again")
      auth_header = reload_auth(driver)
      
      headers = {
      'authority': 'generic.wg.spotify.com',
      'accept': 'application/json',
      'accept-language': 'en-US',
      'app-platform': 'Browser',
      'authorization': f'{auth_header}',
      'content-type': 'application/json',
      'origin': 'https://artists.spotify.com',
      'referer': 'https://artists.spotify.com/',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'spotify-app-version': '1.0.0.9ac0ee2',
      'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0',
        }

      response = requests.get(
      f'https://generic.wg.spotify.com/audience-engagement-view/v1/artist/{id}/stats',
      params=params,
      headers=headers,
      )
      dt = response.json()
    #print(dt)
    stre = pd.DataFrame(dt["streams"]["current_period_timeseries"],)

    #return stre
    try:
      stre.columns = ["Date","Streams"]
    except:
      continue


    lst = pd.DataFrame(dt["listeners"]["current_period_timeseries"],)

    lst.columns = ["Date","listeners"]


    stre_lst = pd.DataFrame(dt["streams_per_listener"]["current_period_timeseries"],)
    try:
      stre_lst.columns = ["Date","streams_per_listener"]
    except:
      stre["streams_per_listener"] = 0


    play = pd.DataFrame(dt["playlist_adds"]["current_period_timeseries"],)
    try:
      play.columns = ["Date","playlist_adds"]
    except:
      stre["playlist_adds"] = 0


    save = pd.DataFrame(dt["saves"]["current_period_timeseries"],)
    try:
      save.columns = ["Date","saves"]
    except:
      stre["saves"] = 0

    followers = pd.DataFrame(dt["followers"]["current_period_timeseries"],)
    try:
      followers.columns = ["Date","followers"]
    except:
      stre["followers"] = 0


    # Combine DataFrames using the 'Date' column
    merged_df = pd.merge(stre, lst, on='Date', how='outer')
    try:
      merged_df = pd.merge(merged_df, stre_lst, on='Date', how='outer')
    except:
      pass
    try:
      merged_df = pd.merge(merged_df, play, on='Date', how='outer')
    except:
      pass
    try:
      merged_df = pd.merge(merged_df, save, on='Date', how='outer')
    except:
      pass

    try:
      merged_df = pd.merge(merged_df, followers, on='Date', how='outer')
    except:
      pass
    merged_df["country"] = name


    canalz.append(merged_df)



  baller = pd.concat(canalz)
  print(baller.shape)

  bind = []
  headers = {
      'authority': 'generic.wg.spotify.com',
      'accept': 'application/json',
      'accept-language': 'en-US',
      'app-platform': 'Browser',
      'authorization': f'{auth_header}',
      'content-type': 'application/json',
      'origin': 'https://artists.spotify.com',
      'referer': 'https://artists.spotify.com/',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'spotify-app-version': '1.0.0.9ac0ee2',
      'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0',
  }
  for cd,name in countries:
    params = {
        'country': f'{cd}',
    }

    response = requests.get(
        f'https://generic.wg.spotify.com/fanatic-audience-segments/v0/artist/{id}/segments',
        params=params,
        headers=headers,
    )

    if response.text == "Token expired":
       auth_header = reload_auth(driver)
       headers = {
        'authority': 'generic.wg.spotify.com',
        'accept': 'application/json',
        'accept-language': 'en-US',
        'app-platform': 'Browser',
        'authorization': f'{auth_header}',
        'content-type': 'application/json',
        'origin': 'https://artists.spotify.com',
        'referer': 'https://artists.spotify.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'spotify-app-version': '1.0.0.9ac0ee2',
        'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0',
            }
       response = requests.get(
            f'https://generic.wg.spotify.com/fanatic-audience-segments/v0/artist/{id}/segments',
            params=params,
            headers=headers,
        )

    moot = pd.DataFrame(response.json()["segmentCountsTimeline"])

    moot["country"] = name

    bind.append(moot)

  brood = pd.concat(bind)
  brood = brood.sort_values('date')
  brood = brood.rename(columns ={"date":"Date"})
  blow = pd.merge(brood, baller, on=['Date','country'], how='outer')

  blow["active"]
  expanded_blow = pd.json_normalize(blow['active'])
  blow = pd.concat([blow.drop('active', axis=1), expanded_blow], axis=1)
  #print(blow)

  blow = blow.rename(columns = {'total':"total_active_audience"})
  blow.head()
  blow["artist_id"] = f"{id}"
  blow["artist_name"] = f"{ttname}"
  print(ttname)
  return auth_header,blow







import re

def lapdog(webpage_text):
    # Define a regular expression pattern to extract video sections between the first occurrence of videoLockup and the next
    video_section_pattern = r'videoLockup":{"compactVideoRenderer":(.*?)(?=\},\{"videoLockup":"|$)'

    # Define the pattern to find occurrences of "videoLockup":{"compactVideoRenderer":
    pattern = r'(?="videoLockup":{"compactVideoRenderer":)'

    # Split the text using the pattern
    video_sections = re.split(pattern, webpage_text)

    # Initialize lists to store the extracted information
    results = {}

    # Define regular expressions to extract the relevant information within each video section
    title_pattern = r'"title":{"simpleText":"([^"]+)"'
    artist_pattern = r'"ARTIST"},"defaultMetadata":{"simpleText":"([^"]+)"'
    album_pattern = r'"ALBUM"},"defaultMetadata":{"simpleText":"([^"]+)"'
    licenses_pattern = r'"LICENSES"},"expandedMetadata":{"simpleText":"([^"]+)"'

    # Iterate through each video section and extract the information
    for i, video_section in enumerate(video_sections[1:], start=1):
        title_match = re.search(title_pattern, video_section)

        if title_match.group(1) == "ARTIST":
            title_match = re.search(r'"title":{"runs":\[\{"text":"([^"]+)"', video_section)

        artist_match = re.search(artist_pattern, video_section)
        if not artist_match :
          artist_pattern = r'"ARTIST"},"defaultMetadata":{"runs":\[\{"text":"([^"]+)"'
          artist_match = re.search(artist_pattern, video_section)

        album_match = re.search(album_pattern, video_section)
        licenses_match = re.search(licenses_pattern, video_section)

        # Extract the information if found and add to the results dictionary
        results[f'song{i}'] = title_match.group(1) if title_match else None
        results[f'artist{i}'] = artist_match.group(1) if artist_match else None
        results[f'album{i}'] = album_match.group(1) if album_match else None
        results[f'licenses{i}'] = licenses_match.group(1) if licenses_match else None

    return results

###########################
import datetime
from googleapiclient.discovery import build




def search_videos(API_KEY,keyword, max_duration, time_filter,COUNTRY_CODE):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    search_response = youtube.search().list(
        q=keyword,
        type='video',
        order='viewCount',  # Sort by view count
        videoDuration='short',
        videoDefinition='high',
        publishedAfter=time_filter[0].isoformat() + 'T00:00:00Z',
        maxResults=100,
        regionCode=COUNTRY_CODE,  # Add the country code
        part='id'
    ).execute()

    video_ids = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]

    videos = []

    for video_id in video_ids:
        video_response = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        ).execute()

        video_info = video_response['items'][0]
        video_title = video_info['snippet']['title']
        channel_title = video_info['snippet']['channelTitle']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        channel_url = f'https://www.youtube.com/channel/{video_info["snippet"]["channelId"]}'
        view_count = video_info['statistics']['viewCount']
        try:
          like_count = video_info['statistics']['likeCount']
        except:
          like_count = 0
        publish_date = video_info['snippet']['publishedAt']

        videos.append({
            'video_title': video_title,
            'channel_title': channel_title,
            'video_url': video_url,
            'channel_url': channel_url,
            'view_count': view_count,
            'like_count': like_count,
            'publish_date': publish_date
        })

    return videos





def get_date_range(time_range):
    today = datetime.date.today()

    if time_range == "last30days":
        start_date = today - datetime.timedelta(days=30)
    elif time_range == "last7days":
        start_date = today - datetime.timedelta(days=7)
    elif time_range == "last24hrs":
        start_date = today - datetime.timedelta(hours=24)
    else:
        # Default to "last30days" if an invalid time_range is provided
        start_date = today - datetime.timedelta(days=30)

    return start_date, today



import requests
import re
import datetime
import pandas as pd

def search_and_extract_info(API_KEY,keyword, max_duration, time_filterz,COUNTRY_CODE):
    time_filter = get_date_range(time_filterz)
    # Perform video search (Replace with your actual search function)
    videos = search_videos(API_KEY,keyword, max_duration, time_filter,COUNTRY_CODE)

    data = []

    for video in videos:
        ll = requests.get(video['video_url'])
        webpage_text = ll.text

        # Define regular expressions to extract the relevant information
        song_pattern = r'"title":{"simpleText":"SONG"},"defaultMetadata":{"runs":\[{"text":"([^"]+)"'
        artist_pattern = r'"title":{"simpleText":"ARTIST"},"defaultMetadata":{"runs":\[{"text":"([^"]+)"'
        album_pattern = r'"title":{"simpleText":"ALBUM"},"defaultMetadata":{"simpleText":"([^"]+)"'
        licenses_pattern = r'"title":{"simpleText":"LICENSES"},"expandedMetadata":{"simpleText":"([^"]+)"'
        den = lapdog(webpage_text)
        if den:
            song = den.get('song1')
            artist = den.get('artist1')
            album = den.get('album1')
            licenses = den.get('licenses1')

            # Extract information for the second iteration (if available)
            try:
                song2 = den.get('song2')
                artist2 = den.get('artist2')
                album2 = den.get('album2')
                licenses2 = den.get('licenses2')
            except KeyError:
                song2 = artist2 = album2 = licenses2 = None

            # Extract information for the third iteration (if available)
            try:
                song3 = den.get('song3')
                artist3 = den.get('artist3')
                album3 = den.get('album3')
                licenses3 = den.get('licenses3')
            except KeyError:
                song3 = artist3 = album3 = licenses3 = None

        else :
            song3 = artist3 = album3 = licenses3 = None
            song2 = artist2 = album2 = licenses2 = None
            # Use regular expressions to find and extract the information
            song_match = re.search(song_pattern, webpage_text)
            if not song_match:
                song_pattern = r'"title":{"simpleText":"SONG"},"defaultMetadata":{"simpleText":"([^"]+)"'
                song_match = re.search(song_pattern, webpage_text)

            artist_match = re.search(artist_pattern, webpage_text)
            if not artist_match:
                artist_pattern = r'"title":{"simpleText":"ARTIST"},"defaultMetadata":{"simpleText":"([^"]+)"'
                artist_match = re.search(artist_pattern, webpage_text)
            album_match = re.search(album_pattern, webpage_text)
            licenses_match = re.search(licenses_pattern, webpage_text)

            # Extract the information if found
            song = song_match.group(1) if song_match else None
            artist = artist_match.group(1) if artist_match else None
            album = album_match.group(1) if album_match else None
            licenses = licenses_match.group(1) if licenses_match else None

        # Append the extracted information to the data list
        data.append({
            'Video Title': video['video_title'],
            'Channel Title': video['channel_title'],
            'Video URL': video['video_url'],
            'SONG': song,
            'ARTIST': artist,
            'ALBUM': album,
            'LICENSES': licenses,
            'SONG2': song2,
            'ARTIST2': artist2,
            'ALBUM2': album2,
            'LICENSES2': licenses2,
            'Channel URL': video['channel_url'],
            'View Count': video['view_count'],
            'Like Count': video['like_count'],
            'Publish Date': video['publish_date']
        })

    # Create a Pandas DataFrame from the extracted data
    df = pd.DataFrame(data)
    df = df.reset_index()
    df["tag"] = keyword
    df["country"] = COUNTRY_CODE
    df["Date"] = time_filter[1]
    df["Date_Range"] = time_filterz

    return df


