# Journal — Personne A (Heythem)

## Protocole
- Seed: 42
- Tours/partie: 200
- Parties/paire: 5
- Format: Round-robin

---

## Stratégies implémentées par MOI

| Stratégie | Règle (1 phrase) | Origine | Prédiction force/faiblesse |
|-----------|------------------|---------|----------------------------|
| ALL-D     | Défectionne toujours (D) | Base | Forte vs naïves, faible vs TFT (score plafonné à 2/tour) |
| RANDOM    | Choix équiprobable 50/50 entre C et D | Base | Baseline imprévisible, détruit la confiance mutuelle |
| GRIM      | Coopère jusqu'au 1er D adverse, puis ALL-D définitif | Friedman 1971 | Très forte vs coopératives, impitoyable |
| PAVLOV    | Win-Stay Lose-Shift : répète si gain≥3, change sinon | Kraines 1989 | S'adapte aux cycles, corrige ses erreurs |

---

## Travail réalisé

### Étape 1 — Moteur + 2 stratégies de base

**Fichiers créés :**
- `src/tournament/engine.py` — `jouer_partie()` et `jouer_tournoi()` (round-robin, seed reproductible)
- `src/tournament/strategies.py` — ALL-D, RANDOM (puis fusion avec TIT-FOR-TAT, TESTER, JOSS de Sara)
- `README.md` — Documentation + commandes de lancement
- `pyproject.toml` — Configuration package installable

**Tests effectués :**
```bash
python -m tournament.engine
```
Résultat : ALL-D gagne (67 pts) vs RANDOM (22 pts) — conforme à la prédiction.

**Git :**
- Branche `heythem` créée
- Commits : engine, strategies, README, config
- Merge vers `main` après résolution conflit `strategies.py` (fusion des 5 stratégies)

---

### Étape 2 — 2 nouvelles stratégies (GRIM, PAVLOV)

**Fichiers créés :**
- `src/tournament/strategies.py` — Ajout GRIM, PAVLOV
- `src/experiments/step2_new.py` — Script tournoi 7 stratégies

**Résultats (Seed 42, 5 parties × 200 tours) :**

| Rang | Stratégie | Score | vs Étape 1 |
|:----:|-----------|:-----:|:-----------|
| 1 | **GRIM** | 15469 | Nouveau |
| 2 | TIT-FOR-TAT | 15109 | +5999 |
| 3 | ALL-D | 15060 | +5515 |
| 4 | PAVLOV | 14068 | Nouveau |
| 5 | TESTER | 13343 | +4340 |
| 6 | JOSS | 13215 | +4501 |
| 7 | RANDOM | 12046 | +3601 |

**Analyse :**
- **GRIM domine** : Coopère avec TFT/JOSS/PAVLOV (score 3×200×5=3000 par paire) et punit ALL-D/TESTER (2×200×5=2000). Meilleur compromis.
- **TIT-FOR-TAT remonte** : Bénéficie de la présence de GRIM/PAVLOV (coopératifs) pour accumuler des scores (3,3).
- **ALL-D chute relative** : Ne perd pas en score absolu mais est dépassé par les stratégies coopératives entre elles.
- **PAVLOV correct** : S'adapte bien mais moins stable que GRIM face aux trahisons.

**Git :**
- Branche `etape2-strategies` créée puis supprimée (travail continu sur `heythem`)
- Commit : stratégies + step2_new.py
- Push vers `origin/heythem`

---

### Étape 3 — Modification A : Bruit (Noise 5%)

**Choix :** Bruit (inversion aléatoire 5% des actions) — plus simple que Horizon, classique en théorie des jeux.

**Prédiction (AVANT exécution) :**
- **TFT va chuter** : Sensible au bruit, un D accidentel déclenche spirale de représailles
- **ALL-D va monter** : Défectionne déjà, bruit ne change pas grand-chose, profite des erreurs adverses
- **GRIM robuste** : Une fois en mode punition, bruit sans effet ; en mode coopération, un D accidentel déclenche punition définitive (risque)
- **PAVLOV va souffrir** : Win-Stay/Lose-Shift confus par actions bruitées
- **JOSS/TESTER** : Déjà stochastiques, bruit se fond dans leur comportement

