from live_tracker.utils import *
from live_tracker.models import Artist, ArtistMetrics


class start(APIView):
    @staticmethod
    def get(req):

        # Create a new instance of ChromeDriver
        driver = wirewebdriver.Chrome(
            service=service, options=chrome_options, seleniumwire_options=options
        )

        # Clear the cache by deleting all cookies
        driver.delete_all_cookies()

        driver.refresh()
        # Now you can use the `driver` object to interact with the browser and access the requests made
        driver.get("https://artists.spotify.com/c/artist/4YYOTpMoikKdYWWuTWjbqo/audience/stats")
        sleep(3)

        auth_header = login(driver)

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
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'spotify-app-version': '1.0.0.4ff711e',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203',
        }

        # 1. Authorize the client using the provided JSON key
        gc = pygsheets.authorize(service_file='my-project-1515950162194-ea018b910e23.json')

        # 2. Open the Google Spreadsheet using its title
        spreadsheet = gc.open('Competitors')
        for sheet in ['Copy of 11:11'] :

            # 3. Select a specific worksheet by its title (assuming the name of the sheet is 'Sheet1')
            worksheet = spreadsheet.worksheet_by_title(sheet)

            # 4. Extract a specific row (for example, the 2nd row)
            row_values = worksheet.get_row(2)

            ddx = row_values[3:]

            tod = str(date.today())

            last = str(date.today() - timedelta(364))


            dc= pd.DataFrame()
            # Iterate over the other sheets and merge them with the main dataframe
            for aid in ddx[:]:

                params = {
                                        'from_date': f'{last}',
                                        'to_date': f'{tod}',
                    }
                try:
                    rff = requests.get(f"https://open.spotify.com/artist/{aid}",headers=headers)

                    artistName = soup_from_html(rff.text).find("title").text.split("|")[0]

                    response = requests.get(
                        f'https://generic.wg.spotify.com/audience-engagement-view/v1/artist/{aid}/stats',
                        params=params,
                        headers=headers,
                    )


                    dt = response.json()
                    fr = pd.DataFrame(dt["streams"]["current_period_timeseries"],)
                    print(aid)
                except:
                    continue

                header_row = ["Date", artistName, ]
                arrays = [header_row, ["Dates",aid]]
                tuples = list(zip(*arrays))
                fr.columns = pd.MultiIndex.from_tuples(tuples)

                if dc.shape == (0,0):
                    dc = fr
                else:
                    dc = pd.merge(dc, fr, on= [('Date','Dates')], how="outer")

            # Create the "TOTAL AMOUNT" column with SUM formulas
            # Create the "TOTAL AMOUNT" column with SUM formulas
            last_column_letter = get_column_letter(len(dc.columns))
            dc["TOTAL AMOUNT"] = [f"=SUM(A{row_num + 2}:{last_column_letter}{row_num + 2})" for row_num in range(len(dc))]
            dc[('Day', 'Day')] = dc[(           'Date',                   'Dates')].apply(get_day_of_week)
            # Reorder the columns to have "TOTAL AMOUNT" first
            dc = dc[[('Day', 'Day')] + [col for col in dc if col != ('Day', 'Day') ]]
            dc = dc[[('TOTAL AMOUNT', '')] + [col for col in dc if col != ('TOTAL AMOUNT', '') ]]

            dc.iloc[0,0] = "TOTAL AMOUNT"
            worksheet.clear()
            # Update the worksheet with the new DataFrame
            worksheet.set_dataframe(dc, start="A1")


        driver.quit()



        return Response(
            {
                "status": "success",
                "data": auth_header
            },
            status=201,
        )
        print("Upload complete")





def get_all_artist_ids():
    genres = Artist.objects.values_list("id", flat=True).distinct()
    return list(genres)


def get_all_artist_names():
    genres = Artist.objects.values_list("name", flat=True).distinct()
    return list(genres)


def append_artist_metrics(data, cd):
    # Check if the row already exists based on the unique fields (e.g., date, artist_id)
    try:
        existing_row = ArtistMetrics.objects.filter(
            date=data["Date"], artist_id=data["ArtistId"], country=data["Country"]
        ).first()
    except:
        sleep(3)
        existing_row = ArtistMetrics.objects.filter(
            date=data["Date"], artist_id=data["ArtistId"], country=data["Country"]
        ).first()

    if existing_row:
        # Row already exists, skip the append step
        print("Row already exists", cd)
    else:
        # Row doesn't exist, proceed with appending
        artist_metrics = ArtistMetrics(
            date=datetime.strptime(data["Date"], "%Y-%m-%d").date(),
            artist_name=data["ArtistName"],
            artist_id=data["ArtistId"],
            country=data["Country"],
            listeners=data["listeners"],
            streams=data["streams"],
            streams_per_listener=data["streams_per_listener"],
            saves=data["saves"],
            playlist_adds=data["playlist_adds"],
            followers=data["followers"],
            total_active_audience=data["Total active audience"],
            super_listeners=data["Super listeners"],
            moderate_listeners=data["Moderate listeners"],
            light_listeners=data["Light listeners"],
        )
        try:
            artist_metrics.save()
            print("Row appended successfully", cd)
        except:
            sleep(3)
            artist_metrics.save()
            print("Row appended successfully", cd)


from datetime import datetime


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


