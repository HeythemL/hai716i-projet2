# Répartition du travail — Équipe de 2

> Objectif : Travailler en parallèle sans conflits git, avec des interfaces claires entre les modules.

---

## 🎯 Option A : Par couche (recommandé)

| Personne A — **Moteur & Tournoi de base** | Personne B — **Stratégies & Expériences** |
|-------------------------------------------|-------------------------------------------|
| `src/tournament/gains.py` ✅ | `src/tournament/strategies.py` (toutes les stratégies) |
| `src/tournament/engine.py` (partie + tournoi round-robin) | `src/experiments/step1_base.py` (lance tournoi de base) |
| `src/experiments/step1_base.py` (si A veut tester) | `src/experiments/step2_new.py` (nouvelles stratégies) |
| `README.md` (commandes de lancement) | `src/experiments/step3_mods.py` (modifications tournoi) |
| Tests moteur : `tests/test_engine.py` | Tests stratégies : `tests/test_strategies.py` |
| | `journal/journal.md` (journal de bord principal) |

### Interface commune (à définir **ensemble** au début)
```python
# Dans engine.py — signature que B utilisera
def jouer_partie(strat_i, strat_j, nb_tours=200, gains=None, bruit=0.0) -> dict:
    """Retourne {'score_i': int, 'score_j': int, 'historique': [(a_i, a_j), ...]}"""

def jouer_tournoi(strategies, nb_parties=5, nb_tours=200, **kwargs) -> pd.DataFrame:
    """Retourne DataFrame classement avec colonnes: strategie, score_total, ..."""
```

**Personne A** implémente ces fonctions. **Personne B** les appelle sans toucher à `engine.py`.

---

## 🔄 Option B : Par étape (si vous préférez séquentiel)

| Semaine / Session | Personne A | Personne B |
|-------------------|------------|------------|
| **Étape 1** | Moteur (`engine.py`) + ALL-D, RANDOM | TIT-FOR-TAT, TESTER, JOSS + `step1_base.py` |
| **Étape 2** | Nouvelles stratégies #1, #2 | Nouvelles stratégies #3, #4 + `step2_new.py` |
| **Étape 3** | Modification A (bruit/horizon) + `step3_mods.py` | Modification B (sélection/gains) + journal |

> ⚠️ Risque : plus de merge conflicts sur `strategies.py` et `engine.py`.

---

## 📋 Règles de collaboration

### Git
```bash
# Chaque personne sur sa branche
git checkout -b prenom/etape1-moteur      # Personne A
git checkout -b prenom/etape1-strategies  # Personne B

# Commits réguliers, push fréquent
git add -A && git commit -m "prenom: description courte"
git push origin prenom/etape1-moteur

# PR / merge vers main quand étape validée à 2
```

### Communication
- **Daily sync 5 min** : "Qu'est-ce qui bloque ? Qu'est-ce qui est prêt ?"
- **Interface figée** : Une fois `engine.py` API définie, A ne change plus les signatures sans prévenir B.
- **Journal partagé** : B écrit le journal, A y ajoute ses captures/résultats moteur.

### Dépendances croisées
| Si A a besoin de B | Si B a besoin de A |
|--------------------|--------------------|
| Stratégies pour tester le moteur | API `engine.py` stable pour lancer expériences |
| → A écrit des **stubs** simples (ALL-D, RANDOM) | → B attend que A valide `jouer_partie()` et `jouer_tournoi()` |

---

## ✅ Checklist de démarrage (à faire ensemble, 10 min)

- [ ] Choisir Option A ou B
- [ ] Définir signatures exactes `jouer_partie()` et `jouer_tournoi()` dans `engine.py`
- [ ] Créer branches git
- [ ] Personne A : squelette `engine.py` avec `pass` + tests qui échouent
- [ ] Personne B : squelette `strategies.py` avec 5 classes/fonctions vides
- [ ] Lancer `pytest` → tout rouge, c'est normal
- [ ] Première sync dans 30 min

---

## 💡 Conseil

**Option A est plus safe** : A finit le moteur → B peut travailler en autonomie totale sur stratégies/expériences. Moins de conflicts, revue de code naturelle à la merge.

Bon duo ! 🤝