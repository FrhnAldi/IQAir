import requests
import pandas as pd
import os
from datetime import datetime

# ==========================
# KONFIGURASI
# ==========================
API_KEY = os.environ.get("IQAIR_API_KEY")

if not API_KEY:
    raise Exception("Environment variable IQAIR_API_KEY tidak ditemukan.")

CITY = "Jakarta"
STATE = "Jakarta"
COUNTRY = "Indonesia"

url = (
    f"https://api.airvisual.com/v2/city?"
    f"city={CITY}&state={STATE}&country={COUNTRY}&key={API_KEY}"
)

# ==========================
# REQUEST API
# ==========================
try:
    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    json_data = response.json()

    if json_data.get("status") != "success":
        raise Exception(f"API Error: {json_data}")

    data = json_data["data"]

    # ==========================
    # SIMPAN DATA
    # ==========================
    record = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": CITY,
        "aqicn": data["current"]["pollution"]["aqicn"],
        "aqius": data["current"]["pollution"]["aqius"],
        "maincn": data["current"]["pollution"]["maincn"],
        "mainus": data["current"]["pollution"]["mainus"],
        "temperature": data["current"]["weather"]["tp"],
        "humidity": data["current"]["weather"]["hu"],
        "pressure": data["current"]["weather"]["pr"],
        "wind_speed": data["current"]["weather"]["ws"],
        "wind_direction": data["current"]["weather"]["wd"]
    }

    df = pd.DataFrame([record])

    file = "aqicn.csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
        print("Data ditambahkan ke aqicn.csv")
    else:
        df.to_csv(file, index=False)
        print("aqicn.csv berhasil dibuat")

    print(df)

except requests.exceptions.RequestException as e:
    print("Request Error:", e)
    raise

except Exception as e:
    print("Error:", e)
    raise