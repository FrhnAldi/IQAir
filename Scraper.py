import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# GANTI URL ini dengan URL kota yang ingin kamu pantau di IQAir
URL = "https://www.iqair.com/indonesia/jakarta"

# Header wajib agar request kita terlihat seperti browser asli (menghindari blokir)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def scrape_aqi():
    try:
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
           
            # Mencari elemen AQI. Kelas HTML IQAir bisa berubah sewaktu-waktu.
            # Saat ini, nilai AQI biasanya dibungkus class "aqi-value__value".
            aqi_element = soup.find(class_="aqi-value__value")
           
            if aqi_element:
                aqi_value = aqi_element.text.strip()
                # Waktu pengambilan data (WIB atau UTC menyesuaikan server cloud)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               
                # Menulis/menambahkan data ke iqair_data.csv
                file_exists = os.path.isfile('iqair_data.csv')
                with open('iqair_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(['Timestamp', 'AQI']) # Header kolom jika file baru
                    writer.writerow([now, aqi_value])
               
                print(f"Berhasil! AQI Jakarta saat ini: {aqi_value} pada {now}")
            else:
                print("Gagal menemukan elemen AQI. Silakan periksa kembali class HTML IQAir.")
        else:
            print(f"Gagal memuat halaman. Status Code: {response.status_code}")
           
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    scrape_aqi()
