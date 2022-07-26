import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 24.829100
MY_LONG = 87.214104
MY_EMAIL = "mdtauseefakhtar284@gmail.com"
MY_PASSWORD = "armaan786"


"""
The aim of this project is to send an email when the ISS is passing to our location and for the visibility of the 
station it should be viewed at night time. So we also have a function which check whether currently it is day or night.
So when the current ISS location is approximately(+5 or -5) equals to our location and it is the night time then
we will be sending the message to the email.
In order to execute the code every 60 seconds then we will be using the time module and then allow it to wait for 60s
and then execute the work using while loop.
"""


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="mohammadtauseef284@gmail.com",
                            msg="Subject:Look Up\n\nThe ISS is above you in the sky.")
        connection.close()