class refreshMain(APIView):
    @staticmethod
    def get(req):
        artid = get_all_artist_ids()
        artName = get_all_artist_names()
        global driver
        for artid, artName in zip(artid[4:], artName[4:]):
            df = pd.DataFrame()
            for cd in codes:
                try:
                    params = {
                        "country": cd,
                        "time-filter": "last5years",
                    }

                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{artid}/stats",
                        params=params,
                        headers=headers,
                    )
                    if response.text == "":
                        continue
                    if response.text == "PERMISSION_DENIED":

                        break
                    nn = response.json()["metricTimelines"]
                    # Extract metrics and their timeline points
                    metrics = [entry["metric"] for entry in nn]
                    timeline_points = [
                        entry["timeline"]["timelinePoint"] for entry in nn
                    ]

                    # Create a dictionary to store the data
                    data_dict = {
                        metric: [point["num"] for point in points]
                        for metric, points in zip(metrics, timeline_points)
                    }

                    # Create the DataFrame
                    df = pd.DataFrame(data_dict)
                    df["Date"] = pd.Series([i["date"] for i in timeline_points[0]])
                    df["Country"] = cd
                    df["ArtistName"] = artName
                    df["ArtistId"] = artid
                    params = {"country": cd}
                    responsex = requests.get(
                        f"https://generic.wg.spotify.com/fanatic-audience-segments/v0/artist/{artid}/segments",
                        params=params,
                        headers=headers,
                    )
                    segment = pd.DataFrame(
                        pd.DataFrame(responsex.json()["segmentCountsTimeline"])[
                            "active"
                        ].to_list()
                    )

                    segment.columns = [
                        "Total active audience",
                        "Super listeners",
                        "Moderate listeners",
                        "Light listeners",
                    ]
                    segment["Date"] = pd.DataFrame(
                        responsex.json()["segmentCountsTimeline"]
                    )["date"]
                    segment["Country"] = cd
                    df = df.merge(segment, how="outer")

                except:
                    try:
                        auth_header = reload_auth(driver)

                        headers = header(auth_header=auth_header)

                        params = {
                            "country": cd,
                            "time-filter": "last5years",
                        }

                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{artid}/stats",
                            params=params,
                            headers=headers,
                        )
                        if response.text == "":
                            continue
                        if response.text == "PERMISSION_DENIED":

                            break
                        nn = response.json()["metricTimelines"]
                        # Extract metrics and their timeline points
                        metrics = [entry["metric"] for entry in nn]
                        timeline_points = [
                            entry["timeline"]["timelinePoint"] for entry in nn
                        ]

                        # Create a dictionary to store the data
                        data_dict = {
                            metric: [point["num"] for point in points]
                            for metric, points in zip(metrics, timeline_points)
                        }

                        # Create the DataFrame
                        df = pd.DataFrame(data_dict)
                        df["Date"] = pd.Series([i["date"] for i in timeline_points[0]])
                        df["Country"] = cd
                        df["ArtistName"] = artName
                        df["ArtistId"] = artid
                        params = {"country": cd}
                        responsex = requests.get(
                            f"https://generic.wg.spotify.com/fanatic-audience-segments/v0/artist/{artid}/segments",
                            params=params,
                            headers=headers,
                        )
                        segment = pd.DataFrame(
                            pd.DataFrame(responsex.json()["segmentCountsTimeline"])[
                                "active"
                            ].to_list()
                        )

                        segment.columns = [
                            "Total active audience",
                            "Super listeners",
                            "Moderate listeners",
                            "Light listeners",
                        ]
                        segment["Date"] = pd.DataFrame(
                            responsex.json()["segmentCountsTimeline"]
                        )["date"]
                        segment["Country"] = cd
                        df = df.merge(segment, how="outer")
                    except:
                        auth_header = reload_auth(driver)

                        headers = header(auth_header=auth_header)

                        params = {
                            "country": cd,
                            "time-filter": "last5years",
                        }

                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{artid}/stats",
                            params=params,
                            headers=headers,
                        )
                        if response.text == "":
                            continue
                        if response.text == "PERMISSION_DENIED":

                            break
                        nn = response.json()["metricTimelines"]
                        # Extract metrics and their timeline points
                        metrics = [entry["metric"] for entry in nn]
                        timeline_points = [
                            entry["timeline"]["timelinePoint"] for entry in nn
                        ]

                        # Create a dictionary to store the data
                        data_dict = {
                            metric: [point["num"] for point in points]
                            for metric, points in zip(metrics, timeline_points)
                        }

                        # Create the DataFrame
                        df = pd.DataFrame(data_dict)
                        df["Date"] = pd.Series([i["date"] for i in timeline_points[0]])
                        df["Country"] = cd
                        df["ArtistName"] = artName
                        df["ArtistId"] = artid
                        params = {"country": cd}
                        responsex = requests.get(
                            f"https://generic.wg.spotify.com/fanatic-audience-segments/v0/artist/{artid}/segments",
                            params=params,
                            headers=headers,
                        )
                        segment = pd.DataFrame(
                            pd.DataFrame(responsex.json()["segmentCountsTimeline"])[
                                "active"
                            ].to_list()
                        )

                        segment.columns = [
                            "Total active audience",
                            "Super listeners",
                            "Moderate listeners",
                            "Light listeners",
                        ]
                        segment["Date"] = pd.DataFrame(
                            responsex.json()["segmentCountsTimeline"]
                        )["date"]
                        segment["Country"] = cd
                        df = df.merge(segment, how="outer")

                # df.Date = pd.to_datetime(df.Date)

                df = df[
                    [
                        "Date",
                        "ArtistName",
                        "ArtistId",
                        "Country",
                        "listeners",
                        "streams",
                        "streams_per_listener",
                        "saves",
                        "playlist_adds",
                        "followers",
                        "Total active audience",
                        "Super listeners",
                        "Moderate listeners",
                        "Light listeners",
                    ]
                ]

                df.loc[df.Country == "", "Country"] = "World"
                df = df.sort_values("Date", ascending=False)
                df = df.reset_index(drop=True).fillna(0)
                jio = df.to_dict(orient="records")

                for row in jio:
                    append_artist_metrics(row, cd)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")
