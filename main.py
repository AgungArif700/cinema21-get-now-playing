from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import json


# driver = webdriver.Chrome() # Buka Chrome
driver = webdriver.Edge()  # Gunakan Edge, pastikan msedgedriver sudah terpasang

try:
    driver.get("https://m.21cineplex.com/id/movies?tabs=now-playing")

    print("Mulai memantau film... (Tekan Ctrl+C untuk berhenti)")
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            data_judul = []
            # Tunggu sampai <h4> muncul kembali setelah refresh
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.line-clamp-2.no-break")))
            titles = driver.find_elements(By.CSS_SELECTOR, "h4.line-clamp-2.no-break")

            print("\nJudul Film ({}):".format(time.strftime("%H:%M:%S")))
            with open("log_get_file.txt","a") as file_log:
                file_log.write("\nJudul Film ({}): \n".format(time.strftime("%H:%M:%S")))

                for title in titles:
                    print("-", title.text)
                    file_log.write(f"- {title.text}\n")
                    data_judul.append(title.text)

            #save 
            with open("data.json","w") as file_json:
                json.dump(data_judul,file_json,indent=4)

            time.sleep(15)  # Tunggu sebelum refresh berikutnya
            driver.refresh()  # Refresh halaman
            print("Refresh halaman")
        except (TimeoutException, WebDriverException) as e:
            print(f"[{time.strftime('%H:%M:%S')}] : Koneksi gagal atau halaman tidak bisa dimuat. Menunggu koneksi pulih...")
            time.sleep(10)  # Tunggu 10 detik sebelum mencoba lagi

            try:
                driver.get("https://m.21cineplex.com/id/movies?tabs=now-playing")
            except:
                pass

except KeyboardInterrupt:
    print("\nPemantauan dihentikan oleh pengguna.")

finally:
    input("Tekan Enter untuk keluar...")
    driver.quit()
