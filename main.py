import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
driver = webdriver.Chrome()

races_de_chiens = [
    "Labrador Retriever",
    "Berger Allemand",
    "Golden Retriever",
    "Bulldog",
    "Caniche",
    "Beagle",
    "Boxer",
    "Chihuahua",
    "Dogue Allemand",
    "Shih Tzu"
]

found_count = 0
picture_box_element = ".fR600b"
all_pictures = "#yDmH0d > div.T1diZc.KWE8qe > c-wiz > div.mJxzWe"

# Fonction pour faire défiler la page
def scroll_down():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1) 

def search(found_count):
    driver.get("https://images.google.com/")
    elem = driver.find_element(By.CSS_SELECTOR, "#APjFqb")
    elem.clear()
    elem.send_keys(f"chien {races_de_chiens[0]}")
    elem.send_keys(Keys.RETURN)
    while found_count < 50:
        # Rechercher les éléments avec la classe spécifiée
        elements = driver.find_elements(By.CSS_SELECTOR, picture_box_element)
        # Incrémenter le compteur d'éléments trouvés
        found_count += len(elements)
        # Faire défiler la page
        scroll_down()
        print(found_count)
    section_html = driver.find_element(By.CSS_SELECTOR, all_pictures).get_attribute("innerHTML")
    soup = BeautifulSoup(section_html, 'html.parser').find_all('div', class_=['fR600b', 'islir'])
    return soup
    

soup = search(found_count)

def get_all_images_link(soup):
    images = 0
    if(soup):
        for image_card in soup:
            images+=1
    print(images)

get_all_images_link(soup)