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

if __name__ == "__main__":
    graphique_etape1()

