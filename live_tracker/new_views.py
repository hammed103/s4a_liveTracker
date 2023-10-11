from live_tracker.utils import *
import cloudinary.uploader
import csv
from io import StringIO


def get_size(content):
    return len(content.getvalue()) / (1024 * 1024)


# Define a maximum size for each file (e.g., 10MB)
MAX_SIZE = 10


def chunk_dataframe(df):
    # Start by splitting the dataframe into two equal parts
    mid_idx = len(df) // 2
    chunks = [df.iloc[:mid_idx], df.iloc[mid_idx:]]

    new_chunks = []
    for chunk in chunks:
        csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
        sio = StringIO(csv_content)

        # If content is larger than MAX_SIZE, divide chunk into two again
        while get_size(sio) > MAX_SIZE:
            mid_idx = len(chunk) // 2
            new_chunks.extend([chunk.iloc[:mid_idx], chunk.iloc[mid_idx:]])
            chunk = new_chunks[-1]

            csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            sio = StringIO(csv_content)
        else:
            new_chunks.append(chunk)

    return new_chunks


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
        driver.get("https://artists.spotify.com/c/artist/3EYY5FwDkHEYLw5V86SAtl/home")
        
        sleep(5)

        auth_header = login(driver)

        print(auth_header)
        basket = []
        for name,id in [ ("HYPERTECHNO","4YYOTpMoikKdYWWuTWjbqo"),( "deadboy","45u4hhyZlr11XAFqO74eTZ"),("SICK LEGEND","3EYY5FwDkHEYLw5V86SAtl"),( "11:11 Music Group","2MDj296KJIfgWDNBtHzeFi"),("TEKKNO","0aUMVkR8QV0LSdv9VZOATn"),
                        ( "90210","4KGcll2G3f04WMGTT19eyz"),
             ("two punks in love","6pOqcPiFkbjIKUBF86cfuM"),( "Dark Ambiental Orchestra","54sRZ8k1rq8Dt83h6LhHey"),("Drill Gates","4anRsJeihT0h3v3YO2q8wQ")] :
            print(name,id)
            auth_header,ban = retro(auth_header,name,id,driver)
            basket.append(ban)

        jk = pd.concat(basket)
        from datetime import date,timedelta
        oki = jk[jk.Date.isin([str(date.today() - timedelta(2)),str(date.today() - timedelta(1))])]

        unique_dates = oki['Date'].unique()

        for date in unique_dates:
            # Filter the dataframe for the specific date
            din = oki[oki['Date'] == date]
            if din[din.country == "Worldwide"].Streams.iloc[0] == 0 :
                continue
            # Convert the date to a string format suitable for filenames
            date_str = str(date)
            file_name = f"spotify_artist/{date_str}_a.csv"

            csv_content = din.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            result = cloudinary.uploader.upload(
            StringIO(csv_content),
            public_id=file_name,
            folder="/Soundcloud/",
            resource_type="raw",
            overwrite=True,
        )
            

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")


class youtube(APIView):
    @staticmethod
    def get(req):
        import datetime
        from googleapiclient.discovery import build

        # Replace with your own API key
        API_KEY = 'AIzaSyAGhD50OAGxkGo1u4CWPUzKr47cAnGNJ8U'


        # Usage example
        time_range = "last7days"
        start_date, end_date = get_date_range(time_range)
        print("Start Date:", start_date)
        print("End Date:", end_date)


        country_data = [
            ("Germany", "DE"),
            ("United Kingdom", "GB"),
            ("United States", "US"),
            ("Netherlands", "NL"),
            ("France", "FR"),
            ("Australia", "AU"),
            ("Brazil", "BR"),
            ("Poland", "PL"),
            ("Sweden", "SE"),
            ("Austria", "AT"),
            ("India", "IN"),
            ("Canada", "CA"),
            ("Turkey", "TR"),
            ("Switzerland", "CH"),
            ("Norway", "NO"),
            ("Indonesia", "ID"),
            ("Mexico", "MX"),
            ("New Zealand", "NZ"),
            ("Belgium", "BE"),
            ("Ireland", "IE"),
            ("Italy", "IT"),
            ("Portugal", "PT"),
            ("Spain", "ES"),
            ("Denmark", "DK"),
            ("Finland", "FI"),
        ]

        # Convert the list to a dictionary
        country_dict = {code: name for name, code in country_data}

        # Example: Look up a country name by its country code
        country_code = "US"
        country_name = country_dict.get(country_code, "Country not found")  # Replace "Country not found" with a default value if needed

        print(f"Country Name for '{country_code}': {country_name}")

        API_KEYS = ['AIzaSyACizvrGekWinFmDxDwDIPzQXmaGcFksyY',
            'AIzaSyAsCTltn26rBbdxgmQfjnKTC10JIDm4D3M',
            'AIzaSyD3Fgh46t4PbTGJDhFCUl5z6CunOdY-7rI',
            'AIzaSyDuELsjFdWHFKneMJJbFWK66qER5oauH_g',
            'AIzaSyCaZOqEp5zFkT5yotp4Y5HdNC3Nj_cv7Uo',
            'AIzaSyAGhD50OAGxkGo1u4CWPUzKr47cAnGNJ8U',
            'AIzaSyB3-bLwTfA9KnK3cjAcmqLUZqZG9gQoUUU',
            'AIzaSyDhu6s9kpQWqaaBBLfFFz0svxg_XOm4N_A',
            'AIzaSyBOrS89w8KbwNBKlgsQtEqkW5T5xtlwyhc',
            'AIzaSyCxb0O2TySWmqUDYwJijC3saaNNZRmLcoI',
            'AIzaSyBvFKe4b6igEnRhyP6-sZmsA_WdfxzNUBc',
            'AIzaSyAV2FGgubcpeK_Edgbxo3gbQQVVS3ns2HM',
            'AIzaSyAfQgBOf36zUrx05rDI4f58XfcJaPnDTBU',
            'AIzaSyDxx5LA1Zrmr0QAexG7Ofc8cP74b77iXJ8',
            'AIzaSyC1h3O-4ZUW81MTXimaXcJw_vxjht_7dxs',
            'AIzaSyDX8ugQezm24U2iS5Visy_-gm7swrk1dDY',
            'AIzaSyAILkvGbTnK_mBd9ND_22ObDFquFRp4h8U',
            'AIzaSyAHSOMAWKNmkqRg0866rFgvLNRJOTQb1j8',
            'AIzaSyBAhKMF_bKBGQWafOV-mw2ZOGgp5a1iOhY',
            'AIzaSyBxXUeSQ01GTzYVZiepNHlZGJn1ksfP8N0',
            'AIzaSyAy8GgJflH2QwLTBVlvdfwUgjOpnh_ESnw',
            'AIzaSyAAaxC9umf4jMM_lCFKd9IvyE-nR6ySLiE',
            'AIzaSyB0SEuHBkuj32erb4wqrrtuUOypfC9rxws',
            'AIzaSyBn4ZsJe3UX4HXjrKyAjj4UJq5hwePIca8',
            ]



        # List of keywords and time filters to iterate through
        keywords = [
                    "hardstyle",
                    "tekkno",
                    "techno",
                    "drill",
                    "hardtekk",
                    "tekk",
                    "rap techno",
                    "phonk",
                    "lofi",
                    "lo-fi",
                    "tiktok",
                    "sped-up",
                    "spedup",
                    "slowed",
                    "remix",
                    "viral",
                    "sad",
                    "tired",
                    "rage",
                    "gym",
                    "pump",
                    "zyzz",
                    "fuark",
                    "zyzzcore",
                    "breakcore",
                    "corecore",
                    "stutterhouse"
                ]
        max_duration = '240'  # 4 minutes in seconds
        time_filters = [
        "last30days","last7days","last24hrs"
        ]
        country_codes = [
            "DE", "GB", "US", "NL", "FR", "AU", "BR", "PL", "SE", "AT","IN", "CA"
        ]



        # Iterate through keywords and time filters
        results = []
        try:
            for keyword in keywords:
                print(keyword)
                print(".........................................................")
                for country_code in country_codes:
                    print(country_code)
                    for time_filter in time_filters:
                        print(time_filter)
                        print(".........................................................")
                        for i in range(len(API_KEYS)):
                            try:
                                result_df = search_and_extract_info(API_KEYS[i], keyword, max_duration, time_filter, country_code)
                                results.append(result_df)
                                print(".........................................................")
                                break  # If successful, break out of the retry loop
                            except Exception as e:
                                print(f"API Key {i+1} failed with error: {str(e)}")
                                if i == len(API_KEYS) -1:
                                    raise Exception("All API keys failed for this combination. Moving to next combination.")  # Raise an error if all tries fail
                                continue  # Try the next API key
                        # Concatenate the DataFrames for each combination of keyword, country code, and time filter
                final_result = pd.concat(results, ignore_index=True)
                from datetime import date,timedelta
        
                date_str = str(date.today())
                file_name = f"youtube/{date_str}_a.csv"
                final_result = final_result.iloc[:,1:]

                chunks = chunk_dataframe(final_result)

                for index, chunk in enumerate(chunks):
                    csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
                    sio = StringIO(csv_content)

                    suffix = chr(97 + index)  # 97 is ASCII for 'a'
                    # file_name = f"{base_file_name}_{suffix}.csv"
                    file_name = f"youtube/{date_str}_{suffix}.csv"

                    result = cloudinary.uploader.upload(
                        sio,
                        public_id=file_name,
                        folder="/Soundcloud/",
                        resource_type="raw",
                        overwrite=True,
                    )
                    
        except Exception as outer_e:
            print(f"Error during the iteration: {str(outer_e)}")




# Now, final_result contains the combined results for all combinations of keywords and time filters.

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")