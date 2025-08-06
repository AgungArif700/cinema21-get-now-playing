from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


driver = webdriver.Chrome() # Buka Chrome

try:
    driver.get("https://m.21cineplex.com/id/movies?tabs=now-playing")

    print("Mulai memantau film... (Tekan Ctrl+C untuk berhenti)")
    wait = WebDriverWait(driver, 10)

    while True:
        data_judul = []
        # Tunggu sampai <h4> muncul kembali setelah refresh
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.line-clamp-2.no-break")))
        titles = driver.find_elements(By.CSS_SELECTOR, "h4.line-clamp-2.no-break")

        print("\nJudul Film ({}):".format(time.strftime("%H:%M:%S")))

        for title in titles:
            print("-", title.text)
            data_judul.append(title.text)

        time.sleep(2)  # Tunggu sebelum refresh berikutnya
        driver.refresh()  # Refresh halaman

        #save 
        with open("data.json","w") as file_json:
            json.dump(data_judul,file_json,indent=4)
        print("Refresh halaman")

except KeyboardInterrupt:
    print("\nPemantauan dihentikan oleh pengguna.")

finally:
    input("Tekan Enter untuk keluar...")
    # driver.quit()
