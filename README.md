# Tournoi - Dilemme du Prisonnier Itéré (HAI716I Projet 2)

Simulateur complet de tournoi round-robin pour le dilemme du prisonnier itéré avec modifications (bruit, évolution).

## Installation

```bash
pip install -e .
```

## Structure

```
src/
├── tournament/
│   ├── __init__.py
│   ├── gains.py          # Matrice de gains
│   ├── strategies.py     # 9 stratégies
│   └── engine.py         # Moteur : jouer_partie(), jouer_tournoi()
├── experiments/
│   ├── __init__.py
│   ├── step1_base.py     # Étape 1 : 5 stratégies de base
│   ├── step2_new.py      # Étape 2 : 7 stratégies
│   ├── step3_noise.py    # Étape 3A : Bruit 5%
│   ├── step3_mods.py     # Étape 3B : Évolution 20 générations
│   ├── generate_charts.py
│   └── md_to_pdf.py
tests/
├── test_strategies.py    # 16 tests unitaires
journal/
├── journal_A.md / .pdf
├── journal_B.md / .pdf
outputs/                  # Résultats CSV, graphiques, logs
```

## Stratégies (9)

| Nom | Description |
|-----|-------------|
| `ALL-D` | Défectionne toujours |
| `RANDOM` | 50/50 C ou D |
| `TIT-FOR-TAT` | Coopère tour 0, puis copie adversaire |
| `TESTER` | D tour 0 pour tester, puis TFT ou exploitation |
| `JOSS` | TFT avec 10% trahison sur C adverse |
| `GRIM` | Coopère jusqu'au 1er D, puis ALL-D définitif |
| `PAVLOV` | Win-Stay Lose-Shift : répète si gain≥3 |
| `TFT-2T` | Pardonne 1 D, riposte après 2 D consécutifs |
| `PROBER` | Test D tour 0, puis C,C ; TFT si riposte, sinon exploitation |

## Matrice de gains

| | C | D |
|---|---|---|
| **C** | (3, 3) | (0, 5) |
| **D** | (5, 0) | (2, 2) |

T=5 > R=3 > P=2 > S=0, 2R=6 > T+S=5 ✓

## Protocole

- **Seed** : 42
- **Tours/partie** : 200
- **Parties/paire** : 5
- **Format** : Round-robin

## Commandes

### Étape 1 — Tournoi base (5 stratégies)
```bash
python src/experiments/step1_base.py
```
Sortie : `outputs/etape1_classement.csv`

### Étape 2 — Tournoi élargi (7 stratégies)
```bash
python src/experiments/step2_new.py
```
Sortie : `outputs/etape2_classement.csv`

### Étape 3A — Bruit 5%
```bash
python src/experiments/step3_noise.py
```
Sortie : `outputs/etape3_bruit_classement.csv`

### Étape 3B — Évolution (20 générations)
```bash
python src/experiments/step3_mods.py
```
Sorties : `outputs/etape3_evolution.csv`, `outputs/etape3_evolution_population.png`

### Tests
```bash
pytest tests/
or 
python -m pytest
```

### Rapports PDF
```bash
python src/experiments/md_to_pdf_A.py journal/journal_A.md journal/journal_A.pdf
python src/experiments/md_to_pdf.py journal/journal_B.md journal/journal_B.pdf
```

## Utilisation programmatique

```python
from tournament.engine import jouer_partie, jouer_tournoi, afficher_classement
from tournament.strategies import STRATEGIES

# Une partie
resultat = jouer_partie(STRATEGIES['TIT-FOR-TAT'], STRATEGIES['ALL-D'], nb_tours=10, seed=42)

# Tournoi
scores = jouer_tournoi(STRATEGIES, nb_parties=5, nb_tours=200, seed=42)
afficher_classement(scores)

# Avec bruit
scores = jouer_tournoi(STRATEGIES, nb_parties=5, nb_tours=200, seed=42, bruit=0.05)
```

## Résultats attendus (seed 42)

**Étape 1 (5 stratégies) :**
1. ALL-D (9545), 2. TIT-FOR-TAT (9109), 3. TESTER (9003), 4. JOSS (8714), 5. RANDOM (8445)

**Étape 2 (7 stratégies) :**
1. GRIM (15469), 2. TIT-FOR-TAT (15109), 3. ALL-D (15060), 4. PAVLOV (14068), 5. TESTER (13343), 6. JOSS (13215), 7. RANDOM (12046)

**Étape 3A Bruit 5% (9 stratégies) :**
- TIT-FOR-TAT : -1804, PAVLOV : -1628, ALL-D : +909, JOSS : +995, GRIM robuste (#1)

**Étape 3B Évolution (génération 20) :**
- TIT-FOR-TAT 34%, GRIM 21%, PROBER 17%, TESTER 11%, autres < 7%

## Fichiers de sortie (outputs/)

- `etape1_classement.csv`
- `etape2_classement.csv` + `etape2_comparaison.png`
- `etape3_bruit_classement.csv`
- `etape3_evolution.csv` + `etape3_evolution_population.png`
- `etape*_sortie_console.txt`, `etape*_tests_console.txt`