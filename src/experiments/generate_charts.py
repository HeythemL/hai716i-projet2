"""Script pour générer les graphiques du journal de bord."""
import matplotlib
matplotlib.use('Agg')  # Backend sans GUI
import matplotlib.pyplot as plt
import os


def graphique_etape1():
    """Graphique en barres du classement Étape 1."""
    strategies = ['ALL-D', 'TIT-FOR-TAT', 'TESTER', 'JOSS', 'RANDOM']
    scores = [9545, 9109, 9003, 8714, 8445]

    colors = ['#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#3498db']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(strategies[::-1], scores[::-1], color=colors[::-1], edgecolor='black', linewidth=0.5)

    # Ajouter les valeurs sur les barres
    for bar, score in zip(bars, scores[::-1]):
        ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                str(score), ha='left', va='center', fontweight='bold', fontsize=12)

    ax.set_xlabel('Score total', fontsize=13)
    ax.set_title('Étape 1 — Classement du tournoi de base\n(5 parties × 200 tours, seed=42)',
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(scores) * 1.12)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/etape1_classement.png', dpi=150, bbox_inches='tight')
    print("Graphique sauvegardé : outputs/etape1_classement.png")
    plt.close()


def graphique_etape2_comparaison(scores_etape1, scores_etape2):
    """
    Graphique comparatif Étape 1 vs Étape 2.
    Montre l'évolution des scores pour les 5 stratégies communes.
    """
    # Stratégies communes aux deux étapes (dans l'ordre du classement Étape 1)
    strategies_communes = ['ALL-D', 'TIT-FOR-TAT', 'TESTER', 'JOSS', 'RANDOM']

    scores1 = [scores_etape1.get(s, 0) for s in strategies_communes]
    scores2 = [scores_etape2.get(s, 0) for s in strategies_communes]

    x = range(len(strategies_communes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))

    bars1 = ax.barh([i + width/2 for i in x], scores1, width,
                    label='Étape 1 (5 stratégies)', color='#3498db', edgecolor='black', linewidth=0.5)
    bars2 = ax.barh([i - width/2 for i in x], scores2, width,
                    label='Étape 2 (9 stratégies)', color='#e74c3c', edgecolor='black', linewidth=0.5)

    # Valeurs sur les barres
    for bar, score in zip(bars1, scores1):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                str(score), ha='left', va='center', fontweight='bold', fontsize=10)
    for bar, score in zip(bars2, scores2):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                str(score), ha='left', va='center', fontweight='bold', fontsize=10)

    ax.set_yticks(x)
    ax.set_yticklabels(strategies_communes[::-1], fontsize=12)
    ax.set_xlabel('Score total', fontsize=13)
    ax.set_title('Comparatif Étape 1 vs Étape 2 — 5 stratégies de base\n(5 parties × 200 tours, seed=42)',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_xlim(0, max(max(scores1), max(scores2)) * 1.15)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/etape2_comparaison.png', dpi=150, bbox_inches='tight')
    print("Graphique comparatif sauvegardé : outputs/etape2_comparaison.png")
    plt.close()


def graphique_etape2_classement(scores):
    """Graphique en barres du classement complet Étape 2 (9 stratégies)."""
    strategies = list(scores.keys())
    scores_list = list(scores.values())

    # Couleurs : stratégies de base en bleu, nouvelles d'A en orange, nouvelles de B en vert
    color_map = {
        'ALL-D': '#3498db', 'RANDOM': '#3498db', 'TIT-FOR-TAT': '#3498db',
        'TESTER': '#3498db', 'JOSS': '#3498db',
        'GRIM': '#e67e22', 'PAVLOV': '#e67e22',
        'TFT-2T': '#27ae60', 'PROBER': '#27ae60'
    }
    colors = [color_map.get(s, '#95a5a6') for s in strategies]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(strategies[::-1], scores_list[::-1], color=colors[::-1], edgecolor='black', linewidth=0.5)

    # Légende des couleurs
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Stratégies de base (5)'),
        Patch(facecolor='#e67e22', label='Nouvelles Personne A (GRIM, PAVLOV)'),
        Patch(facecolor='#27ae60', label='Nouvelles Personne B (TFT-2T, PROBER)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

    for bar, score in zip(bars, scores_list[::-1]):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                str(score), ha='left', va='center', fontweight='bold', fontsize=11)

    ax.set_xlabel('Score total', fontsize=13)
    ax.set_title('Étape 2 — Classement complet (9 stratégies)\n(5 parties × 200 tours, seed=42)',
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(scores_list) * 1.12)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/etape2_classement.png', dpi=150, bbox_inches='tight')
    print("Graphique classement Étape 2 sauvegardé : outputs/etape2_classement.png")
    plt.close()


if __name__ == "__main__":
    graphique_etape1()
    # Test avec données factices
    scores1 = {'ALL-D': 9545, 'TIT-FOR-TAT': 9109, 'TESTER': 9003, 'JOSS': 8714, 'RANDOM': 8445}
    scores2 = {'ALL-D': 19120, 'TIT-FOR-TAT': 21104, 'TESTER': 19843, 'JOSS': 18293, 'RANDOM': 17785,
               'GRIM': 20489, 'PAVLOV': 19403, 'TFT-2T': 18630, 'PROBER': 20347}
    graphique_etape2_comparaison(scores1, scores2)
    graphique_etape2_classement(scores2)

