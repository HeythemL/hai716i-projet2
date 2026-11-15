"""
Étape 3 : Modification A — Bruit (Noise).

Lance le tournoi avec du bruit (inversion aléatoire des actions)
et compare les résultats avec l'Étape 2 (sans bruit).
"""

import os
import sys
import csv

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tournament.engine import jouer_tournoi, afficher_classement
from src.tournament.strategies import STRATEGIES


def sauvegarder_csv(scores, fichier):
    """Sauvegarde le classement en CSV."""
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    with open(fichier, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rang', 'Strategie', 'Score'])
        for rang, (nom, score) in enumerate(tries, 1):
            writer.writerow([rang, nom, score])
    print(f"\nClassement sauvegardé dans : {fichier}")


def main():
    # ========================================
    # SEED FIXE pour reproductibilité
    # ========================================
    SEED = 42
    NB_PARTIES = 5
    NB_TOURS = 200
    BRIUT = 0.05  # 5% de bruit

    print("=" * 50)
    print("ÉTAPE 3 : TOURNOI AVEC BRUIT (Modification A)")
    print("=" * 50)
    print(f"Seed: {SEED}")
    print(f"Parties par paire: {NB_PARTIES}")
    print(f"Tours par partie: {NB_TOURS}")
    print(f"Bruit: {BRIUT*100}%")
    print(f"Stratégies: {list(STRATEGIES.keys())}")
    print()

    # Lancer le tournoi AVEC bruit
    scores_bruit = jouer_tournoi(STRATEGIES, nb_parties=NB_PARTIES, nb_tours=NB_TOURS, seed=SEED, bruit=BRIUT)

    # Afficher le classement
    afficher_classement(scores_bruit)

    # Sauvegarder en CSV
    sauvegarder_csv(scores_bruit, os.path.join('outputs', 'etape3_bruit_classement.csv'))

    # Comparer avec l'Étape 2 (sans bruit)
    print("\n--- Comparaison Étape 2 (sans bruit) vs Étape 3 (avec bruit 5%) ---")
    scores_sans_bruit = jouer_tournoi(STRATEGIES, nb_parties=NB_PARTIES, nb_tours=NB_TOURS, seed=SEED, bruit=0.0)

    print(f"\n{'Rang':<5} {'Stratégie':<20} {'Sans bruit':>12} {'Avec bruit':>12} {'Diff':>8}")
    print("-" * 65)

    tries_sans = sorted(scores_sans_bruit.items(), key=lambda x: x[1], reverse=True)
    tries_avec = sorted(scores_bruit.items(), key=lambda x: x[1], reverse=True)

    # Créer un dict pour accès rapide
    dict_sans = dict(tries_sans)
    dict_avec = dict(tries_avec)

    for rang, (nom, score_avec) in enumerate(tries_avec, 1):
        score_sans = dict_sans.get(nom, 0)
        diff = score_avec - score_sans
        print(f"{rang:<5} {nom:<20} {score_sans:>12} {score_avec:>12} {diff:>+8}")

    return scores_bruit


if __name__ == "__main__":
    main()