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

import pyairtable
from pyairtable.formulas import match
from datetime import date
from slack_sdk import WebClient


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
chrome_profile_path = "/Default"
chrome_options.add_argument("--user-data-dir=" + chrome_profile_path)
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
        username_input.send_keys("hammedfree@gmail.com")
        sleep(1)
        username_input = driver.find_element(By.ID, "login-password")
        username_input.send_keys("Hammedbalo2*")
        sleep(1)
        driver.find_element(By.ID, "login-button").click()
        print("password entered ...")
    except:
        pass
    # Iterate over the requests made by the browser
    sleep(3)
    for request in driver.requests:
        if request.headers:
            if "authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                if auth_header != "":
                    break

    print("Authorization Header:", auth_header)

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
    ("4JoVRTzdITLFtxPx72MaQ5", "SPED UP DRILL GATES"),
    ("4anRsJeihT0h3v3YO2q8wQ", "DRILL GATES"),
    ("3EYY5FwDkHEYLw5V86SAtl", "SICK LEGEND"),
    ("0aUMVkR8QV0LSdv9VZOATn", "TEKKNO"),
    ("4YYOTpMoikKdYWWuTWjbqo", "HYPERTECHNO"),
    ("3nZ3AabGubephVrPTp8rRz", "TECHNO N TEQUILLA"),
    ("2MDj296KJIfgWDNBtHzeFi", "11:11 Music Group"),
    ("6pOqcPiFkbjIKUBF86cfuM", "TWO PUNKS IN LOVE"),
    ("4rlJtMEpxuem6xZ9DPycFD", "RAINY JASPER"),
    ("3vDFmwP5PXRqcAEd9acoNs", "AMBIENT JASPER"),
    ("4KGcll2G3f04WMGTT19eyz", "90210"),
    ("45u4hhyZlr11XAFqO74eTZ", "DEADBOY"),
]

# Get today's date
today = date.today()

api_key = "keyPTU7Oyav6HW5aK"
base_id = "app4ZilmoeAnakNee"
table_name = "Competitor"

airtable = pyairtable.Table(api_key, base_id, table_name)
codes = [
    "WS",
    "PG",
    "TL",
    "SB",
    "NR",
    "KI",
    "TO",
    "NZ",
    "FJ",
    "VU",
    "PW",
    "TV",
    "AU",
    "FM",
    "MH",
    "MO",
    "MN",
    "TW",
    "JP",
    "KR",
    "HK",
    "VN",
    "MY",
    "KH",
    "LA",
    "PH",
    "BN",
    "SG",
    "TH",
    "ID",
    "BR",
    "MX",
    "CR",
    "SV",
    "PA",
    "HN",
    "BZ",
    "NI",
    "GT",
    "DO",
    "DM",
    "KN",
    "JM",
    "GY",
    "BS",
    "VC",
    "TT",
    "GD",
    "SR",
    "LC",
    "AG",
    "HT",
    "BB",
    "CW",
    "CL",
    "AR",
    "UY",
    "PY",
    "CO",
    "EC",
    "PE",
    "BO",
    "VE",
    "BT",
    "NP",
    "IN",
    "MV",
    "BD",
    "LK",
    "PK",
    "BF",
    "LR",
    "CD",
    "GN",
    "SL",
    "ZW",
    "UG",
    "CI",
    "GM",
    "SZ",
    "MZ",
    "ZA",
    "BJ",
    "GW",
    "TZ",
    "CM",
    "MR",
    "GQ",
    "TD",
    "BI",
    "AO",
    "RW",
    "MU",
    "NA",
    "GH",
    "GA",
    "KE",
    "SN",
    "SC",
    "CV",
    "ZM",
    "NE",
    "BW",
    "ML",
    "ST",
    "KM",
    "NG",
    "CG",
    "LS",
    "MG",
    "TG",
    "ET",
    "MW",
    "LY",
    "MA",
    "LB",
    "QA",
    "KW",
    "DZ",
    "OM",
    "IQ",
    "DJ",
    "TN",
    "JO",
    "AE",
    "EG",
    "PS",
    "SA",
    "BH",
    "CA",
    "US",
    "DK",
    "FI",
    "IS",
    "NO",
    "SE",
    "PL",
    "LT",
    "UA",
    "BG",
    "EE",
    "RO",
    "SK",
    "HR",
    "HU",
    "ME",
    "CZ",
    "SI",
    "XK",
    "AL",
    "MK",
    "LV",
    "RS",
    "BA",
    "GB",
    "IE",
    "ES",
    "CY",
    "SM",
    "IL",
    "GR",
    "MT",
    "AD",
    "PT",
    "TR",
    "IT",
    "LU",
    "FR",
    "MC",
    "NL",
    "BE",
    "DE",
    "LI",
    "AT",
    "CH",
    "GE",
    "UZ",
    "BY",
    "TJ",
    "KG",
    "AM",
    "KZ",
    "MD",
    "AZ",
]
