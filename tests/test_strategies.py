"""
Tests unitaires pour les 5 stratégies de base.
Vérifie le comportement attendu de chaque stratégie.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tournament.gains import C, D
from src.tournament.strategies import (all_d, random_strat, tit_for_tat,
                                       tester as strat_tester, joss,
                                       grim, pavlov, tft_2t, prober)


# ============================================================
# ALL-D
# ============================================================

class TestAllD:
    def test_premier_tour(self):
        assert all_d([], [], 0) == D

    def test_toujours_D(self):
        """ALL-D doit toujours retourner D, peu importe l'historique."""
        for tour in range(10):
            assert all_d([D]*tour, [C]*tour, tour) == D
            assert all_d([D]*tour, [D]*tour, tour) == D


# ============================================================
# RANDOM
# ============================================================

class TestRandom:
    def test_retourne_C_ou_D(self):
        """RANDOM doit toujours retourner C ou D."""
        import random
        random.seed(42)
        for tour in range(50):
            resultat = random_strat([], [], tour)
            assert resultat in (C, D)

    def test_pas_toujours_pareil(self):
        """RANDOM ne doit pas toujours donner la même réponse (statistique)."""
        import random
        random.seed(42)
        resultats = [random_strat([], [], 0) for _ in range(100)]
        assert C in resultats and D in resultats


# ============================================================
# TIT-FOR-TAT
# ============================================================

class TestTitForTat:
    def test_premier_tour_coopere(self):
        """TFT doit coopérer au premier tour."""
        assert tit_for_tat([], [], 0) == C

    def test_copie_cooperation(self):
        """TFT doit copier C de l'adversaire."""
        assert tit_for_tat([C], [C], 1) == C

    def test_copie_defection(self):
        """TFT doit copier D de l'adversaire."""
        assert tit_for_tat([C], [D], 1) == D

    def test_sequence_complete(self):
        """TFT suit les coups adverses avec un tour de retard."""
        hist_adv = [C, D, D, C, C]
        hist_moi = [C, C, D, D, C]
        # Tour 5 : doit copier hist_adv[-1] = C
        assert tit_for_tat(hist_moi, hist_adv, 5) == C

    def test_riposter_puis_pardonner(self):
        """TFT riposte à une trahison, puis pardonne si l'adversaire re-coopère."""
        # Adversaire : C, D, C → TFT devrait jouer C, C, D, C
        assert tit_for_tat([], [], 0) == C
        assert tit_for_tat([C], [C], 1) == C
        assert tit_for_tat([C, C], [C, D], 2) == D
        assert tit_for_tat([C, C, D], [C, D, C], 3) == C


# ============================================================
# TESTER
# ============================================================

class TestTester:
    def test_premier_tour_trahit(self):
        """TESTER doit trahir au premier tour (test l'adversaire)."""
        assert strat_tester([], [], 0) == D

    def test_deuxieme_tour_coopere(self):
        """TESTER coopère au tour 1 pour observer la réaction."""
        assert strat_tester([D], [C], 1) == C

    def test_exploite_si_pas_riposte(self):
        """Si l'adversaire n'a pas riposté (C au tour 1), TESTER exploite."""
        # Adversaire joue C au tour 0, puis C au tour 1 → pas de riposte
        hist_moi = [D, C]
        hist_adv = [C, C]  # adversaire n'a pas riposté au tour 1
        # Tour 2 (pair) : devrait jouer D (exploitation)
        assert strat_tester(hist_moi, hist_adv, 2) == D
        # Tour 3 (impair) : devrait jouer C
        hist_moi2 = [D, C, D]
        hist_adv2 = [C, C, C]
        assert strat_tester(hist_moi2, hist_adv2, 3) == C

    def test_tft_si_riposte(self):
        """Si l'adversaire a riposté (D au tour 1), TESTER joue TFT."""
        hist_moi = [D, C]
        hist_adv = [C, D]  # adversaire a riposté au tour 1
        # Tour 2 : TFT → copie hist_adv[-1] = D
        assert strat_tester(hist_moi, hist_adv, 2) == D


# ============================================================
# JOSS
# ============================================================

class TestJoss:
    def test_premier_tour_coopere(self):
        """JOSS doit coopérer au premier tour."""
        assert joss([], [], 0) == C

    def test_copie_defection(self):
        """JOSS doit toujours copier une défection adverse."""
        import random
        random.seed(42)
        # Quand l'adversaire joue D, JOSS doit jouer D (pas de random ici)
        for _ in range(20):
            assert joss([C], [D], 1) == D

    def test_parfois_trahit_sur_cooperation(self):
        """JOSS trahit ~10% du temps quand l'adversaire coopère."""
        import random
        random.seed(42)
        resultats = []
        for i in range(1000):
            resultat = joss([C], [C], 1)
            resultats.append(resultat)
        nb_trahisons = resultats.count(D)
        # Environ 10% de trahisons (tolérance large pour le test)
        assert 50 < nb_trahisons < 200, f"Attendu ~100 trahisons, obtenu {nb_trahisons}"


