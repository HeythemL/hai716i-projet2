"""
Étape 3 : Modification B — Sélection (Évolution par générations).

Implémente la reproduction proportionnelle aux scores (roulette wheel).
À chaque génération : tournoi complet -> scores -> nouvelle population.
Génère un graphique de l'évolution des parts de population.
"""

import os
import sys
import csv
import io
import contextlib

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tournament.engine import jouer_tournoi
from src.tournament.strategies import STRATEGIES


def generation_suivante(population, scores):
    """
    Calcule la nouvelle distribution de population après sélection.

    Reproduction proportionnelle (Roulette Wheel) :
    La fitness d'une stratégie = son score au tournoi * sa proportion actuelle.

    Args:
        population: dict {nom_strategie: proportion} (somme = 1.0)
        scores: dict {nom_strategie: score_total_au_tournoi}

    Returns:
        dict {nom_strategie: nouvelle_proportion} (somme = 1.0)
    """
    # Fitness pondérée = score * proportion actuelle
    fitness = {nom: scores[nom] * population[nom] for nom in population}
    fitness_total = sum(fitness.values())

    # Nouvelle proportion = fitness / fitness_total
    nouvelle_pop = {nom: fitness[nom] / fitness_total for nom in population}
    return nouvelle_pop


def sauvegarder_csv_evolution(historique_pop, fichier):
    """Sauvegarde l'historique des populations en CSV (lignes = générations, colonnes = stratégies)."""
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    strategies = list(historique_pop[0].keys())

    with open(fichier, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Generation'] + strategies)
        for gen, pop in enumerate(historique_pop):
            writer.writerow([gen] + [pop[s] for s in strategies])
    print(f"Historique évolution sauvegardé : {fichier}")


def sauvegarder_sortie_console(contenu, fichier):
    """Sauvegarde la sortie console dans un fichier texte."""
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu)
    print(f"Sortie console sauvegardée : {fichier}")


def main():
    # ========================================
    # PARAMÈTRES
    # ========================================
    SEED = 42
    NB_PARTIES = 5
    NB_TOURS = 200
    NB_GENERATIONS = 20

    # Population initiale : uniforme
    stratégies_noms = list(STRATEGIES.keys())
    population_initiale = {nom: 1.0 / len(stratégies_noms) for nom in stratégies_noms}

    print("=" * 60)
    print("ÉTAPE 3 : MODIFICATION B — SÉLECTION (ÉVOLUTION)")
    print("=" * 60)
    print(f"Seed: {SEED}")
    print(f"Parties par paire: {NB_PARTIES}")
    print(f"Tours par partie: {NB_TOURS}")
    print(f"Générations: {NB_GENERATIONS}")
    print(f"Stratégies: {stratégies_noms}")
    print()
    print("Population initiale (uniforme):")
    for nom, prop in population_initiale.items():
        print(f"  {nom}: {prop:.4f} ({prop*100:.1f}%)")
    print()

    # Capture de la sortie console
    sortie_buffer = io.StringIO()

    with contextlib.redirect_stdout(sortie_buffer):
        print("=" * 60)
        print("ÉTAPE 3 : MODIFICATION B — SÉLECTION (ÉVOLUTION)")
        print("=" * 60)
        print(f"Seed: {SEED}")
        print(f"Parties par paire: {NB_PARTIES}")
        print(f"Tours par partie: {NB_TOURS}")
        print(f"Générations: {NB_GENERATIONS}")
        print(f"Stratégies: {stratégies_noms}")
        print()
        print("Population initiale (uniforme):")
        for nom, prop in population_initiale.items():
            print(f"  {nom}: {prop:.4f} ({prop*100:.1f}%)")
        print()

        # Historique pour graphique
        historique_pop = [population_initiale.copy()]
        population = population_initiale.copy()

        # Boucle évolutionnaire
        for gen in range(1, NB_GENERATIONS + 1):
            print(f"\n{'='*20} GÉNÉRATION {gen} {'='*20}")

            # Construire le dict de stratégies pondéré par la population
            # Pour le tournoi, on utilise les stratégies pures (pas de mélange dans une partie)
            # Le tournoi se joue entre toutes les stratégies, mais les scores finaux
            # seront pondérés par la population pour la sélection
            scores = jouer_tournoi(STRATEGIES, nb_parties=NB_PARTIES, nb_tours=NB_TOURS, seed=SEED + gen * 1000)

            # Afficher scores du tournoi
            print(f"Scores du tournoi (génération {gen}):")
            for nom, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                print(f"  {nom}: {score}")

            # Calculer nouvelle population
            population = generation_suivante(population, scores)
            historique_pop.append(population.copy())

            # Afficher nouvelle population
            print(f"\nPopulation après sélection (génération {gen}):")
            for nom, prop in sorted(population.items(), key=lambda x: x[1], reverse=True):
                print(f"  {nom}: {prop:.4f} ({prop*100:.1f}%)")

        print("\n" + "=" * 60)
        print("RÉSUMÉ FINAL — ÉVOLUTION SUR 20 GÉNÉRATIONS")
        print("=" * 60)
        print(f"{'Gén.':<6}", end="")
        for nom in stratégies_noms:
            print(f"{nom:<12}", end="")
        print()
        print("-" * (6 + 12 * len(stratégies_noms)))

        for gen, pop in enumerate(historique_pop):
            print(f"{gen:<6}", end="")
            for nom in stratégies_noms:
                print(f"{pop[nom]:<12.4f}", end="")
            print()

    # Sauvegarder la sortie console
    sortie_console = sortie_buffer.getvalue()
    print(sortie_console)
    sauvegarder_sortie_console(sortie_console, os.path.join('outputs', 'etape3_sortie_console.txt'))

    # Sauvegarder CSV évolution
    sauvegarder_csv_evolution(historique_pop, os.path.join('outputs', 'etape3_evolution.csv'))

    # Générer le graphique
    print("\n--- Génération du graphique ---")
    try:
        from src.experiments.generate_charts import graphique_etape3_evolution
        graphique_etape3_evolution(historique_pop, stratégies_noms)
    except Exception as e:
        print(f"Erreur génération graphique: {e}")

    return historique_pop


if __name__ == "__main__":
    main()