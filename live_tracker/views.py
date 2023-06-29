from live_tracker.utils import *
from live_tracker.models import Artist, ArtistMetrics

auth_header = "Bearer BQCcjMVsNWMNV9-55PgvWjFUyeuXS7GXqmNgSdwKkgjAo4fhylTGU21rO7EKcgt_9Q5_wl4fc5_kVND-xEAnJ7C_nksYQ3LUDUQO78vyYGBT5OpFm0rx5BAfivlq8bi3QUduB6pHyvZ61R1B3xWUW0stfxjLK3hnN34ThYoeveAXNh8kzsTLQKMC-NVjEglPbXsrPqJH3kcjUUQ_EIMIckwuZzoP"

headers = {
    "authority": "generic.wg.spotify.com",
    "accept": "application/json",
    "accept-language": "en-US",
    "app-platform": "Browser",
    "authorization": f"{auth_header}",
    "content-type": "application/json",
    "origin": "https://artists.spotify.com",
    "referer": "https://artists.spotify.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "spotify-app-version": "1.0.0.d5715c5",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    "x-cloud-trace-context": "0000000000000000123d34fd4b219e3a/7064777314035793204;o=1",
}


def get_all_artist_ids():
    genres = Artist.objects.values_list("id", flat=True).distinct()
    return list(genres)


def get_all_artist_names():
    genres = Artist.objects.values_list("name", flat=True).distinct()
    return list(genres)


def append_artist_metrics(data):
    # Check if the row already exists based on the unique fields (e.g., date, artist_id)
    existing_row = ArtistMetrics.objects.filter(
        date=data["Date"], artist_id=data["ArtistId"], country=data["Country"]
    ).first()

    if existing_row:
        # Row already exists, skip the append step
        print("Row already exists")
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
        artist_metrics.save()
        print("Row appended successfully")


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
    "",
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
        for artid, artName in zip(artid, artName):
            df = pd.DataFrame()
            for cd in codes:
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
                timeline_points = [entry["timeline"]["timelinePoint"] for entry in nn]

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
                    append_artist_metrics(row)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")
