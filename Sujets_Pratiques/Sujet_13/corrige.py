"""
Corrigé Python - Bac NSI 2026 - Épreuve pratique - Sujet 13
Thème : données climatiques CSV et génération KML
"""

from __future__ import annotations


def recupere_donnees_fichier_csv(nom_fichier: str) -> tuple[list[int], list[float], list[float], list[float]]:
    altitudes = []
    temperatures = []
    longitudes = []
    latitudes = []
    with open(nom_fichier, "r", encoding="utf-8") as contenu_fichier:
        contenu_fichier.readline()
        for ligne in contenu_fichier.readlines():
            valeurs = ligne.rstrip().split(";")
            altitudes.append(int(valeurs[0]))
            temperatures.append(float(valeurs[1]))
            longitudes.append(float(valeurs[2]))
            latitudes.append(float(valeurs[3]))
    return altitudes, temperatures, longitudes, latitudes


# Question 1 :
# altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv("releves_ballon_sonde.csv")


def conversion_K_en_C(liste_temperatures: list[float]) -> list[float]:
    """Convertit des températures de kelvins vers degrés Celsius."""
    return [round(temp - 273.15, 1) for temp in liste_temperatures]


def altitude_la_plus_froide(liste_altitudes: list[int], liste_temperatures: list[float]) -> tuple[float, list[int]]:
    """Renvoie la température minimale et toutes les altitudes correspondantes."""
    temperature_min = min(liste_temperatures)
    altitudes_min = []
    for i in range(len(liste_temperatures)):
        if liste_temperatures[i] == temperature_min:
            altitudes_min.append(liste_altitudes[i])
    return temperature_min, altitudes_min


def genere_kml(liste_longitudes: list[float], liste_latitudes: list[float]) -> None:
    """Génère un fichier KML à partir de listes de longitudes et latitudes."""
    assert len(liste_longitudes) == len(liste_latitudes), "Les deux listes doivent avoir la même longueur."

    with open("ballon sonde.kml", "w", encoding="utf-8") as fichier_kml:
        fichier_kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fichier_kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        fichier_kml.write("<Document>\n")
        fichier_kml.write("<name>Trajectoire ballon sonde</name>\n")

        for i in range(len(liste_longitudes)):
            fichier_kml.write("<Placemark>\n")
            fichier_kml.write(f"<name>Point {i}</name>\n")
            fichier_kml.write("<Point>\n")
            fichier_kml.write(f"<coordinates>{liste_longitudes[i]},{liste_latitudes[i]}</coordinates>\n")
            fichier_kml.write("</Point>\n")
            fichier_kml.write("</Placemark>\n")

        fichier_kml.write("</Document>\n")
        fichier_kml.write("</kml>\n")


def tests() -> None:
    assert conversion_K_en_C([273.15, 293.15, 300]) == [0.0, 20.0, 26.9]
    assert altitude_la_plus_froide([7000, 10125, 13896, 14211], [-35.2, -52.1, -57.4, -57.4]) == (-57.4, [13896, 14211])
    assert altitude_la_plus_froide([6000, 7250, 11542, 15214, 17300], [-33.7, -45, -53, -58.5, -60.1]) == (-60.1, [17300])
    print("Tous les tests du sujet 13 sont passés.")



tests()
