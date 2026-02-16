import os
import time
import logging
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 1. KÖRNYEZETI VÁLTOZÓK BETÖLTÉSE (.env fájlból)
load_dotenv()

# 2. NAPLÓZÁS (LOGGING) BEÁLLÍTÁSA
logging.basicConfig(
    filename='robot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# 3. BÖNGÉSZŐ BEÁLLÍTÁSA
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-notifications")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Globális lista a vásárolt termékeknek
megvett_termekek = []

# --- FUNKCIÓK ---

def bejelentkezes():
    try:
        logging.info("--- Bejelentkezés indítása ---")
        user = os.getenv("SAUCE_USER")
        password = os.getenv("SAUCE_PASSWORD")

        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        time.sleep(1)

        driver.find_element(By.ID, "user-name").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        
        logging.info("Sikeres bejelentkezés.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Hiba a bejelentkezésnél: {e}")
        driver.save_screenshot("login_hiba.png")
        raise # Megállítjuk a programot, ha nem sikerült belépni

def vasarlas(ar_limit):
    try:
        logging.info(f"--- Vásárlás indítása ${ar_limit} alatt ---")
        ar_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        nev_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        gombok = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        
        for i in range(len(ar_elemek)):
            ar_szoveg = ar_elemek[i].text.replace("$", "")
            ar_szam = float(ar_szoveg)
            nev = nev_elemek[i].text
            
            if ar_szam < ar_limit:
                gombok[i].click()
                megvett_termekek.append(f"{nev} - ${ar_szam}")
                logging.info(f"Kosárba téve: {nev}")
    except Exception as e:
        logging.error(f"Hiba a vásárlás során: {e}")

def jelentes_iras():
    try:
        most = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fajlnev = f"riport_{most}.txt"
        
        with open(fajlnev, "w", encoding="utf-8") as fajl:
            fajl.write(f"VÁSÁRLÁSI RIPORT - {most}\n")
            fajl.write("----------------\n")
            if not megvett_termekek:
                fajl.write("Nem történt vásárlás.\n")
            else:
                for t in megvett_termekek:
                    fajl.write(f"Megvett tétel: {t}\n")
            fajl.write("----------------\n")
            fajl.write(f"Összesen: {len(megvett_termekek)} db termék.\n")
        
        print(f"Riport elkészült: {fajlnev}")
        logging.info(f"Riport sikeresen mentve: {fajlnev}")
    except Exception as e:
        logging.error(f"Nem sikerült a riportot megírni: {e}")

# --- FŐ PROGRAMFUTTATÁS ---

if __name__ == "__main__":
    try:
        bejelentkezes()
        vasarlas(20.00) # Itt állíthatod az árlimitet
        jelentes_iras()
    except Exception as e:
        print(f"Váratlan hiba történt a futás során: {e}")
    finally:
        # Ez a rész mindig lefut: bezárja a böngészőt
        driver.quit()
        print("Böngésző bezárva, program vége.")
