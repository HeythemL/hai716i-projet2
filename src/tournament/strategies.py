"""
Stratégies pour le dilemme du prisonnier itéré.

Chaque stratégie est une fonction :
    strategie(historique_moi, historique_adv, tour) -> 'C' ou 'D'

- historique_moi : liste de mes actions passées ['C', 'D', ...]
- historique_adv : liste des actions adverses passées
- tour : numéro du tour courant (0-indexé)
"""

import random
from .gains import C, D


def all_d(historique_moi, historique_adv, tour):
    """ALL-D : Défectionne toujours."""
    return D


def random_strat(historique_moi, historique_adv, tour):
    """RANDOM : Choisit C ou D aléatoirement (50/50)."""
    return random.choice([C, D])


# Dictionnaire des stratégies disponibles
STRATEGIES = {
    'ALL-D': all_d,
    'RANDOM': random_strat,
}


if __name__ == "__main__":
    print("Stratégies disponibles :")
    for nom in STRATEGIES:
        print(f"  - {nom}")