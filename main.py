import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "mroverledge@gmail.com"
MY_PASSWORD = "tctwsukxzuvfhpzg"
MY_LAT = 26.223400 # Your latitude
MY_LONG = 79.841003 # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    print(f"LAT: {iss_latitude}")
    print(f"LONG: {iss_longitude}")


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    #Below code, sunrise and sunset ke time ko short/cut-down karke hours ke form me laane ke liye likha hai
    #split("x") = jha-jha x hog vha se break karke list bna dega yeh function
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(3)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="abhinaybhadauria99@gmail.com",
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )


