# -*- coding: utf-8 -*-
"""
Corrigé Python - Bac NSI 2026 - Épreuve pratique - Sujet 17
Thème : analyse budgétaire d'un club de handball et fichiers CSV
"""

from __future__ import annotations

import csv


def lire_mouvements_depuis_csv(nom_fichier_csv: str) -> list[dict]:
    mouvements_csv = []
    with open(nom_fichier_csv, mode="r", newline="", encoding="utf-8") as fichier_csv:
        lecteur_csv = csv.DictReader(fichier_csv)
        for ligne in lecteur_csv:
            ligne["montant"] = float(ligne["montant"])
            ligne["mois"] = int(ligne["mois"])
            mouvements_csv.append(ligne)
    return mouvements_csv


mouvements_test = [
    {"type": "recette", "catégorie": "cotisations", "montant": 1200.0, "mois": 1},
    {"type": "recette", "catégorie": "billetterie", "montant": 300.0, "mois": 6},
    {"type": "dépense", "catégorie": "fonctionnement", "montant": 450.0, "mois": 6},
    {"type": "dépense", "catégorie": "déplacements", "montant": 200.0, "mois": 12},
    {"type": "dépense", "catégorie": "salaires", "montant": 1500.0, "mois": 12},
    {"type": "recette", "catégorie": "subventions", "montant": 800.0, "mois": 12},
]


def total_par_type(mouvements: list[dict], type_mouvement: str) -> float:
    """Renvoie la somme des montants correspondant au type demandé."""
    total = 0.0
    for mouvement in mouvements:
        if mouvement["type"] == type_mouvement:
            total += mouvement["montant"]
    return total


def test_total() -> None:
    assert total_par_type(mouvements_test, "recette") == 2300.0
    assert total_par_type(mouvements_test, "dépense") == 2150.0
    assert total_par_type(mouvements_test, "autre") == 0


def solde_mensuel(mouvements: list[dict], mois: int) -> float:
    total_recettes = 0.0
    total_depenses = 0.0
    for m in mouvements:
        if m["mois"] == mois:
            if m["type"] == "recette":
                total_recettes += m["montant"]
            else:
                total_depenses += m["montant"]
    return total_recettes - total_depenses


def solde_annuel(mouvements: list[dict]) -> float:
    """Calcule le solde annuel. Correction : il faut inclure le mois 12."""
    total = 0.0
    for mois in range(1, 13):
        total += solde_mensuel(mouvements, mois)
    return total


def test_solde_annuel() -> None:
    assert solde_annuel(mouvements_test) == 150.0


def tests() -> None:
    test_total()
    test_solde_annuel()
    print("Tous les tests du sujet 17 sont passés.")


if __name__ == "__main__":
    tests()
    # mouvements_complets = lire_mouvements_depuis_csv("budget_complet.csv")
    # print("Le solde annuel sur le fichier complet est de :", solde_annuel(mouvements_complets))
