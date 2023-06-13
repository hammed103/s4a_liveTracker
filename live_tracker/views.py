from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response

#####################################
import json
import os
import requests
import io
from urllib.parse import urlparse
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import pygsheets


def extract_artist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("artist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


def extract_playlist_id(url):
    # Split the URL by "/"
    url_parts = url.split("/")

    # Find the index of "artist" in the URL
    artist_index = url_parts.index("playlist")

    # Extract the artist ID
    artist_id = url_parts[artist_index + 1]

    return artist_id


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

# Example usage
slack_token = "xoxb-907605934689-5286686717863-8EN26FvWuun1C8M8ZkUe7uZj"
channel_id = "C05901NKQSY"

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


def colnum_to_colname(colnum):
    colname = ""
    while colnum > 0:
        colnum, remainder = divmod(colnum - 1, 26)
        colname = chr(65 + remainder) + colname
    return colname


def soup_from_html(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    return soup


import pyairtable
from pyairtable.formulas import match
from datetime import date
from slack_sdk import WebClient

# Get today's date
today = date.today()

api_key = "keyPTU7Oyav6HW5aK"
base_id = "app4ZilmoeAnakNee"
table_name = "Competitor"

airtable = pyairtable.Table(api_key, base_id, table_name)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wirewebdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="chromedriver")

options = {
    "verify_ssl": True  # Verify SSL certificates but beware of errors with self-signed certificates
}

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
# chrome_profile_path = "/content/Default"
chrome_options.add_argument("--user-data-dir=Default")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# Create a new instance of ChromeDriver
driver = wirewebdriver.Chrome(
    service=service, options=chrome_options, seleniumwire_options=options
)
# Now you can use the `driver` object to interact with the browser and access the requests made
driver.get("https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home")
sleep(3)
# Find the login input box by its ID and enter the login credentials
from selenium.webdriver.common.by import By

try:
    username_input = driver.find_element(By.ID, "login-username")
    username_input.send_keys("hammedfree@gmail.com")
    sleep(1)
    username_input = driver.find_element(By.ID, "login-password")
    username_input.send_keys("Hammedbalo2*")
    sleep(1)
    driver.find_element(By.ID, "login-button").click()
except:
    pass
# Iterate over the requests made by the browser
for request in driver.requests:
    if request.headers:
        if "authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header != "":
                break

print("Authorization Header:", auth_header)

# %%


import requests
import base64
from time import sleep


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


def HomePage(req):
    return render(
        req,
        "base/index.html",
    )


def Playlist(req):
    return render(
        req,
        "base/play.html",
    )


class UploadView(APIView):
    @staticmethod
    def post(req):
        aid = req.data["aid"]
        try:
            aid = extract_artist_id(aid)
        except:
            pass
        print(aid)
        rff = requests.get(f"https://open.spotify.com/artist/{aid}")

        artistName = soup_from_html(rff.text).find("title").text.split("|")[0]
        airtable = pyairtable.Table(api_key, base_id, table_name)
        global driver
        for request in driver.requests:
            if request.headers:
                if "authorization" in request.headers:
                    auth_header = request.headers["Authorization"]
                    if auth_header != "":
                        break

        print("Authorization Header:", auth_header)
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

        params = {
            "aggregation-level": "recording",
            "time-filter": "last5years",
        }

        response = requests.get(
            f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/streams/{aid}",
            params=params,
            headers=headers,
        )
        try:
            response = response.json()["timelinePoint"][:180]
        except:
            # Create a new instance of ChromeDriver
            driver = wirewebdriver.Chrome(
                service=service, options=chrome_options, seleniumwire_options=options
            )
            # Now you can use the `driver` object to interact with the browser and access the requests made
            driver.get(
                "https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home"
            )
            sleep(3)
            # Find the login input box by its ID and enter the login credentials
            from selenium.webdriver.common.by import By

            try:
                username_input = driver.find_element(By.ID, "login-username")
                username_input.send_keys("hammedfree@gmail.com")
                sleep(1)
                username_input = driver.find_element(By.ID, "login-password")
                username_input.send_keys("Hammedbalo2*")
                sleep(1)
                driver.find_element(By.ID, "login-button").click()
            except:
                pass
            # Iterate over the requests made by the browser
            for request in driver.requests:
                if request.headers:
                    if "authorization" in request.headers:
                        auth_header = request.headers["Authorization"]
                        if auth_header != "":
                            break

            print("Authorization Header:", auth_header)

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

            params = {
                "aggregation-level": "recording",
                "time-filter": "last5years",
            }

            response = requests.get(
                f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/streams/{aid}",
                params=params,
                headers=headers,
            )

            response = response.json()["timelinePoint"]

        key_mapping = {"date": "Date", "num": artistName}

        # Create a new list of dictionaries with renamed keys
        response = [
            {key_mapping.get(key, key): value for key, value in item.items()}
            for item in response
        ]

        # Print the updated list of dictionaries

        # Define the keys to convert from string to integer
        keys_to_convert = [artistName]

        # Convert string values to integers using list comprehension
        response = [
            {
                key: int(value) if key in keys_to_convert else value
                for key, value in item.items()
            }
            for item in response
        ]

        dc = pd.DataFrame(response)
        gc = pygsheets.authorize(
            service_file="./my-project-1515950162194-ea018b910e23.json"
        )

        # Open the Excel sheet by its name
        sh = gc.open("Competitors")

        wks = sh.worksheet_by_title("Competitor-Grid view")
        pt = wks.get_as_df()

        # Merge df1 and df2 on 'Date', and if there are common columns, df2's values will be used
        df = pt.merge(dc, on="Date", how="outer", suffixes=("_y", ""))

        # Delete the columns from df1 which are common with df2
        to_drop = [x for x in df if x.endswith("_y")]
        df.drop(to_drop, axis=1, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"], format="mixed")
        df = df.sort_values("Date", ascending=False)

        df = df.fillna(0)

        num_columns = df.shape[1]

        # Convert the number of columns into a column label
        last_column_label = colnum_to_colname(num_columns)

        df["Total Amount"] = pd.DataFrame(
            [f"=SUM(C{i+2}:{last_column_label}{i+2})" for i in range(wks.rows - 1)],
            columns=["Total Amount"],
        )
        wks.clear()
        wks.set_dataframe(df, start="A1", extend=True)
        try:
            for rr in response:
                records = airtable.first(formula=match({"Date": rr["Date"]}))
                if not records:
                    airtable.create(rr)
                else:
                    record_id = records["id"]
                    updated_fields = rr
                    airtable.update(record_id, rr)
        except:
            pass

        print("Upload complete")

        return Response(
            {
                "status": "success",
                "data": response,
            },
            status=201,
        )
        print("Upload complete")


class UploadPlay(APIView):
    @staticmethod
    def post(req):
        aid = req.data["playid"]
        try:
            data = vio(aid)
        except:
            aid = extract_playlist_id(aid)
        data = vio(aid)
        # Authenticate with Google Sheets
        gc = pygsheets.authorize(
            service_file="my-project-1515950162194-ea018b910e23.json"
        )

        # Open the Google Spreadsheet using its title
        spreadsheet = gc.open("Playlist Tracker")

        # Select the worksheet
        worksheet = spreadsheet.sheet1

        # Add new data

        new_row = [
            data["id"],
            data["name"],
            data["total"],
            0,
        ]  # Assuming Last24Hours is 0 for new rows

        # Add the new row to the end of the sheet
        worksheet.append_table(new_row)

        return Response(
            {
                "status": "success",
                "data": new_row,
            },
            status=201,
        )
        print("Upload complete")


class refresh(APIView):
    @staticmethod
    def get(req):
        gc = pygsheets.authorize(
            service_file="my-project-1515950162194-ea018b910e23.json"
        )

        # Open the Google Spreadsheet using its title
        spreadsheet = gc.open("Playlist Tracker")

        # Select the worksheet
        worksheet = spreadsheet.sheet1

        ll = worksheet.get_as_df()
        for index, val in ll.iterrows():
            data = vio(val.PlaylistId)
            pix = data["total"] - val.Total
            ll.loc[index, "Total"] = data["total"]
            ll.loc[index, "Last24Hours"] = pix

        worksheet.clear()

        worksheet.set_dataframe(ll, start="A1", extend=True)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")


class refreshMain(APIView):
    @staticmethod
    def get(req):
        cont = False
        global driver
        #########  MAIN   ###################################
        for request in driver.requests:
            if request.headers:
                if "authorization" in request.headers:
                    auth_header = request.headers["Authorization"]
                    if auth_header != "":
                        break

        print("Authorization Header:", auth_header)
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

        table_name = "main"  # Replace with your Airtable table name

        artx = art.copy()
        artx.remove(artx[1])
        artx.remove(artx[4])
        params = {
            "aggregation-level": "recording",
            "time-filter": "last5years",
        }
        # Listeners Summary
        for topic in ["listeners", "Streams", "Followers"]:
            table_name = f"{topic} Summary"  # Replace with your Airtable table name

            airtable = pyairtable.Table(api_key, base_id, table_name)

            comb = []
            for aid, anam in art:

                response = requests.get(
                    f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/{topic.lower()}/{aid}",
                    params=params,
                    headers=headers,
                )
                HYPERTECHNO = response.json()["timelinePoint"][:143]

                # Iterate over each dictionary in the list
                # Example list of dictionaries

                # Define a dictionary mapping old keys to new keys
                key_mapping = {"date": "Date", "num": f"{anam}"}

                # Create a new list of dictionaries with renamed keys
                new_HYPERTECHNO = [
                    {key_mapping.get(key, key): value for key, value in item.items()}
                    for item in HYPERTECHNO
                ]

                # Print the updated list of dictionaries

                # Define the keys to convert from string to integer
                keys_to_convert = [f"{anam}"]

                # Convert string values to integers using list comprehension
                new_HYPERTECHNO = [
                    {
                        key: int(value) if key in keys_to_convert else value
                        for key, value in item.items()
                    }
                    for item in new_HYPERTECHNO
                ]

                # Print the updated dictionary
                comb.append(new_HYPERTECHNO)
            comb = [i for j in comb for i in j]
            # Merge dictionaries based on 'Date'
            merged_dict = {}

            for item in comb:
                date = item["Date"]
                if date not in merged_dict:
                    merged_dict[date] = {}

                for key, value in item.items():
                    if key != "Date":
                        merged_dict[date][key] = value

            # Convert merged_dict to a list of dictionaries
            merged_list = [{"Date": key, **value} for key, value in merged_dict.items()]

            # Print the merged list
            print(merged_list)

            existing_records = airtable.all()

            record_exists = False

            bobo = [i["fields"]["Date"] for i in existing_records]
            for record in merged_list:

                if record["Date"] in bobo:
                    pass
                else:
                    cont = True
                    print(f"Update made for {record['Date'] }")
                    # Insert the new record at the top
                    airtable.create(
                        record,
                    )
                    upx = record

        if cont:

            # COUNTRY DEMOGRAPHIC #################################################

            for request in driver.requests:
                if request.headers:
                    if "authorization" in request.headers:
                        auth_header = request.headers["Authorization"]
                        if auth_header != "":
                            break

            print("Authorization Header:", auth_header)
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

            current_date = merged_list[0]["Date"]
            # Define a function that calculates the difference between the last and first value
            def diff(x):
                return x.iloc[-1] - x.iloc[0]

            table_name = "Country Demographics Monthly Listeners"  # Replace with your Airtable table name

            airtable = pyairtable.Table(api_key, base_id, table_name)

            existing_records = airtable.all()

            record_exists = False

            bobo = [
                (
                    i["fields"]["Date"],
                    i["fields"]["Country"],
                    i["fields"]["ArtistName"],
                    i["fields"]["Age Group"],
                )
                for i in existing_records
            ]
            for cd in codes:
                params = {
                    "time-filter": "28day",
                    "aggregation-level": "recording",
                    "country": f"{cd}",
                }

                for aid, anam in artx:
                    try:

                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/gender-by-age",
                            params=params,
                            headers=headers,
                        )

                        if response.text == "":
                            print("skipping", aid)
                            continue
                        else:
                            print("running :", aid)
                            data = response.json()

                    except:
                        for request in driver.requests:
                            if request.headers:
                                if "authorization" in request.headers:
                                    auth_header = request.headers["Authorization"]
                                    if auth_header != "":
                                        break

                        print("Authorization Header:", auth_header)
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
                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/gender-by-age",
                            params=params,
                            headers=headers,
                        )

                        if response.text == "":
                            print("skipping", aid)
                            continue
                        else:
                            print("running :", aid)
                            data = response.json()

                    age_groups = [
                        "0-17",
                        "18-22",
                        "23-27",
                        "28-34",
                        "35-44",
                        "45-59",
                        "60+",
                    ]

                    # The current date

                    # List of dictionaries for Airtable
                    airtable_data = []
                    for i, age_group in enumerate(age_groups):
                        age_group_data = {
                            "Date": current_date,
                            "ArtistName": anam,
                            "Age Group": age_group.replace("0-17", "<18"),
                            "Country": cd,
                            "Total Amount": int(
                                data[
                                    f"age_{age_group.replace('-', '_').replace('+', '')}"
                                ]
                            ),
                            "Female": int(
                                data[
                                    f"age_{age_group.replace('-', '_').replace('+', '')}_gender"
                                ]["female"]
                            ),
                            "Male": int(
                                data[
                                    f"age_{age_group.replace('-', '_').replace('+', '')}_gender"
                                ]["male"]
                            ),
                            "Nonbinary": int(
                                data[
                                    f"age_{age_group.replace('-', '_').replace('+', '')}_gender"
                                ]["nonbinary"]
                            ),
                            "Unknown": int(
                                data[
                                    f"age_{age_group.replace('-', '_').replace('+', '')}_gender"
                                ]["unknown"]
                            ),
                        }
                        airtable_data.append(age_group_data)

                print("uploading", cd)

                # Print the data to check it
                for record in airtable_data:
                    if (
                        record["Date"],
                        record["Country"],
                        record["ArtistName"],
                        record["Age Group"],
                    ) in bobo:
                        pass
                    else:
                        # print(f"Update made for {record['Date'] }")
                        airtable.create(
                            record,
                        )
                ####################################################

            ######## CITY MONTHLY ############################
            for request in driver.requests:
                if request.headers:
                    if "authorization" in request.headers:
                        auth_header = request.headers["Authorization"]
                        if auth_header != "":
                            break

            print("Authorization Header:", auth_header)
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

            params = {
                "time-filter": "28day",
                "aggregation-level": "recording",
            }
            table_name = (
                "City Listeners Monthly"  # Replace with your Airtable table name
            )

            airtable = pyairtable.Table(api_key, base_id, table_name)

            # Get all records
            records = airtable.all()

            # Delete each record
            for record in records:
                airtable.delete(record["id"])

            comb = []
            for cd in codes:
                params = {
                    "time-filter": "28day",
                    "aggregation-level": "recording",
                    "country": f"{cd}",
                }
                for aid, anam in artx:

                    try:
                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{aid}/audience/top-cities?time-filter=28day&aggregation-level=recording",
                            params=params,
                            headers=headers,
                        )
                        if response.text == "":
                            print("skipping", aid)
                            continue
                        else:
                            # print("running :" ,aid)
                            HYPERTECHNO = response.json()["geography"]

                    except:

                        for request in driver.requests:
                            if request.headers:
                                if "authorization" in request.headers:
                                    auth_header = request.headers["Authorization"]
                                    if auth_header != "":
                                        break

                        print("Authorization Header:", auth_header)
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

                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{aid}/audience/top-cities?time-filter=28day&aggregation-level=recording",
                            params=params,
                            headers=headers,
                        )
                        if response.text == "":
                            print("skipping", aid)
                            continue
                        else:
                            # print("running :" ,aid)
                            HYPERTECHNO = response.json()["geography"]
                    # Iterate over each dictionary in the list
                    # Example list of dictionaries

                    # Define a mapping from old keys to new keys
                    key_mapping = {
                        "name": "City",
                        "num": anam,
                        "country": "Country",
                        "region": "Region",
                    }

                    # Create a new list of dictionaries with renamed keys
                    new_HYPERTECHNO = [
                        {
                            key_mapping.get(key, key): value
                            for key, value in item.items()
                        }
                        for item in HYPERTECHNO
                    ]

                    # Print the updated list of dictionaries
                    # Add 'daye' key to each dictionary
                    new_HYPERTECHNO = [
                        {**d, "Date": current_date} for d in new_HYPERTECHNO
                    ]
                    # Define the keys to convert from string to integer
                    keys_to_convert = [f"{anam}"]

                    # Convert string values to integers using list comprehension
                    new_HYPERTECHNO = [
                        {
                            key: int(value) if key in keys_to_convert else value
                            for key, value in item.items()
                        }
                        for item in new_HYPERTECHNO
                    ]

                    # Print the updated dictionary
                    comb.append(new_HYPERTECHNO)

            comb = [i for j in comb for i in j]

            # Merge dictionaries based on 'Date' and 'City'
            merged_dict = {}

            for item in comb:
                date = item["Date"]
                city = item["City"]
                if (date, city) not in merged_dict:
                    merged_dict[(date, city)] = {}

                for key, value in item.items():
                    # if key not in ['Date', ]:
                    merged_dict[(date, city)][key] = value

            # Convert merged_dict to a list of dictionaries
            merged_list = [
                {"Datex": key, **value} for key, value in merged_dict.items()
            ]
            # Remove 'Datex' key from each dictionary
            merged_list = [
                {k: v for k, v in d.items() if k != "Datex"} for d in merged_list
            ]

            for record in merged_list:

                # print(f"Update made for {record['Date'] }")
                # Insert the new record at the top
                airtable.create(
                    record,
                )

            ######## COUNTRY MONTHLY ############################
            for request in driver.requests:
                if request.headers:
                    if "authorization" in request.headers:
                        auth_header = request.headers["Authorization"]
                        if auth_header != "":
                            break

            print("Authorization Header:", auth_header)
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

            params = {
                "time-filter": "28day",
                "aggregation-level": "recording",
            }
            table_name = (
                "Country Listeners Monthly"  # Replace with your Airtable table name
            )

            airtable = pyairtable.Table(api_key, base_id, table_name)
            comb = []

            for aid, anam in artx:

                try:
                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/locations?time-filter=28day&aggregation-level=recording",
                        params=params,
                        headers=headers,
                    )
                    if response.text == "":
                        print("skipping", aid)
                        continue
                    else:
                        print("running :", aid)
                    HYPERTECHNO = response.json()["geography"]
                except:
                    for request in driver.requests:
                        if request.headers:
                            if "authorization" in request.headers:
                                auth_header = request.headers["Authorization"]
                                if auth_header != "":
                                    break

                    print("Authorization Header:", auth_header)
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
                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/locations?time-filter=28day&aggregation-level=recording",
                        params=params,
                        headers=headers,
                    )
                    if response.text == "":
                        print("skipping", aid)
                        continue
                    else:
                        print("running :", aid)
                    HYPERTECHNO = response.json()["geography"]

                # Iterate over each dictionary in the list
                # Example list of dictionaries

                # Define a mapping from old keys to new keys
                key_mapping = {
                    "name": "Country",
                    "num": anam,
                    "region": "Region",
                }

                # Create a new list of dictionaries with renamed keys
                new_HYPERTECHNO = [
                    {key_mapping.get(key, key): value for key, value in item.items()}
                    for item in HYPERTECHNO
                ]

                # Print the updated list of dictionaries
                # Add 'daye' key to each dictionary
                new_HYPERTECHNO = [{**d, "Date": current_date} for d in new_HYPERTECHNO]
                # Define the keys to convert from string to integer
                keys_to_convert = [f"{anam}"]

                # Convert string values to integers using list comprehension
                new_HYPERTECHNO = [
                    {
                        key: int(value) if key in keys_to_convert else value
                        for key, value in item.items()
                    }
                    for item in new_HYPERTECHNO
                ]

                # Print the updated dictionary
                comb.append(new_HYPERTECHNO)

            comb = [i for j in comb for i in j]

            # Merge dictionaries based on 'Date' and 'City'
            merged_dict = {}

            for item in comb:
                date = item["Date"]
                city = item["Country"]
                if (date, city) not in merged_dict:
                    merged_dict[(date, city)] = {}

                for key, value in item.items():
                    # if key not in ['Date', ]:
                    merged_dict[(date, city)][key] = value

            # Convert merged_dict to a list of dictionaries
            merged_list = [
                {"Datex": key, **value} for key, value in merged_dict.items()
            ]
            # Remove 'Datex' key from each dictionary
            merged_list = [
                {k: v for k, v in d.items() if k != "Datex"} for d in merged_list
            ]
            for record in merged_list:

                # print(f"Update made for {record['Date'] }")
                # Insert the new record at the top
                airtable.create(
                    record,
                )

        return Response(
            {
                "status": "success",
            },
            status=200,
        )
        print("Upload complete")