# ============================================================
# GRIM (Personne A)
# ============================================================

class TestGrim:
    def test_premier_tour_coopere(self):
        """GRIM doit coopérer au premier tour."""
        assert grim([], [], 0) == C

    def test_coopere_tant_que_pas_de_D(self):
        """GRIM coopère tant que l'adversaire n'a jamais joué D."""
        assert grim([C], [C], 1) == C
        assert grim([C, C], [C, C], 2) == C
        assert grim([C, C, C], [C, C, C], 3) == C

    def test_bascule_apres_premier_D(self):
        """GRIM bascule en ALL-D dès le premier D adverse."""
        assert grim([C, C], [C, D], 2) == D
        assert grim([C, C, D], [C, D, C], 3) == D
        assert grim([C, C, D, D], [C, D, C, C], 4) == D


# ============================================================
# PAVLOV (Personne A)
# ============================================================

class TestPavlov:
    def test_premier_tour_coopere(self):
        """PAVLOV doit coopérer au premier tour."""
        assert pavlov([], [], 0) == C

    def test_win_stay(self):
        """PAVLOV répète son coup si gain >= 3 (R=3 ou T=5)."""
        # (C,C) -> gain 3 -> Win-Stay -> rejoue C
        assert pavlov([C], [C], 1) == C
        # (D,C) -> gain 5 -> Win-Stay -> rejoue D
        assert pavlov([D], [C], 1) == D

    def test_lose_shift(self):
        """PAVLOV change de coup si gain < 3 (P=2 ou S=0)."""
        # (C,D) -> gain 0 -> Lose-Shift -> change vers D
        assert pavlov([C], [D], 1) == D
        # (D,D) -> gain 2 -> Lose-Shift -> change vers C
        assert pavlov([D], [D], 1) == C


# ============================================================
# TFT-2T (Personne B)
# ============================================================

class TestTFT2T:
    def test_premier_tour_coopere(self):
        """TFT-2T doit coopérer au premier tour."""
        assert tft_2t([], [], 0) == C

    def test_pardonne_premier_D(self):
        """TFT-2T pardonne la première défection adverse."""
        # Adversaire joue D une seule fois -> TFT-2T continue de coopérer
        assert tft_2t([C], [D], 1) == C

    def test_ripote_apres_deux_D_consecutifs(self):
        """TFT-2T riposte seulement après DEUX défections consécutives."""
        # Un seul D -> pardon
        assert tft_2t([C], [D], 1) == C
        # Deux D consécutifs -> riposte
        assert tft_2t([C, C], [D, D], 2) == D

    def test_recoopere_apres_ripote_si_adversaire_coopere(self):
        """TFT-2T re-coopère si l'adversaire re-coopère après la riposte."""
        # Adversaire : D, D, C -> TFT-2T : C, D, C
        assert tft_2t([], [], 0) == C
        assert tft_2t([C], [D], 1) == C  # pardonne 1er D
        assert tft_2t([C, C], [D, D], 2) == D  # riposte au 2ème D
        assert tft_2t([C, C, D], [D, D, C], 3) == C  # re-coopère


# ============================================================
# PROBER (Personne B)
# ============================================================

class TestProber:
    def test_premier_tour_trahit(self):
        """PROBER doit trahir au premier tour (test)."""
        assert prober([], [], 0) == D

    def test_deuxieme_tour_coopere(self):
        """PROBER coopère au tour 1."""
        assert prober([D], [C], 1) == C

    def test_troisieme_tour_coopere(self):
        """PROBER coopère au tour 2."""
        assert prober([D, C], [C, C], 2) == C

    def test_passe_en_tft_si_riposte_tour1(self):
        """Si adversaire riposte au tour 1 (joue D), PROBER passe en TFT."""
        # Adversaire : C (tour 0), D (tour 1 = riposte)
        hist_moi = [D, C]
        hist_adv = [C, D]
        # Tour 3 : TFT -> copie hist_adv[-1] = D
        assert prober(hist_moi, hist_adv, 3) == D
        # Tour 4 : TFT -> copie hist_adv[-1] = C (si adv joue C)
        hist_moi2 = [D, C, D]
        hist_adv2 = [C, D, C]
        assert prober(hist_moi2, hist_adv2, 4) == C

    def test_exploite_si_pas_riposte(self):
        """Si adversaire ne riposte pas aux tours 1 et 2, PROBER exploite en alternant D/C."""
        # Adversaire : C, C, C -> pas de riposte
        hist_moi = [D, C, C]
        hist_adv = [C, C, C]
        # Tour 3 (impair) : D
        assert prober(hist_moi, hist_adv, 3) == D
        # Tour 4 (pair) : C
        hist_moi2 = [D, C, C, D]
        hist_adv2 = [C, C, C, C]
        assert prober(hist_moi2, hist_adv2, 4) == C

