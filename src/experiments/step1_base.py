"""
Étape 1 : Tournoi de base — 5 stratégies du cours.

Lance le tournoi au format Axelrod (5 parties × 200 tours)
et produit un classement + export CSV.
"""

import random
import csv
import os
import sys

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tournament.engine import jouer_tournoi, afficher_classement
from src.tournament.strategies import STRATEGIES_BASE


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

    print("=" * 50)
    print("ÉTAPE 1 : TOURNOI DE BASE")
    print("=" * 50)
    print(f"Seed: {SEED}")
    print(f"Parties par paire: {NB_PARTIES}")
    print(f"Tours par partie: {NB_TOURS}")
    print(f"Stratégies: {list(STRATEGIES_BASE.keys())}")
    print()

    # Lancer le tournoi
    scores = jouer_tournoi(STRATEGIES_BASE, nb_parties=NB_PARTIES, nb_tours=NB_TOURS, seed=SEED)

    # Afficher le classement
    afficher_classement(scores)

    # Sauvegarder en CSV
    sauvegarder_csv(scores, os.path.join('outputs', 'etape1_classement.csv'))

    # Afficher les détails pour l'analyse
    print("\n--- Analyse ---")
    tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    gagnant = tries[0][0]
    print(f"Gagnant : {gagnant}")

    if gagnant == "TIT-FOR-TAT":
        print("→ TIT-FOR-TAT gagne, comme dans le tournoi d'Axelrod 1980.")
    else:
        print(f"→ TIT-FOR-TAT ne gagne PAS (c'est {gagnant} qui gagne).")
        print("  Explication possible : avec seulement 5 stratégies dont")
        print("  ALL-D et TESTER (exploiteuses), TFT ne bénéficie pas de")
        print("  l'effet coopératif du grand tournoi d'Axelrod (14 stratégies).")

    return scores


if __name__ == "__main__":
    main()

