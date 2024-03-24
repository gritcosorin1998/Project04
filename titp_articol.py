import pandas as pd
import requests
from bs4 import BeautifulSoup
import certifi
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def extrage_text(url):
    try:

        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/106.0.0.0 Safari/537.36'}
        print(url)
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        session.mount('http://', adapter)

        response = session.get(url, headers=headers)
        response.raise_for_status()
        # print(response.status_code)

        if response.status_code == 200:
            # Parsăm conținutul paginii folosind BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extragem textul din toate tag-urile <p> (paragrafe)
            paragrafe = soup.find_all('p')

            # Construim textul final
            text_final = ''
            for paragraf in paragrafe:
                text_final += paragraf.get_text() + '\n'

            return sterge_linii_noi_spatii(text_final)
        else:
            # Dacă cererea nu a reușit, afișăm un mesaj de eroare
            print("Eroare la preluarea paginii:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        return None


def sterge_linii_noi_spatii(sir):
    sir_final = ""
    linii = sir.split("\n")
    for linie in linii:
        linie = linie.strip()
        if linie:
            sir_final += linie + "\n"
    return sir_final


def adauga_text_articol(fisier_csv):
    # Citim CSV-ul cu nume de coloane implicite
    df = pd.read_csv(fisier_csv, header=None)

    # Parcurgem fiecare rând din DataFrame
    for index, row in df.iterrows():
        url = row.iloc[4]  # Assuming the URL is in the 7th column

        text_pagina = extrage_text(url)
        print(text_pagina)
        if text_pagina is not None:
            # Adaugăm textul la DataFrame
            df.at[index, 5] = text_pagina  # Assuming the text will be inserted in the 8th column

    # Salvăm DataFrame-ul actualizat în același fișier CSV
    df.to_csv(fisier_csv, index=False)
#
# fisier_input = 'database.csv'
# adauga_text_articol(fisier_input)