**Fichiers créés :**
- `src/tournament/engine.py` — Paramètre `bruit` ajouté à `jouer_partie()` et `jouer_tournoi()`
- `src/experiments/step3_mods.py` — Script tournoi avec bruit

**Résultats (Seed 42, 5 parties × 200 tours, Bruit=5%) :**

| Rang | Stratégie | Sans bruit | Avec bruit | Diff |
|:----:|-----------|:----------:|:----------:|:----:|
| 1 | **GRIM** | 15469 | 15613 | +144 |
| 2 | **ALL-D** | 15060 | 15500 | +440 |
| 3 | JOSS | 13215 | 13770 | +555 |
| 4 | TIT-FOR-TAT | 15109 | 13763 | -1346 |
| 5 | TESTER | 13343 | 13543 | +200 |
| 6 | PAVLOV | 14068 | 12280 | -1788 |
| 7 | RANDOM | 12046 | 12205 | +159 |

**Analyse :**
- **GRIM reste #1** : Gagne légèrement — sa punition définitive la protège des spirales (un D accidentel = punition, mais elle punissait déjà ALL-D/TESTER)
- **ALL-D bondit (+440)** : Profite des C accidentels des coopératifs (TFT, PAVLOV, GRIM en phase cooperative)
- **TFT s'effondre (-1346)** : Confirmé — bruit crée des D accidentels → représailles mutuelles → score plafonné à P=2
- **PAVLOV s'effondre (-1788)** : Plus grande perte — Win-Stay/Lose-Shift perd son repère avec actions bruitées
- **JOSS monte (+555)** : Ses 10% de trahisons sournoises se fondent dans le bruit, moins détectables
- **TESTER/RANDOM** : Légère hausse, comportement stochastique absorbe le bruit

**Conclusion :** Le bruit favorise les stratégies "méchantes" (ALL-D) et celles déjà bruitées (JOSS), pénalise sévèrement les stratégies réactives pures (TFT, PAVLOV). GRIM reste robuste grâce à sa simplicité binaire.

**Git :**
- Commit : engine.py (paramètre bruit) + step3_mods.py
- Push vers `origin/heythem`

---

## Impasses / Bugs

- **Conflit merge `strategies.py`** : Les deux branches avaient créé le fichier.
  - *Solution* : Fusion manuelle gardant les 5 stratégies (ALL-D, RANDOM + TIT-FOR-TAT, TESTER, JOSS)

---

## Checklist personnel

### Étape 1
- [x] `engine.py` : `jouer_partie()` fonctionnel + testé
- [x] `engine.py` : `jouer_tournoi()` fonctionnel + testé
- [x] `strategies.py` : ALL-D, RANDOM ajoutés
- [x] `README.md` : commandes de lancement documentées
- [x] `pyproject.toml` : package installable (`pip install -e .`)
- [x] Merge final vers `main` avec Sara

### Étape 2
- [x] 2 nouvelles stratégies choisies + documentées dans journal (GRIM, PAVLOV)
- [x] Implémentées dans `strategies.py`
- [x] `step2_new.py` créé et lancé → comparaison notée dans journal
- [x] Branche `etape2-strategies` pushée

### Étape 3
- [x] Modification A choisie : **Bruit** (5%) + prédiction écrite AVANT dans journal
- [x] Moteur modifié (`engine.py` : paramètre `bruit`)
- [x] `step3_mods.py` créé et lancé
- [x] Résultats + analyse dans journal

### Final
- [x] `README.md` à jour (commandes exactes)
- [x] Push final sur `heythem` → prêt pour merge vers `main` avec Sara

---

*Journal tenu conformément aux exigences du projet HAI716I — Novembre 2026*