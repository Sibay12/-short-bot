# YouTube refresh token निकालने की स्क्रिप्ट (एक बार चलानी है)।
# Google Colab (colab.research.google.com) में नया नोटबुक खोलकर यह पूरा कोड एक सेल में पेस्ट करके चलाएँ।
import requests, time

CLIENT_ID = "यहाँ अपनी CLIENT_ID डालें"
CLIENT_SECRET = "यहाँ अपनी CLIENT_SECRET डालें"

d = requests.post("https://oauth2.googleapis.com/device/code",
                  data={"client_id": CLIENT_ID,
                        "scope": "https://www.googleapis.com/auth/youtube"}).json()
print("1) यह लिंक खोलें:", d["verification_url"])
print("2) यह कोड डालें:", d["user_code"])
print("3) जिस Google अकाउंट में YouTube चैनल है, उसी से लॉगिन करें और Allow करें...")

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
