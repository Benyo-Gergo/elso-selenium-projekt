import os
import time
import logging
import datetime
import pandas as pd  # <--- Ez kell az Excelhez!
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. KÖRNYEZETI VÁLTOZÓK BETÖLTÉSE
load_dotenv()

# 2. NAPLÓZÁS BEÁLLÍTÁSA
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

# Globális lista - ide gyűjtjük az adatokat szótár formátumban a Pandasnak
megvett_termekek = []

# --- FUNKCIÓK ---

def bejelentkezes():
    try:
        logging.info("--- Bejelentkezés indítása ---")
        user = os.getenv("SAUCE_USER")
        password = os.getenv("SAUCE_PASSWORD")

        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # WebDriverWait - nem vár fixen, csak amíg meg nem jelenik az elem
        wait = WebDriverWait(driver, 10)

        user_field = wait.until(EC.element_to_be_clickable((By.ID, "user-name")))
        user_field.send_keys(user)

        pass_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        pass_field.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        
        logging.info("Sikeres bejelentkezés.")
    except Exception as e:
        logging.error(f"Hiba a bejelentkezésnél: {e}")
        driver.save_screenshot("login_hiba.png")
        raise

def vasarlas(ar_limit): # <--- EZ HIÁNYZOTT!
    try:
        logging.info(f"--- Vásárlás indítása ${ar_limit} alatt ---")
        wait = WebDriverWait(driver, 10)
        
        # Várunk, amíg legalább egy termék ára megjelenik
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price")))

        ar_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        nev_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        gombok = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        
        for i in range(len(ar_elemek)):
            ar_szoveg = ar_elemek[i].text.replace("$", "")
            ar_szam = float(ar_szoveg)
            nev = nev_elemek[i].text
            
            if ar_szam < ar_limit:
                gombok[i].click()
                # Szótárként mentjük az adatot a Pandas miatt
                megvett_termekek.append({
                    "Termék Neve": nev,
                    "Ár ($)": ar_szam,
                    "Vásárlás Időpontja": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                logging.info(f"Kosárba téve: {nev}")
    except Exception as e:
        logging.error(f"Hiba a vásárlás során: {e}")

def jelentes_iras_excel(): # <--- Átnevezve a modern változatra
    try:
        if not megvett_termekek:
            logging.info("Nem történt vásárlás, nem készül Excel.")
            return

        # Pandas táblázat készítése a listából
        df = pd.DataFrame(megvett_termekek)
        
        most = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fajlnev = f"riport_{most}.xlsx"
        
        # Mentés Excelbe
        df.to_excel(fajlnev, index=False)
        
        print(f"Excel riport elkészült: {fajlnev}")
        logging.info(f"Excel riport sikeresen mentve: {fajlnev}")
    except Exception as e:
        logging.error(f"Nem sikerült az Excel jelentés írása: {e}")

# --- FŐ PROGRAMFUTTATÁS ---

if __name__ == "__main__":
    try:
        bejelentkezes()
        vasarlas(20.00) 
        jelentes_iras_excel() # Most már az Excelt hívjuk meg!
    except Exception as e:
        print(f"Váratlan hiba történt a futás során: {e}")
    finally:
        driver.quit()
        print("Böngésző bezárva, program vége.")
