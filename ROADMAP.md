# Roadmap - HAI716I Projet 2 : Tournoi de Dilemme du Prisonnier Itéré

> **Deadline** : Dimanche 15 novembre 2026, 23h59 (heure de Paris)
> **Temps estimé** : ~5h (séance du vendredi 13 novembre)

---

## 🎯 Objectif Global

Construire un moteur de tournoi de dilemme du prisonnier itéré, implémenter des stratégies, faire des expériences et documenter le tout dans un journal de bord.

---

## 📦 Stack Technique Recommandée

| Composant | Choix Recommandé | Justification |
|-----------|------------------|---------------|
| **Langage** | **Python 3.10+** | Écosystème scientifique, facile pour prototypage, reproductible via `random.seed()` |
| **Tests** | `pytest` | Standard, simple |
| **Reproductibilité** | `random.seed(42)` + `requirements.txt` / `pyproject.toml` | Seed fixe exigée par l'énoncé |
| **Visualisation (optionnel)** | `matplotlib` / `seaborn` | Pour graphiques dans le journal |
| **Format journal** | **Markdown** (converti en PDF via `pandoc` ou VS Code) | Versionnable dans git, facile à écrire |
| **Git** | Commits réguliers (historique = trace de travail) | Exigé par l'énoncé |

### Structure de dépôt suggérée
```
project2/
├── src/
│   ├── tournament/
│   │   ├── __init__.py
│   │   ├── engine.py       # Moteur de partie + tournoi
│   │   ├── strategies.py   # Stratégies de base + nouvelles
│   │   └── payoff.py       # Matrice de gains
│   └── experiments/
│       ├── __init__.py
│       ├── step1_base.py   # Étape 1
│       ├── step2_new.py    # Étape 2
│       └── step3_mods.py   # Étape 3
├── journal/
│   ├── journal.md          # Journal de bord (source)
│   └── journal.pdf         # Version rendue
├── outputs/                # Classements, captures, graphiques
├── tests/
│   └── test_strategies.py
├── requirements.txt
├── pyproject.toml
├── README.md               # Commandes de lancement
└── ROADMAP.md              # Ce fichier
```

---

## 🗓️ Plan Détaillé par Étape

### ✅ ÉTAPE 1 : Le Tournoi de Base (~1h30)

| Sous-tâche | Description | Fichiers concernés | Temps |
|------------|-------------|-------------------|-------|
| **1.1** | Créer structure projet + `requirements.txt` | `src/`, `requirements.txt` | 10 min |
| **1.2** | Implémenter matrice de gains (C/C=3, C/D=0, D/C=5, D/D=2) | `src/tournament/payoff.py` | 10 min |
| **1.3** | Implémenter moteur de **partie** (2 stratégies, N tours, historique) | `src/tournament/engine.py` | 20 min |
| **1.4** | Implémenter **tournoi tous-contre-tous** (5 parties × 200 tours) | `src/tournament/engine.py` | 15 min |
| **1.5** | Implémenter 5 stratégies de base | `src/tournament/strategies.py` | 25 min |
| **1.6** | Script lancement Étape 1 + classement + seed fixe | `src/experiments/step1_base.py` | 10 min |
| **1.7** | Répondre : *TIT-FOR-TAT gagne-t-il ? Pourquoi différence 1980 ?* | `journal/journal.md` | 10 min |

#### Stratégies de base à implémenter
| Stratégie | Description courte |
|-----------|-------------------|
| **ALL-D** | Toujours défectionner (D) |
| **RANDOM** | C ou D avec p=0.5 |
| **TIT-FOR-TAT** | Commence par C, puis copie le dernier coup adverse |
| **TESTER** | Commence D, puis si adversaire a joué C au tour 1 → TFT, sinon ALL-D |
| **JOSS** | TFT mais avec 10% de défection "par erreur" (ou p=0.1 de D au lieu de copier) |

> ⚠️ **Note** : Vérifier les définitions exactes dans les slides du cours 4 pour JOSS et TESTER.

---

### ✅ ÉTAPE 2 : Nouvelles Stratégies (~1h)

| Sous-tâche | Description | Fichiers concernés | Temps |
|------------|-------------|-------------------|-------|
| **2.1** | Choisir + implémenter **≥ 2 nouvelles stratégies** | `src/tournament/strategies.py` | 30 min |
| **2.2** | Relancer tournoi population élargie | `src/experiments/step2_new.py` | 10 min |
| **2.3** | Comparer classements (Étape 1 vs Étape 2) + analyse | `journal/journal.md` | 20 min |

#### Idées de stratégies supplémentaires (choisir ≥ 2)
| Stratégie | Source | Pourquoi intéressante |
|-----------|--------|----------------------|
| **ALL-C** | Triviale | Baseline coopérative pure |
| **GRIM** (Trigger) | Axelrod 1980 | Coopère jusqu'à 1ère défection, puis ALL-D à vie |
| **PAVLOV** (Win-Stay Lose-Shift) | Kraines & Kraines 1989 | Répète si gain ≥ 3, change sinon |
| **TFT-2T** (Two Tits for Tat) | Variantes TFT | Pardonne 1 défection, punit la 2ème |
| **RANDOM(p)** | Paramétrée | Explorer p ≠ 0.5 |
| **PROBER** | Li 2011 | Teste l'adversaire au début |
| **ADAPTIVE** | Propre | Change de mode selon score adversaire |

