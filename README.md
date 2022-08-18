# ENGETO PROJEKT 3

Třetí projekt na Python Akademii od Engeta.

## Popis projektu
Tento projekt slouží k extrahování výsledků parlamentních voleb v roce 2017. Odkaz k prohlednutí najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven
Knihovny, které jsou použity v kódu, jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s naistalovaným manažerem spustit následovně:
```
$ pip3 --version                # overim verzi manazeru
$ pip3 install -r requirements  # naistalujeme knihovny
```

## Spuštění projektu
Spuštění souboru `Election_Scraper.py` v rámci příkazového rádku požaduje dva povinné argumenty.
```
python3 Election_Scraper.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

## Ukázka projektu
Výsledky hlasování pro okres Třebíč:

1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104`
2. argument: `vysledky_Třebíč.csv`

Spuštění programu:
```
python3 Election_Scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104' 'vysledky_Třebíč.csv'
```
Průběh stahování:
```
STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104
UKLADAM DO SOUBORU: 'vysledky_Třebíč.csv'
UKONCUJI Election_scraper.py
```
Částečný výstup:
```
code,town,voters,envelopes,valid votes,...
590282,Bačice,165,104,104,1,1,0,5,0,6,23,0,1,0,0,0,5,1,2,33,1,7,0,0,0,0,14,4
544833,Bačkovice,88,53,52,1,0,0,9,0,1,7,0,1,0,0,0,3,0,3,18,0,5,0,0,0,0,4,0
...
```
