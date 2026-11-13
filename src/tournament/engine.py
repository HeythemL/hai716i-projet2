"""
Moteur du tournoi - Partie et tournoi round-robin.
Code simple, sans types compliqués.
"""

import random
from .gains import gain, C, D


def jouer_partie(strat_i, strat_j, nb_tours=200, seed=None):
    """
    Joue une partie entre deux stratégies.

    Args:
        strat_i: fonction(historique_moi, historique_adv, tour) -> C ou D
        strat_j: fonction(historique_moi, historique_adv, tour) -> C ou D
        nb_tours: nombre de tours (défaut 200)
        seed: graine aléatoire pour reproductibilité

    Returns:
        dict avec keys: 'score_i', 'score_j', 'historique'
    """
    if seed is not None:
        random.seed(seed)

    historique = []
    score_i = 0
    score_j = 0

    # Listes d'actions pour chaque joueur (leur point de vue)
    actions_i = []
    actions_j = []

    for tour in range(nb_tours):
        # Chaque stratégie choisit son action basée sur SON historique
        action_i = strat_i(actions_i, actions_j, tour)
        action_j = strat_j(actions_j, actions_i, tour)

        # Calculer les gains
        g_i, g_j = gain(action_i, action_j)
        score_i += g_i
        score_j += g_j

        # Enregistrer les actions
        actions_i.append(action_i)
        actions_j.append(action_j)
        historique.append((action_i, action_j))

    return {
        'score_i': score_i,
        'score_j': score_j,
        'historique': historique
    }


def jouer_tournoi(strategies, nb_parties=5, nb_tours=200, seed=42):
    """
    Tournoi round-robin : chaque stratégie affronte chaque autre.

    Args:
        strategies: dict {nom: fonction_strategie}
        nb_parties: nombre de parties par paire (défaut 5)
        nb_tours: tours par partie (défaut 200)
        seed: graine aléatoire

    Returns:
        dict {nom_strategie: score_total}
    """
    random.seed(seed)

    noms = list(strategies.keys())
    scores_totaux = {nom: 0 for nom in noms}

    # Chaque paire joue nb_parties fois
    for i in range(len(noms)):
        for j in range(i + 1, len(noms)):
            nom_i = noms[i]
            nom_j = noms[j]
            strat_i = strategies[nom_i]
            strat_j = strategies[nom_j]

            for partie in range(nb_parties):
                # Seed différent pour chaque partie
                resultat = jouer_partie(strat_i, strat_j, nb_tours, seed + partie * 1000 + i * 100 + j)

                scores_totaux[nom_i] += resultat['score_i']
                scores_totaux[nom_j] += resultat['score_j']

    return scores_totaux


def afficher_classement(scores):
    """Affiche un joli classement trié par score décroissant."""
    print("\n" + "=" * 40)
    print("CLASSEMENT FINAL")
    print("=" * 40)
    print(f"{'Rang':<5} {'Stratégie':<20} {'Score':>10}")
    print("-" * 40)

    # Trier par score décroissant
    tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for rang, (nom, score) in enumerate(tries, 1):
        print(f"{rang:<5} {nom:<20} {score:>10}")

    print("=" * 40)


if __name__ == "__main__":
    # Test rapide avec stratégies basiques
    def all_d(hist_moi, hist_adv, tour):
        return D

    def random_strat(hist_moi, hist_adv, tour):
        return random.choice([C, D])

    strategies_test = {
        'ALL-D': all_d,
        'RANDOM': random_strat,
    }

    print("Test moteur avec 2 stratégies...")
    scores = jouer_tournoi(strategies_test, nb_parties=2, nb_tours=10, seed=42)
    afficher_classement(scores)

    # Test une partie seule
    print("\nTest une partie seule (5 tours) :")
    resultat = jouer_partie(all_d, random_strat, nb_tours=5, seed=123)
    print(f"Score ALL-D: {resultat['score_i']}")
    print(f"Score RANDOM: {resultat['score_j']}")
    print(f"Historique: {resultat['historique']}")