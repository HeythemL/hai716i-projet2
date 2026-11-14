"""
Étape 2 : Tournoi élargi — 7 stratégies (5 de base + 2 nouvelles).

Lance le tournoi avec les 2 stratégies supplémentaires (GRIM, PAVLOV)
et compare les résultats avec l'Étape 1.
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

    print("=" * 50)
    print("ÉTAPE 2 : TOURNOI ÉLARGI (7 stratégies)")
    print("=" * 50)
    print(f"Seed: {SEED}")
    print(f"Parties par paire: {NB_PARTIES}")
    print(f"Tours par partie: {NB_TOURS}")
    print(f"Stratégies: {list(STRATEGIES.keys())}")
    print()

    # Lancer le tournoi
    scores = jouer_tournoi(STRATEGIES, nb_parties=NB_PARTIES, nb_tours=NB_TOURS, seed=SEED)

    # Afficher le classement
    afficher_classement(scores)

    # Sauvegarder en CSV
    sauvegarder_csv(scores, os.path.join('outputs', 'etape2_classement.csv'))

    # Comparer avec l'Étape 1
    print("\n--- Comparaison Étape 1 vs Étape 2 ---")
    tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for rang, (nom, score) in enumerate(tries, 1):
        print(f"  {rang}. {nom}: {score}")

    return scores


if __name__ == "__main__":
    main()