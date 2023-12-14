import time
import os
import math
import csv
import base64
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


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

picture_box_element = ".fR600b"
all_pictures = "#yDmH0d > div.T1diZc.KWE8qe > c-wiz > div.mJxzWe"


def scroll_down(driver):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


def search(found_count, search_query, max_count):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://images.google.com/")
    elem = driver.find_element(By.CSS_SELECTOR, "#APjFqb")
    elem.clear()
    elem.send_keys(search_query)
    elem.send_keys(Keys.RETURN)
    while found_count < max_count:
        # Rechercher les éléments avec la classe spécifiée
        elements = driver.find_elements(By.CSS_SELECTOR, picture_box_element)
        # Incrémenter le compteur d'éléments trouvés
        found_count += len(elements)
        # Faire défiler la page
        scroll_down(driver)
        wait = WebDriverWait(driver, 10)
    scroll_down(driver)
    wait = WebDriverWait(driver, 10)
    section_html = driver.find_element(
        By.CSS_SELECTOR, all_pictures).get_attribute("innerHTML")
    driver.close()
    soup = BeautifulSoup(section_html, 'html.parser').find_all(
        'div', class_=['fR600b', 'islir'])
    return soup


def get_all_images_link(soup):
    images = []
    if (soup):
        for image_card in soup:
            img = image_card.find('img').get('src')
            images.append(img)
    return images


def load_data(folder, images, title="images"):
    if images is None:
        # Gérer le cas où images est None
        print("La liste d'images est Vide.")
        return

    if not os.path.exists(f'result/{folder}'):
        os.makedirs(f'result/{folder}')
    with open(f'result/{folder}/{title}.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['index', 'src']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # On initialise un compteur d'index.
        index = 1
        for image in images:
            # Créer un nouveau dictionnaire pour chaque image avec les clés 'index' et 'src'
            if (image):
                image_data = {'index': index, 'src': image}
                writer.writerow(image_data)
                index += 1
    images = []


# Cherche {number} photos de chien et Stock dans un fichier csv : Renvoie Minimum 500 ohhhh même si vous spécifiez moins
def searchDogPictures(number):
    category = "chien"
    racesNumber = len(races_de_chiens)
    images_per_race = math.ceil(number/racesNumber)
    images = []
    for race in races_de_chiens:
        found_count = 0
        search_query = f"{category} {race}"
        soup = search(found_count, search_query, images_per_race)
        images.extend(get_all_images_link(soup))
    load_data(category, images)


# Parcours le fichier csv soumis via csv_path et télécharges les images dans le folder spécifié
def download_images_from_csv(csv_path, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            index = row['index']
            src = row['src']
            if src.startswith("data"):
                # Ignorer la partie 'data:image/jpeg;base64,'
                base64_data = row['src'].split(',')[1]
                try:
                    # Décodez la chaîne base64 pour obtenir les données binaires de l'image
                    image_data = base64.b64decode(base64_data)

                    # Utilisez PIL pour créer une image à partir des données binaires
                    image = Image.open(BytesIO(image_data))

                    # Construire le chemin du fichier local
                    file_path = os.path.join(folder, f'image_{index}.jpg')

                    # Enregistrez l'image dans le fichier local
                    image.save(file_path, 'JPEG')
                    print(
                        f"Image {index} téléchargée avec succès dans {file_path}")
                except Exception as e:
                    print(f"Échec du téléchargement de l'image {index}: {e}")
            else:
                try:
                    # Utilisez requests pour télécharger l'image
                    response = requests.get(src)

                    if response.status_code == 200:
                        # Extraire le nom du fichier à partir de l'URL
                        file_name = os.path.basename(urlparse(src).path)

                        # Construire le chemin du fichier local
                        file_path = os.path.join(
                            folder, f'image_{index}_{file_name}.jpg')

                        # Enregistrez l'image dans le fichier local
                        with open(file_path, 'wb') as local_file:
                            local_file.write(response.content)
                            print(
                                f"Image {index} téléchargée avec succès dans {file_path}")
                    else:
                        print(
                            f"Échec du téléchargement de l'image {index}: Code de statut {response.status_code}")
                except Exception as e:
                    print(f"Échec du téléchargement de l'image {index}: {e}")
                    # print("La variable src ne commence pas par 'data'")


def __main__():
    searchDogPictures(25000)
    download_images_from_csv('result/chien/images.csv', 'images_chien')


__main__()
