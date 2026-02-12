from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# --- ALAPBEÁLLÍTÁSOK ---
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-notifications")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Globális lista, amibe gyűjtjük, mit vettünk (hogy a jelentésíró is lássa)
megvett_termekek = []

# --- 1. LECKE: A "BEJELENTKEZÉS" PARANCS ---
def bejelentkezes():
    print("--- 1. LÉPÉS: Bejelentkezés indítása ---")
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    time.sleep(1)
    
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    print("Sikeresen beléptünk!")
    time.sleep(2)

# --- 2. LECKE: A "VÁSÁRLÁS" PARANCS ---
# A zárójelben lévő 'ar_limit' azt jelenti: ezt majd megmondhatjuk neki híváskor!
def vasarlas(ar_limit):
    print(f"--- 2. LÉPÉS: Vásárlás ${ar_limit} alatt ---")
    
    ar_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    nev_elemek = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    gombok = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    
    for i in range(len(ar_elemek)):
        szoveg = ar_elemek[i].text.replace("$", "")
        szam = float(szoveg)
        nev = nev_elemek[i].text
        
        if szam < ar_limit:
            gombok[i].click()
            # Hozzáadjuk a közös listához, hogy emlékezzünk rá
            megvett_termekek.append(f"{nev} - ${szam}")
            print(f"Kosárba téve: {nev}")

# --- 3. LECKE: A "JELENTÉS" PARANCS ---
def jelentes_iras():
    print("--- 3. LÉPÉS: Jelentés írása ---")
    with open("profi_jelentes.txt", "w", encoding="utf-8") as fajl:
        fajl.write("VÁSÁRLÁSI RIPORT\n")
        fajl.write("----------------\n")
        for t in megvett_termekek:
            fajl.write(f"Megvett tétel: {t}\n")
        fajl.write("----------------\n")
        fajl.write(f"Összesen: {len(megvett_termekek)} db termék.\n")
    print("Fájl elmentve: profi_jelentes.txt")

# ==========================================
# --- A FŐVEZÉRLŐ KÖZPONT (MAIN) ---
# Itt hívjuk meg a parancsokat!
# ==========================================

try:
    # 1. Parancs: Lépj be!
    bejelentkezes()

    # 2. Parancs: Vásárolj be 15 dollár alatt!
    # Látod? Itt adom meg a számot. Ha 50-et írnék, drágábbakat is venne.
    vasarlas(50.00)

    # 3. Parancs: Írd meg a jelentést!
    jelentes_iras()

    input("Nyomj ENTER-t a kilépéshez...")

except Exception as e:
    print(f"Valami hiba történt: {e}")

finally:
    # A 'finally' blokk MINDIG lefut, még hiba esetén is.
    # Így biztosan bezáródik a böngésző.
    driver.quit()