> 💡 **Conseil** : Choisir des stratégies qui illustrent des principes différents (pardon, exploitation, adaptation).

---

### ✅ ÉTAPE 3 : Modifications du Tournoi (~1h30)

> Appliquer **au moins 2 modifications** parmi les 4 proposées. Pour chacune : **prédiction → exécution → analyse**.

| Modification | Fichiers | Temps estimé |
|--------------|----------|--------------|
| **A. Bruit** (5% inversion coup) | `engine.py` + `step3_mods.py` | 25 min |
| **B. Horizon probabiliste** (w=0.95 ou 0.98) | `engine.py` + `step3_mods.py` | 25 min |
| **C. Sélection évolutive** (générations, proportions ∝ score) | `engine.py` + `step3_mods.py` | 35 min |
| **D. Autres gains** (matrice 2×2 section 07 cours) | `payoff.py` + `step3_mods.py` | 25 min |

#### Ordre de travail par modification choisie
```
1. Écrire PRÉDICTION dans journal/journal.md (AVANT de coder)
2. Implémenter la modification dans le moteur
3. Lancer le tournoi modifié
4. Capturer sortie + graphiques → outputs/
5. COMPARER et EXPLIQUER l'écart dans journal/journal.md
```

---

### ✅ JOURNAL DE BORD (Continu, ~30 min total répartis)

| Section | Contenu | Quand |
|---------|---------|-------|
| **Protocole** | N tours, N parties, seed, paramètres, mods choisies, justifications | Au fil de l'eau |
| **Stratégies** | Règle (1-2 phrases), origine, forces/faiblesses théoriques | À chaque implémentation |
| **Prédictions Étape 3** | **Avant** chaque exécution | Avant step3_mods.py |
| **Captures** | Classements (txt/csv), sorties console, graphiques | Après chaque run |
| **Impasses** | Ce qui a échoué, bugs, changements d'approche | Au fur et à mesure |

> Format : `journal/journal.md` (source) → export PDF pour le rendu final.

---

### ✅ RENDU FINAL (~15 min)

| Livrable | Vérification |
|----------|--------------|
| **Code** moteur + stratégies | `src/tournament/` complet |
| **README.md** | Commandes exactes pour relancer Étape 1, 2, 3 |
| **Journal** | `journal/journal.pdf` + `journal/journal.md` |
| **Git** | Push sur dépôt avant deadline, commits réguliers |

---

## ⚙️ Commandes de Lancement (à mettre dans README.md)

```bash
# Installation
pip install -r requirements.txt

# Étape 1 : Tournoi de base
python -m src.experiments.step1_base

# Étape 2 : Nouvelles stratégies
python -m src.experiments.step2_new

# Étape 3 : Modifications (ex: bruit + horizon)
python -m src.experiments.step3_mods --mods noise horizon

# Tous les tests
pytest tests/
```

---

## 📋 Checklist de Progression

### Étape 1
- [ ] Structure projet + deps
- [ ] Matrice de gains
- [ ] Moteur partie (historique, score)
- [ ] Moteur tournoi (round-robin, 5×200)
- [ ] 5 stratégies de base
- [ ] Seed fixe (ex: 42)
- [ ] Classement Étape 1 généré
- [ ] Réponse question TIT-FOR-TAT dans journal

### Étape 2
- [ ] Stratégie nouvelle #1 implémentée + documentée
- [ ] Stratégie nouvelle #2 implémentée + documentée
- [ ] (Optionnel) Stratégie #3
- [ ] Classement Étape 2 généré
- [ ] Comparaison Étape 1 vs 2 dans journal

### Étape 3
- [ ] Modification A choisie : prédiction écrite
- [ ] Modification A implémentée + résultats + analyse
- [ ] Modification B choisie : prédiction écrite
- [ ] Modification B implémentée + résultats + analyse
- [ ] (Optionnel) Modification C/D

### Journal & Rendu
- [ ] Journal complet (protocole, stratégies, prédictions, captures, impasses)
- [ ] Export PDF journal
- [ ] README à jour avec commandes
- [ ] Push git final avant deadline

---

## 💡 Conseils Pratiques

1. **Commencez simple** : Faites marcher l'Étape 1完全 avant d'ajouter de la complexité.
2. **Seed fixe** : `random.seed(42)` au tout début de chaque script d'expérience.
3. **Sorties structurées** : Écrivez les classements en CSV/JSON pour facile import dans journal.
4. **Commits réguliers** : `git add -A && git commit -m "step1: base tournament working"` etc.
5. **Journal au fil de l'eau** : N'attendez pas la fin pour tout écrire.
6. **Graphiques** : Un simple bar chart des scores suffit (matplotlib).

---

## 🔗 Ressources Utiles

- **Cours 4 slides** : Définitions exactes JOSS, TESTER, matrice gains
- **Axelrod 1980** : "The Evolution of Cooperation" - résultats originaux
- **Bibliothèque `axelrod-python`** : Pour vérifier vos implémentations (pas pour copier)
  ```bash
  pip install axelrod  # pour comparaison seulement
  ```

---

*Roadmap générée le 2026-11-13 — Bon courage ! 🚀*