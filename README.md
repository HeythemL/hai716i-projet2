# Tournoi - Dilemme du Prisonnier Itéré

Simulateur de tournoi round-robin pour le dilemme du prisonnier itéré.

## Installation

```bash
pip install -e .
```

## Utilisation

### Lancer un tournoi

```bash
python -m tournament.engine
```

### Utiliser dans votre code

```python
from tournament.engine import jouer_tournoi, afficher_classement
from tournament.strategies import STRATEGIES

# Sélectionner les stratégies
mes_strategies = {
    'ALL-D': STRATEGIES['ALL-D'],
    'TIT-FOR-TAT': STRATEGIES['TIT-FOR-TAT'],
    'GRIM-TRIGGER': STRATEGIES['GRIM-TRIGGER'],
}

# Lancer le tournoi
scores = jouer_tournoi(mes_strategies, nb_parties=10, nb_tours=200)
afficher_classement(scores)
```

## Stratégies disponibles

| Nom | Description |
|-----|-------------|
| `ALL-D` | Défectionne toujours |
| `RANDOM` | Choix aléatoire (50/50) |

## Matrice de gains

| | C | D |
|---|---|---|
| **C** | (3, 3) | (0, 5) |
| **D** | (5, 0) | (2, 2) |

Conditions : T=5 > R=3 > P=2 > S=0 et 2R=6 > T+S=5 ✓

## Structure

```
src/tournament/
├── __init__.py
├── gains.py      # Matrice de gains
├── strategies.py # Stratégies
└── engine.py     # Moteur de jeu/tournoi
```