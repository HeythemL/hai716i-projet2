# FEUILLE DE ROUTE — PERSONNE A (Moteur + Étape 1 partiel + Étape 2 partiel + Étape 3 partiel)

> **Option B choisie** — Travail par étapes séquentielles
> **Branche git** : `prenom/etape1-moteur` → `prenom/etape2-strategies` → `prenom/etape3-mods`

---

## 📁 FICHIERS DONT TU ES RESPONSABLE

| Fichier | Description |
|---------|-------------|
| `src/tournament/gains.py` | ✅ Déjà fait |
| `src/tournament/engine.py` | **TOI SEUL** — Moteur partie + tournoi |
| `src/tournament/strategies.py` | **PARTAGÉ** — Tu ajoutes : ALL-D, RANDOM, Nouvelles #1, #2, Modifs Étape 3 |
| `src/experiments/step1_base.py` | **PARTAGÉ** — Tu lances pour tester ton moteur |
| `src/experiments/step2_new.py` | **PARTAGÉ** — Tu ajoutes tes nouvelles stratégies |
| `src/experiments/step3_mods.py` | **PARTAGÉ** — Tu implémentes Modification A |
| `tests/test_engine.py` | **TOI SEUL** |
| `README.md` | **TOI SEUL** (commandes de lancement) |
| `journal/journal_A.md` | **TON journal personnel** |

---

## 🗓️ PLANNING DÉTAILLÉ AVEC DÉPENDANCES

### PHASE 1 — ÉTAPE 1 : Moteur + 2 stratégies (JOUR 1, ~1h30)

```
┌─────────────────────────────────────────────────────────────┐
│ 1.1 CRÉER engine.py (squelette)                            │
│     ├── jouer_partie(strat_i, strat_j, nb_tours=200)       │
│     ├── jouer_tournoi(strategies, nb_parties=5, ...)       │
│     └── PUSH → prenom/etape1-moteur                        │
│         ↓ B a besoin de ça pour step1_base.py              │
├─────────────────────────────────────────────────────────────┤
│ 1.2 IMPLÉMENTER jouer_partie()                             │
│     ├── Historique coups : liste [(action_i, action_j)]    │
│     ├── Score cumulé par joueur                            │
│     ├── Seed aléatoire (random.seed)                       │
│     └── TEST unitaire minimal + PUSH                       │
├─────────────────────────────────────────────────────────────┤
│ 1.3 IMPLÉMENTER jouer_tournoi()                            │
│     ├── Round-robin tous contre tous                       │
│     ├── 5 parties × 200 tours par paire                    │
│     ├── Retourne dict/DataFrame : {strat: score_total}     │
│     └── PUSH → B peut maintenant lancer step1_base.py      │
├─────────────────────────────────────────────────────────────┤
│ 1.4 AJOUTER dans strategies.py : ALL-D, RANDOM             │
│     def all_d(historique_moi, historique_adv, tour): return D
│     def random(historique_moi, historique_adv, tour): return choice([C,D])
│     └── PUSH                                               │
├─────────────────────────────────────────────────────────────┤
│ 1.5 LANCER step1_base.py (avec B) → vérifier classement    │
│     └── NOTE résultats dans journal_A.md                   │
└─────────────────────────────────────────────────────────────┘
```

**⏰ MOMENT CLÉ PUSH** : Après 1.3 — B est bloqué tant que `jouer_tournoi()` ne marche pas.

---

### PHASE 2 — ÉTAPE 2 : Tes 2 nouvelles stratégies (JOUR 1, ~45 min)

```
┌─────────────────────────────────────────────────────────────┐
│ 2.1 CHOISIR 2 stratégies (ex: GRIM, PAVLOV)                │
│     └── NOTE règles + prédictions dans journal_A.md        │
├─────────────────────────────────────────────────────────────┤
│ 2.2 IMPLÉMENTER dans strategies.py                         │
│     def grim(historique_moi, historique_adv, tour): ...    │
│     def pavlov(historique_moi, historique_adv, tour): ...  │
│     └── PUSH → prenom/etape2-strategies                    │
├─────────────────────────────────────────────────────────────┤
│ 2.3 LANCER step2_new.py (avec B) → comparer classements    │
│     └── NOTE diff Étape 1 vs 2 dans journal_A.md           │
└─────────────────────────────────────────────────────────────┘
```

