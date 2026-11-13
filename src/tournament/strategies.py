"""
Stratégies pour le dilemme du prisonnier itéré.

Chaque stratégie est une fonction :
    def strategie(historique_moi, historique_adv, tour) -> C ou D

- historique_moi : liste de mes actions passées ['C', 'D', ...]
- historique_adv : liste des actions passées de l'adversaire
- tour : numéro du tour actuel (0 = premier tour)
"""

import random
from .gains import C, D


# ============================================================
# STRATÉGIES DE BASE (5 du cours)
# ============================================================

def all_d(historique_moi, historique_adv, tour):
    """Toujours défectionner. Stratégie la plus agressive."""
    return D


def random_strat(historique_moi, historique_adv, tour):
    """Joue C ou D au hasard avec probabilité 50/50."""
    return random.choice([C, D])


def tit_for_tat(historique_moi, historique_adv, tour):
    """
    TIT-FOR-TAT (Axelrod 1980) :
    - Tour 0 : coopère (C)
    - Tours suivants : copie le dernier coup de l'adversaire
    """
    if tour == 0:
        return C
    return historique_adv[-1]


def tester(historique_moi, historique_adv, tour):
    """
    TESTER (Axelrod 1980) :
    - Tour 0 : trahit (D) pour tester la réaction
    - Si l'adversaire a riposté (joué D au tour 1) : joue TIT-FOR-TAT ensuite
    - Si l'adversaire n'a pas riposté (joué C au tour 1) : exploite en alternant C et D
    """
    if tour == 0:
        return D
    # Tour 1 : on attend la réponse de l'adversaire au test
    if tour == 1:
        return C
    # À partir du tour 2 : on décide selon la réaction au tour 0
    adversaire_a_riposte = (historique_adv[1] == D)
    if adversaire_a_riposte:
        # L'adversaire a riposté → on joue TIT-FOR-TAT (coopératif)
        return historique_adv[-1]
    else:
        # L'adversaire n'a pas riposté → on l'exploite (alterne D/C)
        if tour % 2 == 0:
            return D
        else:
            return C


def joss(historique_moi, historique_adv, tour):
    """
    JOSS (Axelrod 1980) :
    - Variante sournoise de TIT-FOR-TAT
    - Tour 0 : coopère (C)
    - Tours suivants : copie l'adversaire MAIS avec 10% de chance de trahir
      même quand l'adversaire a coopéré
    """
    if tour == 0:
        return C
    # Copie le dernier coup adverse
    coup = historique_adv[-1]
    # Mais avec 10% de chance de trahir à la place de coopérer
    if coup == C and random.random() < 0.1:
        return D
    return coup


# ============================================================
# DICTIONNAIRE DES 5 STRATÉGIES DE BASE
# ============================================================

STRATEGIES_BASE = {
    "ALL-D": all_d,
    "RANDOM": random_strat,
    "TIT-FOR-TAT": tit_for_tat,
    "TESTER": tester,
    "JOSS": joss,
}

