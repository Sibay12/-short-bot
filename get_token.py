"""Obtain a YouTube OAuth refresh token once, using Google Colab."""
# Open https://colab.research.google.com, create a notebook, and run this code in one cell.
import requests, time

CLIENT_ID = "PASTE_YOUR_OAUTH_CLIENT_ID_HERE"
CLIENT_SECRET = "PASTE_YOUR_OAUTH_CLIENT_SECRET_HERE"

d = requests.post("https://oauth2.googleapis.com/device/code",
                  data={"client_id": CLIENT_ID,
                        "scope": "https://www.googleapis.com/auth/youtube"}).json()
print("1) Open this URL:", d["verification_url"])
print("2) Enter this code:", d["user_code"])
print("3) Sign in with the Google account that owns your YouTube channel, then approve access.")

while True:
    time.sleep(d.get("interval", 5))
    t = requests.post("https://oauth2.googleapis.com/token",
                      data={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                            "device_code": d["device_code"],
                            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}).json()
    if "refresh_token" in t:
        print("\nYT_REFRESH_TOKEN =", t["refresh_token"])
        break
    if t.get("error") not in ("authorization_pending", "slow_down"):
        print("Error:", t)
        break