**⏰ MOMENT CLÉ PUSH** : Après 2.2 — B a besoin de tes stratégies pour le tournoi élargi.

---

### PHASE 3 — ÉTAPE 3 : Modification A (JOUR 1, ~45 min)

```
┌─────────────────────────────────────────────────────────────┐
│ 3.1 CHOISIR Modification A (Bruit OU Horizon)              │
│     └── ÉCRIRE PRÉDICTION dans journal_A.md (AVANT de coder)│
├─────────────────────────────────────────────────────────────┤
│ 3.2 MODIFIER engine.py pour supporter la modif             │
│     • Bruit : paramètre bruit=0.05, inverser action 5%     │
│     • Horizon : paramètre w=0.95, arrêt probabiliste       │
│     └── PUSH                                               │
├─────────────────────────────────────────────────────────────┤
│ 3.3 AJOUTER dans step3_mods.py l'appel pour ta modif       │
│     └── PUSH → prenom/etape3-mods                          │
├─────────────────────────────────────────────────────────────┤
│ 3.4 LANCER → RÉSULTATS → ANALYSE dans journal_A.md         │
│     └── Comparer prédiction vs réalité                     │
└─────────────────────────────────────────────────────────────┘
```

**⏰ MOMENT CLÉ PUSH** : Après 3.2 — B a besoin du moteur modifié pour sa modif B.

---

## 📝 TON JOURNAL — `journal/journal_A.md`

Structure minimale :
```markdown
# Journal — Personne A

## Protocole
- Seed: 42
- Tours/partie: 200
- Parties/paire: 5
- Modifs choisies: [Bruit/Horizon] + [Sélection/Gains]

## Stratégies implémentées par MOI
| Stratégie | Règle (1 phrase) | Origine | Prédiction force/faiblesse |
|-----------|------------------|---------|----------------------------|
| ALL-D     | Toujours D       | Base    | Forte vs naïves, faible vs TFT |
| RANDOM    | 50/50 C/D        | Base    | Baseline |
| GRIM      | Coopère jusqu'à 1er D, puis ALL-D | Axelrod | Forte vs coopératives |
| PAVLOV    | Win-Stay Lose-Shift | Kraines | S'adapte aux cycles |

## Prédictions Étape 3 (ÉCRITES AVANT EXÉCUTION)
### Modification A : [Bruit/Horizon]
**Prédiction :** ...
**Résultat :** ...
**Analyse :** ...

## Impasses / Bugs
- [Date] Problème : ...
- Solution : ...
```

---

## 🔄 SYNC AVEC PERSONNE B

| Moment | Action |
|--------|--------|
| **Après 1.3** | Dis à B : "API `jouer_tournoi()` prête, tu peux coder `step1_base.py`" |
| **Après 2.2** | Dis à B : "Mes 2 stratégies poussées, lance `step2_new.py`" |
| **Après 3.2** | Dis à B : "Moteur supporte ma modif, tu peux tester la tienne" |
| **Fin** | Merge final vers `main` ensemble |

---

## ✅ CHECKLIST PERSONNELLE

### Étape 1
- [ ] `engine.py` : `jouer_partie()` fonctionnel + testé
- [ ] `engine.py` : `jouer_tournoi()` fonctionnel + testé
- [ ] `strategies.py` : ALL-D, RANDOM ajoutés
- [ ] `test_engine.py` : au moins 2 tests passent
- [ ] `step1_base.py` lancé avec B → classement OK
- [ ] `journal_A.md` : résultats Étape 1 notés

### Étape 2
- [ ] 2 nouvelles stratégies choisies + documentées dans journal
- [ ] Implémentées dans `strategies.py`
- [ ] `step2_new.py` lancé → comparaison notée dans journal

### Étape 3
- [ ] Modification A choisie + **prédiction écrite AVANT** dans journal
- [ ] Moteur modifié (`engine.py`)
- [ ] `step3_mods.py` mis à jour
- [ ] Résultats + analyse dans journal

### Final
- [ ] `README.md` à jour (commandes exactes)
- [ ] Push final → merge vers `main` avec B