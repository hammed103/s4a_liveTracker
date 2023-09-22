from live_tracker.utils import *
import cloudinary.uploader
import csv
from io import StringIO

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
             ("two punks in love","6pOqcPiFkbjIKUBF86cfuM"),( "Dark Ambiental Orchestra","54sRZ8k1rq8Dt83h6LhHey"),("Drill Gates","4anRsJeihT0h3v3YO2q8wQ"),  ( "RAINY JASPER","4rlJtMEpxuem6xZ9DPycFD"),
                    ("AMBIENT JASPER","3vDFmwP5PXRqcAEd9acoNs")] :
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