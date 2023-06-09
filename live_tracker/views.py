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

service = Service(executable_path='chromedriver')

options = {
    "verify_ssl": True  # Verify SSL certificates but beware of errors with self-signed certificates
}

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_profile_path = "/content/Default"
chrome_options.add_argument("--user-data-dir=Default" )
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")










# Create a new instance of ChromeDriver
driver = wirewebdriver.Chrome(service=service, options=chrome_options,seleniumwire_options=options)
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


def HomePage(req):
    return render(
        req,
        "base/index.html",
    )


class UploadView(APIView):
    @staticmethod
    def post(req):
        aid = req.data["aid"]
        artistName = req.data["artistName"]
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
            driver = wirewebdriver.Chrome(service=service, options=chrome_options,seleniumwire_options=options)
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

            response = response.json()["timelinePoint"][:180]

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

        for rr in response:
            records = airtable.first(formula=match({"Date": rr["Date"]}))
            if not records:
                airtable.create(rr)
            else:
                record_id = records["id"]
                updated_fields = rr
                airtable.update(record_id, rr)

        print("Upload complete")

        return Response(
            {
                "status": "success",
                "data": response,
            },
            status=201,
        )
        print("Upload complete")
