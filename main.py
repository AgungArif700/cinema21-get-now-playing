from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import json

URL = "https://m.21cineplex.com/id/movies?tabs=now-playing"
MAX_REFRESH = 50  # Ganti sesuai kebutuhan
refresh_count = 0

def create_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    return webdriver.Edge(options=options)

# Inisialisasi driver pertama kali
driver = create_driver()
wait = WebDriverWait(driver, 10)

try:
    driver.get(URL)
    print("Mulai memantau film... (Tekan Ctrl+C untuk berhenti)")

    while True:
        try:
            data_judul = []
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.line-clamp-2.no-break")))
            titles = driver.find_elements(By.CSS_SELECTOR, "h4.line-clamp-2.no-break")

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"\nJudul Film ({timestamp}):")

            with open("log_get_file.txt", "a", encoding="utf-8") as file_log:
                file_log.write(f"\nJudul Film ({timestamp}):\n")

                for title in titles:
                    print("-", title.text)
                    file_log.write(f"- {title.text}\n")
                    data_judul.append(title.text)

            with open("data.json", "w", encoding="utf-8") as file_json:
                json.dump(data_judul, file_json, indent=4, ensure_ascii=False)

            time.sleep(15)
            driver.refresh()
            refresh_count += 1
            print(f"Refresh halaman ke-{refresh_count}")

            # Restart driver tiap N refresh
            if refresh_count >= MAX_REFRESH:
                print("Restart driver untuk mencegah browser not responding...")
                driver.quit()
                driver = create_driver()
                wait = WebDriverWait(driver, 10)
                driver.get(URL)
                refresh_count = 0

        except (TimeoutException, WebDriverException) as e:
            error_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{error_time}] : Koneksi gagal atau halaman tidak bisa dimuat. Menunggu koneksi pulih...")

            with open("log_get_file.txt", "a", encoding="utf-8") as file_log:
                file_log.write(f"[{error_time}] : Gagal memuat halaman. Coba lagi nanti.\n")

            time.sleep(10)
            try:
                driver.get(URL)
            except Exception as err:
                print(f"[{error_time}] : Gagal membuka ulang halaman: {err}")
                with open("log_get_file.txt", "a", encoding="utf-8") as file_log:
                    file_log.write(f"[{error_time}] : Gagal membuka ulang halaman: {err}\n")

except KeyboardInterrupt:
    print("\nPemantauan dihentikan oleh pengguna.")

finally:
    input("Tekan Enter untuk keluar...")
    driver.quit()

