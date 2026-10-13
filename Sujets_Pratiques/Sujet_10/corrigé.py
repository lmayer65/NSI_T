# -*- coding: utf-8 -*-
"""
Corrigé Python - Bac NSI 2026 - Épreuve pratique - Sujet 10
Thème : analyse de consommation d'eau, listes de dictionnaires et lissage
"""

from __future__ import annotations


donnees = [
    {"jour": "2025-02-04", "heure": "00:00", "chaude": 2, "froide": 3},
    {"jour": "2025-02-04", "heure": "01:00", "chaude": 1, "froide": 2},
    {"jour": "2025-02-04", "heure": "02:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "03:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "04:00", "chaude": 0, "froide": 1},
    {"jour": "2025-02-04", "heure": "05:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "06:00", "chaude": 4, "froide": 6},
    {"jour": "2025-02-04", "heure": "07:00", "chaude": 6, "froide": 8},
    {"jour": "2025-02-05", "heure": "00:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "01:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "02:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "03:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "04:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "05:00", "chaude": 0, "froide": 0},
]

# Question 1 
def total_conso(donnees: list[dict], jour: str) -> int:
    """Renvoie la consommation totale d'eau chaude et froide pour le jour donné."""
    total = 0
    jour_dans_les_donnees = False 
    for mesure in donnees:
        if mesure["jour"] == jour:
            jour_dans_les_donnees = True
            total += mesure["chaude"] + mesure["froide"]
    if jour_dans_les_donnees:
        return total
    else:
        return None

# Question 2 : solution 1
def fuite_possible(donnees: list[dict], jour: str) -> bool:
    """
    Renvoie True s'il existe au moins trois mesures nocturnes consécutives non
    nulles entre 00:00 et 05:00 inclus.
    """
    consecutives = 0
    for heure in ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"]:
        conso = 0
        for mesure in donnees:
            if mesure["jour"] == jour and mesure["heure"] == heure:
                conso = mesure["chaude"] + mesure["froide"]
        if conso > 0:
            consecutives += 1
            if consecutives >= 3:
                return True
        else:
            consecutives = 0
    return False

# Question 2 : solution 2
def fuite_possible2(donnees, jour):
    serie = 0
    for mesure in donnees:
        if mesure["jour"] == jour:
            if mesure["heure"] >= "00:00" and mesure["heure"] <= "05:00":
                if mesure["chaude"] + mesure["froide"] >0 and serie<3:
                    serie+=1
                    if serie>2:
                        return True
                else:
                    serie=0
    return False

# Question 3

def lissage_conso(valeurs: list[float]) -> list[float]:
    """
    Calcule une moyenne glissante en conservant une liste de même longueur.
    """
    if len(valeurs) == 0:
        return []
    if len(valeurs) == 1:
        return valeurs.copy()

    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[0] + valeurs[1]) / 2
        elif i == len(valeurs) - 1:
            m = (valeurs[-2] + valeurs[-1]) / 2
        else:
            m = (valeurs[i - 1] + valeurs[i] + valeurs[i + 1]) / 3 # on doit diviser les 3 valeurs par 3
        lisse.append(m)
    return lisse

# ******************************************************************
def tests() -> None:
    assert total_conso(donnees, "2025-02-04") == 33
    assert total_conso(donnees, "2025-12-25") == None
    assert fuite_possible(donnees, "2025-02-04") is False
    assert fuite_possible(donnees, "2025-02-05") is True
    assert fuite_possible2(donnees, "2025-02-04") is False
    assert fuite_possible2(donnees, "2025-02-05") is True
    assert lissage_conso([10, 20, 30, 40, 50]) == [15, 20, 30, 40, 45]
    assert lissage_conso([10, 20]) == [15, 15]
    assert lissage_conso([10]) == [10]
    assert lissage_conso([]) == []
    print("Tous les tests du sujet 10 sont passés.")


if __name__ == "__main__":
    tests()
