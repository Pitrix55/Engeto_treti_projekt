"""
projekt_3.py: Třetí projekt do Engeto Online Python Akademie
author: Petr Vodák
email: vodak.petr10@seznam.cz
discord: (Petr V.) Pitrix#0619
"""

import os
import sys
import csv


from bs4 import BeautifulSoup
import requests


def kontrola_poctu_arg(argumenty):
    if len(argumenty) != 3:
        print("Nesprávný počet argumentů! Zadejte přesně 2 argumenty..")
        quit()


def kontrola_prvniho_arg(prvni_arg):
    url_okres = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    html_okres = requests.get(url_okres)
    soup_okresu = BeautifulSoup(html_okres.text, 'html.parser')

    def zpracovani_td_hlavicek():
        td_vysledek = []
        table_pocet = len(soup_okresu.find_all('table', {'class': 'table'}))
        for cislo in range(1, table_pocet + 1):
            td_vysledek.extend(soup_okresu.find_all('td', {'headers': f't{cislo}sa3'}))
        return td_vysledek

    td_tagy = zpracovani_td_hlavicek()
    okresy = ["https://volby.cz/pls/ps2017nss/" + (td_tag.a['href'])
                    for td_tag in td_tagy]
    if prvni_arg not in okresy:
        print("Neplatná webová adresa okresu!")
        quit()


def okres_soup():
    url = sys.argv[1]
    strana_okresu = requests.get(url)
    return BeautifulSoup(strana_okresu.text, 'html.parser')


def jmeno_souboru():
    div_topline = okres_soup().find('div', {'class': 'topline'})
    okres_jmeno_tag = div_topline.find_all('h3')[1]
    okres_jmeno_raw = okres_jmeno_tag.text
    okres_jmeno = okres_jmeno_raw.strip().lstrip('Okres: ')
    return f"vysledky_{okres_jmeno}.csv"


def kontrola_druheho_arg(druhy_arg, nazev_souboru_csv):
    if druhy_arg != nazev_souboru_csv:
        print("Nesprávný název csv souboru!  Správný formát: 'vysledky_<nazev_okresu>.csv'")
        quit()


def obce():
    div_inner = okres_soup().find('div', {'id': 'inner'})
    tr_tagy = div_inner.find_all('tr')
    return tr_tagy


def statistiky(tag_tr, obec_tag):
    link_tag = tag_tr.find('td', {'class': 'cislo'})
    obec_link_tag = link_tag.a

    def obec_soup(link_tag_obce):
        obec_link = link_tag_obce["href"]
        obec_url = f"https://volby.cz/pls/ps2017nss/{obec_link}"
        strana_obce = requests.get(obec_url)
        return BeautifulSoup(strana_obce.text, 'html.parser')

    def zakladni_statistiky(tag_obec, obec_link_tag):
        div_tag = obec_soup(obec_link_tag).find('div', {'id': 'publikace'})
        volici_statistika = div_tag.table.find_all('td')

        nazev_obce = tag_obec.text
        kod_obce = obec_link_tag.text
        volici_v_seznamu = volici_statistika[3].text
        vydane_obalky = volici_statistika[4].text
        platne_hlasy = volici_statistika[7].text

        return {'code': kod_obce, 'town': nazev_obce, 'voters': volici_v_seznamu,
                'envelopes': vydane_obalky, 'valid votes': platne_hlasy}

    def politicke_strany():
        div_inner = obec_soup(obec_link_tag).find('div', {'id': 'inner'})
        strany = [tag.text for tag in (div_inner.find_all('td', {'class': 'overflow_name'}))]
        hlasy_1 = [tag.text for tag in (div_inner.find_all('td', {'headers': 't1sa2 t1sb3'}))]
        hlasy_2 = [tag.text for tag in (div_inner.find_all('td', {'headers': 't2sa2 t2sb3'}))]

        hlasy_pro_strany = hlasy_1 + hlasy_2
        strany_a_volici = {strany[i]: hlasy_pro_strany[i]
                             for i in range(len(strany))}
        return strany_a_volici

    statistika_slovnik = {}
    statistika_slovnik.update(zakladni_statistiky(obec_tag, obec_link_tag))
    statistika_slovnik.update(politicke_strany())
    return statistika_slovnik


def ulozeni_do_souboru(statistiky_slovnik):
    soubor = open(jmeno_souboru(), mode='a', newline='\n')
    prvni_radek = list(statistiky_slovnik.keys())
    zapis = csv.DictWriter(soubor, prvni_radek)
    if os.path.getsize(jmeno_souboru()) == 0:
        zapis.writeheader()
    else:
        zapis.writerow(statistiky_slovnik)
    soubor.close()


def zpracovani_dat():
    for tr_tag in obce():
        obec_tag = tr_tag.find('td', {'class': 'overflow_name'})
        if obec_tag is None:
            continue
        else:
            ulozeni_do_souboru(statistiky(tr_tag, obec_tag))

kontrola_poctu_arg(sys.argv)
kontrola_prvniho_arg(sys.argv[1])
kontrola_druheho_arg(sys.argv[2], jmeno_souboru())


novy_soubor = open(jmeno_souboru(), mode="w")
novy_soubor.close()


print(f"STAHUJI DATA Z VYBRANEHO URL: {sys.argv[1]}")
zpracovani_dat()
print(f"UKLADAM DO SOUBORU: '{jmeno_souboru()}'")
print("UKONCUJI Election_scraper.py")
