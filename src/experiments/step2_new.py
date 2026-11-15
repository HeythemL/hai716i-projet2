"""
Étape 2 : Tournoi élargi — 9 stratégies (5 de base + 2 A + 2 B).

Lance le tournoi avec les 4 stratégies supplémentaires (GRIM, PAVLOV de A + TFT-2T, PROBER de B)
et compare les résultats avec l'Étape 1.
"""

import os
import sys
import csv
import io
import contextlib

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


def charger_scores_etape1(fichier):
    """Charge les scores de l'Étape 1 depuis le CSV."""
    scores = {}
    if os.path.exists(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scores[row['Strategie']] = int(row['Score'])
    return scores


def sauvegarder_sortie_console(contenu, fichier):
    """Sauvegarde la sortie console dans un fichier texte."""
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu)
    print(f"Sortie console sauvegardée : {fichier}")


def main():
    # ========================================
    # SEED FIXE pour reproductibilité
    # ========================================
    SEED = 42
    NB_PARTIES = 5
    NB_TOURS = 200

    # Capture de la sortie console
    sortie_buffer = io.StringIO()

    with contextlib.redirect_stdout(sortie_buffer):
        print("=" * 50)
        print("ÉTAPE 2 : TOURNOI ÉLARGI (9 stratégies)")
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

        # Charger les résultats de l'Étape 1
        scores_etape1 = charger_scores_etape1(os.path.join('outputs', 'etape1_classement.csv'))

        # Comparer avec l'Étape 1
        print("\n--- Comparaison Étape 1 vs Étape 2 ---")
        print("(5 stratégies communes)")
        tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for rang, (nom, score) in enumerate(tries, 1):
            if nom in scores_etape1:
                diff = score - scores_etape1[nom]
                signe = "+" if diff > 0 else ""
                print(f"  {rang}. {nom}: {score} (Étape 1: {scores_etape1[nom]}, {signe}{diff})")
            else:
                print(f"  {rang}. {nom}: {score} (nouvelle)")

    # Sauvegarder la sortie console
    sortie_console = sortie_buffer.getvalue()
    print(sortie_console)
    sauvegarder_sortie_console(sortie_console, os.path.join('outputs', 'etape2_sortie_console.txt'))

    # Générer les graphiques
    print("\n--- Génération des graphiques ---")
    try:
        from src.experiments.generate_charts import graphique_etape2_comparaison, graphique_etape2_classement
        graphique_etape2_comparaison(scores_etape1, scores)
        graphique_etape2_classement(scores)
    except Exception as e:
        print(f"Erreur génération graphiques: {e}")

    return scores


if __name__ == "__main__":
    main()