from live_tracker.utils import *

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
        sheet = req.data["sheetName"]
        try:
            aid = extract_artist_id(aid)
        except:
            pass
        print(aid)
        rff = requests.get(f"https://open.spotify.com/artist/{aid}")

        artistName = soup_from_html(rff.text).find("title").text.split("|")[0]
        airtable = pyairtable.Table(api_key, base_id, table_name)
        global driver
        auth_header = reload_auth(driver=driver)

        try:

            headers = header(auth_header=auth_header)

            params = {
                "aggregation-level": "recording",
                "time-filter": "last5years",
            }

            response = requests.get(
                f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/streams/{aid}",
                params=params,
                headers=headers,
            )

            if response.text == "":
                response = [{"date": "", "num": "0"}]
            else:

                response = response.json()["timelinePoint"]
        except:
            # Create a new instance of ChromeDriver
            driver = wirewebdriver.Chrome(
                service=service, options=chrome_options, seleniumwire_options=options
            )
            # Now you can use the `driver` object to interact with the browser and access the requests made
            driver.get(
                "https://artists.spotify.com/c/artist/4YYOTpMoikKdYWWuTWjbqo/home"
            )
            sleep(3)
            auth_header = login(driver=driver)

            headers = header(auth_header=auth_header)

            response = requests.get(
                f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/streams/{aid}",
                params=params,
                headers=headers,
            )
            if response.text == "":
                response = [{"date": "", "num": "0"}]
            else:

                response = response.json()["timelinePoint"]

        key_mapping = {"date": "Date", "num": aid}

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
        response.insert(0, {"Date": "Date", aid: artistName})
        dc = pd.DataFrame(response)

        gc = pygsheets.authorize(
            service_file="./my-project-1515950162194-ea018b910e23.json"
        )

        # Open the Excel sheet by its name
        sh = gc.open("Competitors")
        # Find the title row

        wks = sh.worksheet_by_title(sheet)
        pt = wks.get_as_df(start="A1")
        pt.columns = [i.strip(" ") for i in pt.columns]
        dc.columns = [i.strip(" ") for i in dc.columns]
        # Merge df1 and df2 on 'Date', and if there are common columns, df2's values will be used
        df = pt.merge(dc, on="Date", how="outer", suffixes=("_yxx", "_xser"))

        # Get the common columns
        common_columns = [col for col in df.columns if col.endswith("_xser")]

        # Update the old column with new values where they are common
        for col in common_columns:
            # Remove the suffix "_y" to get the old column name
            df[col[:-5] + "_yxx"] = df[col]

        # Delete the columns from df1 which are common with df2
        to_drop = [x for x in df if x.endswith("_xser")]
        df.drop(to_drop, axis=1, inplace=True)
        # Rename columns ending with "_xser"
        df.rename(columns=lambda x: x[:-4] if x.endswith("_yxx") else x, inplace=True)

        df.loc[1:, "Date"] = pd.to_datetime(
            df["Date"].iloc[1:], format="%Y-%m-%d"
        ).dt.date

        # Separate the first row
        first_row = df.iloc[:1]

        # Sort the remaining rows by column 'A'
        sorted_rows = df.iloc[1:].sort_values(by="Date", ascending=False)

        # Concatenate the first row and the sorted rows
        df = pd.concat([first_row, sorted_rows])

        df = df.fillna("").reset_index(drop=True)

        num_columns = df.shape[1]

        # Convert the number of columns into a column label
        last_column_label = colnum_to_colname(num_columns)
        df["Total Amount"] = pd.DataFrame(
            [f"=SUM(C{i+2}:{last_column_label}{i+2})" for i in range(wks.rows - 1)],
            columns=["Total Amount"],
        )

        df.loc[0, "Total Amount"] = "Total Amount"

        wks.clear(start="A1")
        wks.set_dataframe(df, start="A1", extend=True)

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

                try:

                    auth_header = reload_auth(driver=driver)

                    headers = header(auth_header=auth_header)

                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/4YYOTpMoikKdYWWuTWjbqo/audience/timeline/{topic.lower()}/{aid}",
                        params=params,
                        headers=headers,
                    )

                    HYPERTECHNO = response.json()["timelinePoint"][:143]
                except:

                    # Create a new instance of ChromeDriver
                    try:
                        # Now you can use the `driver` object to interact with the browser and access the requests made
                        driver.get(
                            "https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home"
                        )
                    except:

                        driver = wirewebdriver.Chrome(
                            service=service,
                            options=chrome_options,
                            seleniumwire_options=options,
                        )

                        driver.get(
                            "https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home"
                        )
                    sleep(3)

                    auth_header = login(driver=driver)

                    headers = header(auth_header=auth_header)

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
            # print(merged_list)

            existing_records = airtable.all()

            record_exists = False

            bobo = [i["fields"]["Date"] for i in existing_records]
            for record in merged_list:

                if record["Date"] in bobo:
                    pass
                else:
                    cont = True
                    # print(f"Update made for {record['Date'] }")
                    # Insert the new record at the top
                    airtable.create(
                        record,
                    )
                    upx = record

        if cont:

            ########## COUNTRY DEMOGRAPHIC #################################################

            #################################################################################################################

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
                        auth_header = login(driver=driver)

                        headers = header(auth_header=auth_header)
                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/gender-by-age",
                            params=params,
                            headers=headers,
                        )

                        if response.text == "":
                            # print("skipping", aid)
                            continue
                        else:
                            # print("running :", aid)
                            data = response.json()

                    except:

                        auth_header = login(driver=driver)

                        headers = header(auth_header=auth_header)
                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/gender-by-age",
                            params=params,
                            headers=headers,
                        )

                        if response.text == "":
                            # print("skipping", aid)
                            continue
                        else:
                            # print("running :", aid)
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

                # print("uploading", cd)

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

            ######## COUNTRY MONTHLY ############################
            auth_header = login(driver=driver)

            headers = header(auth_header=auth_header)

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
                        # print("skipping", aid)
                        continue
                    else:
                        print("running :", aid)
                        HYPERTECHNO = response.json()["geography"]
                except:
                    auth_header = login(driver=driver)

                    headers = header(auth_header=auth_header)
                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{aid}/audience/locations?time-filter=28day&aggregation-level=recording",
                        params=params,
                        headers=headers,
                    )
                    if response.text == "":
                        # print("skipping", aid)
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

            ######## CITY MONTHLY ############################

            auth_header = login(driver=driver)

            headers = header(auth_header=auth_header)

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
                            # print("skipping", aid)
                            continue
                        else:
                            # print("running :" ,aid)
                            HYPERTECHNO = response.json()["geography"]

                    except:
                        auth_header = login(driver=driver)

                        headers = header(auth_header=auth_header)

                        response = requests.get(
                            f"https://generic.wg.spotify.com/s4x-insights-api/v2/artist/{aid}/audience/top-cities?time-filter=28day&aggregation-level=recording",
                            params=params,
                            headers=headers,
                        )
                        if response.text == "":
                            # print("skipping", aid)
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

        return Response(
            {},
            status=200,
        )
        print("Upload complete")
