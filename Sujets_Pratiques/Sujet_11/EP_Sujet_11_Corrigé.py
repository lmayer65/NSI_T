# -*- coding: utf-8 -*-
"""
Corrigé Python - Bac NSI 2026 - Épreuve pratique - Sujet 11
Thème : prédiction d'habitat avec distance euclidienne et k plus proches voisins
"""

from __future__ import annotations

from math import sqrt


nouveau = {"vegetation": 5, "proximite_eau": 2, "densite_urbaine": 4, "disponibilite_proies": 6}

zones_connues = [
    {"vegetation": 9, "proximite_eau": 6, "densite_urbaine": 0, "disponibilite_proies": 4, "presence_renard": True},
    {"vegetation": 10, "proximite_eau": 5, "densite_urbaine": 9, "disponibilite_proies": 10, "presence_renard": False},
    {"vegetation": 8, "proximite_eau": 5, "densite_urbaine": 1, "disponibilite_proies": 6, "presence_renard": False},
    {"vegetation": 8, "proximite_eau": 5, "densite_urbaine": 7, "disponibilite_proies": 6, "presence_renard": True},
    {"vegetation": 6, "proximite_eau": 9, "densite_urbaine": 9, "disponibilite_proies": 6, "presence_renard": True},
]


def distance(habitat_1: dict, habitat_2: dict) -> float:
    """Renvoie la distance euclidienne entre deux habitats."""
    return sqrt(
        (habitat_1["vegetation"] - habitat_2["vegetation"]) ** 2
        + (habitat_1["proximite_eau"] - habitat_2["proximite_eau"]) ** 2
        + (habitat_1["densite_urbaine"] - habitat_2["densite_urbaine"]) ** 2
        + (habitat_1["disponibilite_proies"] - habitat_2["disponibilite_proies"]) ** 2
    )


def distance_d_un_habitat(habitat: dict, habitats: list[dict]) -> list[tuple[float, dict]]:
    """Renvoie la liste des couples (distance, habitat connu)."""
    return [(distance(habitat, h), h) for h in habitats]


def premiere_composante(c: tuple) -> float:
    return c[0]


def k_plus_proches(k: int, habitat: dict, habitats: list[dict]) -> list[tuple[float, dict]]:
    distances = distance_d_un_habitat(habitat, habitats)
    distances.sort(key=premiere_composante)
    return distances[:k]


def presence_renard(k: int, habitat: dict, habitats: list[dict]) -> bool:
    """Renvoie True si plus de la moitié des k voisins contiennent un renard."""
    voisins = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for _, caracteristiques in voisins:
        if caracteristiques["presence_renard"]:
            n_renards += 1
    return n_renards > k / 2


def tests() -> None:
    resultats = distance_d_un_habitat(nouveau, zones_connues)
    assert abs(resultats[0][0] - 7.211102550927978) < 1e-12
    assert abs(resultats[1][0] - 8.660254037844387) < 1e-12
    assert abs(resultats[2][0] - 5.196152422706632) < 1e-12
    assert len(k_plus_proches(3, nouveau, zones_connues)) == 3
    assert isinstance(presence_renard(3, nouveau, zones_connues), bool)
    print("Tous les tests du sujet 11 sont passés.")


if __name__ == "__main__":
    tests()
