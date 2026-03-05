"""
Corrigé (programme Python) — Bac pratique NSI (sujet 1)

Fichiers fournis dans le sujet :
- donnees.py : petit jeu de données "employes" :contentReference[oaicite:0]{index=0}
- donnees_completes.py : jeu de données plus complet (même structure) :contentReference[oaicite:1]{index=1}
- analyse.py : squelette à compléter (fonctions + tests) :contentReference[oaicite:2]{index=2}

Ce programme :
1) implémente les fonctions manquantes
2) corrige la fonction calcul_ecart_sexe (bugs + formule)
3) conserve les fonctions KNN (k plus proches voisins) et fournit des tests
"""

import donnees
import donnees_completes
from math import sqrt


# ------------------------------------------------------------
# 1) Statistiques conditionnelles
# ------------------------------------------------------------

def salaire_moyen_condition(employes, champ, valeur):
    """
    Renvoie le salaire moyen des employés ayant 'valeur' pour le champ 'champ'.
    Exemple : champ='sexe', valeur='F' -> moyenne des salaires des femmes.

    Si aucun employé ne vérifie la condition, renvoie None.
    """
    somme = 0
    compteur = 0

    for e in employes:
        if e[champ] == valeur:
            somme += e['salaire']
            compteur += 1

    if compteur == 0:
        return None
    return somme / compteur


def test_salaire_moyen_condition():
    e = donnees.employes
    assert salaire_moyen_condition([], 'sexe', 'F') is None
    assert salaire_moyen_condition(e, 'sexe', 'F') == 2400.0
    assert salaire_moyen_condition(e, 'etudes', 3) == 2550.0
    assert salaire_moyen_condition(e, 'etudes', 12) is None


# ------------------------------------------------------------
# 2) Effectifs
# ------------------------------------------------------------

def effectif_par_sexe(employes):
    """
    Renvoie un dictionnaire {'F': nb_femmes, 'M': nb_hommes}.
    """
    nb_f = 0
    nb_m = 0

    for e in employes:
        if e['sexe'] == 'F':
            nb_f += 1
        else:
            nb_m += 1

    return {'F': nb_f, 'M': nb_m}


def test_effectif_par_sexe():
    e = donnees.employes
    assert effectif_par_sexe(e) == {'F': 3, 'M': 3}


# ------------------------------------------------------------
# 3) Écart de salaire (femmes par rapport aux hommes)
# ------------------------------------------------------------

def calcul_ecart_sexe(employes):
    """
    Renvoie l'écart de salaire en POURCENTAGE des femmes par rapport aux hommes.

    Convention : écart = ((moy_h - moy_f) / moy_h) * 100

    - Si moy_h ou moy_f n'existe pas (aucun homme ou aucune femme), renvoie None.
    - Exemple : moy_h=3000, moy_f=2700 -> (3000-2700)/3000*100 = 10.0 (%)
    """
    moy_h = salaire_moyen_condition(employes, 'sexe', 'M')
    moy_f = salaire_moyen_condition(employes, 'sexe', 'F')

    if moy_h is None or moy_f is None:
        return None

    return (moy_h - moy_f) / moy_h * 100


def test_calcul_ecart_sexe():
    # cas standard
    e = donnees.employes
    ecart = calcul_ecart_sexe(e)
    assert ecart is not None

    # cas où un sexe manque -> None
    e2 = [{'experience': 1, 'etudes': 3, 'sexe': 'M', 'salaire': 2000}]
    assert calcul_ecart_sexe(e2) is None


# ------------------------------------------------------------
# 4) Attribution d'un salaire par k plus proches voisins (KNN)
# ------------------------------------------------------------

def sexe_vers_entier(e):
    """Encode 'F' en 1 et 'M' en -1."""
    return 1 if e['sexe'] == 'F' else -1


def distance(e1, e2):
    """
    Mesure de distance (euclidienne) entre 2 personnes sur :
    - sexe (encodé)
    - experience
    - etudes
    """
    s = 0
    s += (sexe_vers_entier(e1) - sexe_vers_entier(e2)) ** 2
    s += (e1['experience'] - e2['experience']) ** 2
    s += (e1['etudes'] - e2['etudes']) ** 2
    return sqrt(s)


def k_plus_proches(k, employes, e):
    """
    Renvoie la liste des k employés les plus proches de e.
    On trie des couples (distance, index) par distance croissante.
    """
    # liste de (distance à e, index employé)
    e_d = [(distance(e, employes[i]), i) for i in range(len(employes))]
    e_d.sort()  # tri croissant sur la distance

    voisins = []
    # hypothèse : k <= len(employes)
    for i in range(k):
        voisins.append(employes[e_d[i][1]])
    return voisins


def salaire_moyen(employes):
    """Renvoie le salaire moyen d'une liste d'employés, ou None si vide."""
    if len(employes) == 0:
        return None
    s = sum(e['salaire'] for e in employes)
    return s / len(employes)


def salaire_par_proximite(employes, e):
    """
    Renvoie un salaire estimé pour e en moyennant les 3 plus proches voisins.
    """
    voisins = k_plus_proches(3, employes, e)
    return salaire_moyen(voisins)


def test_knn():
    # On teste juste que ça renvoie un nombre (pas None) avec assez de données
    base = donnees.employes
    nouvel_employe = {'experience': 4, 'etudes': 3, 'sexe': 'F'}
    estimation = salaire_par_proximite(base, nouvel_employe)
    assert estimation is not None
    assert isinstance(estimation, (int, float))


# ------------------------------------------------------------
# 5) Programme principal : lance les tests + exemples
# ------------------------------------------------------------

def main():
    # Tests (style bac pratique : assertions)
    test_salaire_moyen_condition()
    test_effectif_par_sexe()
    test_calcul_ecart_sexe()
    test_knn()

    # Exemples d'affichage sur les données de donnees.py
    e = donnees.employes

    print("=== Données (donnees.py) ===")
    print("Effectif par sexe :", effectif_par_sexe(e))
    print("Salaire moyen femmes :", salaire_moyen_condition(e, 'sexe', 'F'))
    print("Salaire moyen hommes :", salaire_moyen_condition(e, 'sexe', 'M'))
    print("Écart (%) femmes par rapport aux hommes :", calcul_ecart_sexe(e))

    # Exemple KNN
    nouvel_employe = {'experience': 4, 'etudes': 3, 'sexe': 'F'}
    print("Salaire estimé (KNN, k=3) pour", nouvel_employe, ":", salaire_par_proximite(e, nouvel_employe))

    # Optionnel : même calcul sur le jeu complet si disponible
    e_full = donnees_completes.employes
    print("\n=== Données (donnees_completes.py) ===")
    print("Effectif par sexe :", effectif_par_sexe(e_full))
    print("Écart (%) femmes par rapport aux hommes :", calcul_ecart_sexe(e_full))





