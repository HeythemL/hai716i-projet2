# Journal de bord — HAI716I Projet 2

> **Projet** : HAI716I Projet 2 — Tournoi de Dilemme du Prisonnier Itéré  
> **Auteurs** : Heythem (Personne A) & Sara (Personne B)  
> **Date** : Novembre 2026  
> **Deadline** : Dimanche 15 novembre 2026, 23h59

---

## 1. Protocole commun

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| **Seed aléatoire** | 42 | Reproductibilité absolue exigée par l'énoncé |
| **Tours par partie** | 200 | Format Axelrod standard (énoncé) |
| **Parties par paire** | 5 | Format Axelrod standard (énoncé) |
| **Format tournoi** | Round-robin (tous contre tous) | Chaque stratégie affronte chaque autre |
| **Actions possibles** | C (Coopérer) ou D (Défectionner) | Choix simultané à chaque tour |

### Matrice de gains standard

|   | Adversaire joue C | Adversaire joue D |
|---|:---:|:---:|
| **Joueur joue C** | (3, 3) | (0, 5) |
| **Joueur joue D** | (5, 0) | (2, 2) |

- $T = 5$ (Tentation) > $R = 3$ (Récompense) > $P = 2$ (Punition) > $S = 0$ (Dupe)
- Condition du dilemme : $2R = 6 > T + S = 5$

---

## 2. Fiches des stratégies (Étape 1 - 5 stratégies de base)

| Stratégie | Règle résumée | Origine | Force théorique | Faiblesse théorique | Auteur |
|-----------|---------------|---------|-----------------|---------------------|--------|
| **ALL-D** | Défectionne toujours (D) | Axelrod 1980 | Inexploitable, score max vs coopérateurs | Coopération impossible (2 pts/tour) | Heythem |
| **RANDOM** | Choix équiprobable 50/50 entre C et D | Axelrod 1980 | Imprévisible | Score moyen faible, détruit la confiance | Heythem |
| **TIT-FOR-TAT** | Coopère au tour 0, puis copie le dernier coup adverse | Anatol Rapoport (1980) | Gentille, réactive, pardonnante | Vulnérable au bruit / trahisons aléatoires | Sara |
| **TESTER** | D au tour 0 ; si riposte adverse -> TFT, sinon exploite (alterne D/C) | Axelrod 1980 | Exploite les naïfs | Le test initial pénalise la relation avec TFT | Sara |
| **JOSS** | Copie le coup adverse mais trahit sournoisement 10% du temps | Axelrod 1980 | Tente de voler des points bonus | Spirales de représailles destructrices avec TFT | Sara |

---

## 3. Étape 1 : Tournoi de base

### 3.1 Classement obtenu

Exécution avec `python -m src.experiments.step1_base` (Seed 42) :

| Rang | Stratégie | Score total | Moyenne / partie |
|:----:|-----------|:-----------:|:----------------:|
| 🥇 1 | **ALL-D** | **9545** | 477.3 |
| 🥈 2 | TIT-FOR-TAT | 9109 | 455.5 |
| 🥉 3 | TESTER | 9003 | 450.2 |
| 4 | JOSS | 8714 | 435.7 |
| 5 | RANDOM | 8445 | 422.3 |

### 3.2 Visualisation

![Classement Étape 1](../outputs/etape1_classement.png)

### 3.3 Analyse : TIT-FOR-TAT gagne-t-elle ?

**Non, c'est ALL-D qui arrive en tête.**

**Explication de la différence avec le tournoi d'Axelrod (1980) :**
Dans le tournoi historique de 1980, TIT-FOR-TAT avait triomphé car la population comportait 14 stratégies avec une forte proportion de participants coopératifs ("nice"). TFT accumulait ainsi de gros scores ($3, 3$) lors de ses duels mutuellement vertueux.

Dans notre environnement restreint à 5 stratégies :
1. La population est majoritairement hostile : 3 stratégies sur 5 intègrent une composante de trahison ou d'exploitation (ALL-D, TESTER, JOSS).
2. Face à ALL-D, TFT perd le premier tour ($0$ vs $5$) avant de basculer en défection mutuelle ($2, 2$).
3. Face à JOSS, les trahisons imprévues (10%) rompent la coopération et enclenchent des séries de punitions mutuelles.
4. ALL-D profite du premier coup naïf de TFT et JOSS tout en ne concédant jamais de score à ses adversaires.

---

## 4. Journal des impasses et résolutions

1. **Pytest et la fonction `tester()`** : Pytest considérait la fonction de stratégie `tester` comme un test unitaire ou une fixture manquante (`fixture 'historique_moi' not found`).  
   *Résolution* : Importée sous un alias (`strat_tester`) dans les tests et restriction du scope de collecte via `pytest.ini`.
2. **Dépendances PDF sans bibliothèques système** : `WeasyPrint` nécessitait des bibliothèques C GTK externes (`libgobject`).  
   *Résolution* : Utilisation de `fpdf2` en Python pur pour garantir une compilation immédiate et portable du PDF.

---

## 5. Fichiers du projet à la fin de l'Étape 1

- `src/tournament/engine.py` (Moteur de jeu et tournoi)
- `src/tournament/gains.py` (Matrice de gains)
- `src/tournament/strategies.py` (5 stratégies du cours)
- `src/experiments/step1_base.py` (Script de lancement Étape 1)
- `tests/test_strategies.py` (Tests unitaires)
- `outputs/etape1_classement.csv`
- `outputs/etape1_classement.png`
- `outputs/etape1_sortie_console.txt`
- `outputs/etape1_tests_console.txt`
- `journal/journal_B.md` & `journal/journal_B.pdf`

