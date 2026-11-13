## HAI716I Projet 2 (partie 1)

## Cadre

Vous construisez seul un tournoi de dilemme du prisonnier itéré, vous y faites s'affronter des stratégies, et vous expliquez ce que vous observez.

| Séance vendredi 13 novembre 2026, environ 5 h |   |
| --- | --- |
| Modalité travail individuel |   |
| Rendu Code fourni aucun : le moteur du tournoi fait partie du travail | push sur votre dépôt git avant dimanche 15 novembre 2026, 23h59 (heure de Paris) |
| Langage libre Livrables le code et un journal de bord |   |

Le sujet part du cours 4 et vous demande d'aller plus loin que lui. Recopier les stratégies des diapositives ne suffit pas.

## Le jeu de départ

Le point de départ est le tournoi d'Axelrod du cours : chaque stratégie affronte chaque autre sur 5 parties de 200 tours, et le meilleur score total gagne.

À chaque tour, les deux joueurs choisissent C ou D en même temps, sans voir le choix de l'autre. Chacun connaît ensuite les coups passés de son adversaire. Les gains sont ceux du cours :

|   | j joue C | j joue D |
| --- | --- | --- |
| i joue C | 3, 3 | 0, 5 |
| i joue D | 5, 0 | 2, 2 |

Les cinq stratégies vues en cours servent de population de base : ALL-D, RANDOM, TIT-FOR-TAT, TESTER et JOSS.

## Travail demandé

Le travail se fait en trois étapes, dans l'ordre.

## Étape 1 : le tournoi de base

- 1. Écrivez un moteur qui fait jouer une partie entre deux stratégies, puis un tournoi tous contre tous.

- 2. Implémentez les cinq stratégies du cours.

- 3. Lancez le tournoi au format d'Axelrod et produisez un classement.

- 4. Question : TIT-FOR-TAT gagne-t-il chez vous ? Si non, expliquez pourquoi votre résultat diffère de celui de 1980.

Fixez la graine aléatoire : vos résultats doivent pouvoir être relancés à l'identique.

## Étape 2 : de nouvelles stratégies

Ajoutez au moins 2 stratégies absentes du cours.

Relancez le tournoi avec la population élargie et comparez au classement de l'étape 1.

## Étape 3 : modifier le tournoi

Appliquez au moins deux modifications parmi les suivantes. Le choix est libre mais doit être justifié.


| Modification Principe |   |
| --- | --- |
| Bruit | chaque coup est inversé avec une petite probabilité, par exemple 5 % |
| Horizon | après chaque tour, la partie continue avec une probabilité w au lieu de durer 200 tours |
| inconnu |   |
| Sélection | le tournoi est rejoué sur plusieurs générations ; la part de chaque stratégie dans la population |
|   | suit son score |
| Autres gains | la matrice change : soit elle reste un dilemme, soit elle devient un autre jeu 2 × 2 de la section |
|   | 07 du cours |

Pour chaque modification, procédez dans cet ordre :

- 1. Écrivez votre prédiction dans le journal avant de lancer quoi que ce soit.

- 2. Lancez le tournoi.

- 3. Comparez et expliquez l'écart.

## Journal de bord

Tenez un document de prise de notes tout au long du travail. Il sert de trace de votre démarche et pourra servir de support si une présentation orale est organisée.

Il contient au minimum :

- Le protocole : nombre de tours, de parties, valeurs des paramètres, modifications retenues, et la raison de chaque choix.

- Chaque stratégie : sa règle en une ou deux phrases, d'où elle vient, contre qui elle devrait bien ou mal jouer, et pourquoi.

- Les prédictions de l'étape 3, écrites avant les résultats.

- Des captures d'écran de vos avancements : classements, sorties de programme, graphiques éventuels.

- Les impasses : ce qui n'a pas marché et ce que vous avez changé.

Toute trace est importante, les échecs et impasses ne feront pas perdre de points si elles sont expliquées.

## Rendu

Poussez sur votre dépôt git avant dimanche 15 novembre 2026, 23h59 (heure de Paris). Seul l'état du dépôt à cette heure est pris en compte.

Le dépôt contient :

- le code du moteur et des stratégies

- un README qui donne la commande pour relancer chaque tournoi

- le journal de bord, en PDF ou en Markdown, avec ses captures d'écran

Je vous recommande de faire des commits réguliers pendant la séance: l'historique fait partie de la trace de votre travail.
