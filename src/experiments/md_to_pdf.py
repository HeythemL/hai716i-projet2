"""
Convertit journal_B.md en journal_B.pdf avec fpdf2.
Gère les tableaux, les blocs de code, les titres, et les images.
"""
import os
import re
from fpdf import FPDF


class JournalPDF(FPDF):
    def normalize_text(self, text):
        if isinstance(text, str):
            text = text.replace('—', '-').replace('–', '-').replace('’', "'").replace('‘', "'")
            text = text.replace('“', '"').replace('”', '"')
            text = text.replace('🥇', '1.').replace('🥈', '2.').replace('🥉', '3.').replace('✅', '[OK]')
            text = text.replace('≥', '>=').replace('≤', '<=').replace('→', '->')
            text = text.replace('×', 'x').replace('→', '->')
            text = text.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a')
            text = text.replace('ù', 'u').replace('ô', 'o').replace('î', 'i').replace('ç', 'c')
            text = text.replace('â', 'a').replace('ï', 'i').replace('œ', 'oe').replace('æ', 'ae')
        return super().normalize_text(text)

    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, 'HAI716I Projet 2 - Journal de bord - Personne B', align='C')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('Helvetica', 'B', 18)
            self.set_text_color(44, 62, 80)
            self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(52, 152, 219)
            self.set_line_width(0.8)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)
        elif level == 2:
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(44, 62, 80)
            self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(189, 195, 199)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)
        elif level == 3:
            self.set_font('Helvetica', 'B', 12)
            self.set_text_color(52, 73, 94)
            self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(3)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bold_text(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.multi_cell(0, 5.5, text)
        self.set_font('Helvetica', '', 10)
        self.ln(2)

    def code_block(self, code):
        self.set_fill_color(45, 45, 45)
        self.set_text_color(248, 248, 242)
        self.set_font('Courier', '', 8)
        lines = code.strip().split('\n')
        x = self.get_x()
        y = self.get_y()
        block_height = len(lines) * 4.5 + 6
        if y + block_height > 270:
            self.add_page()
            y = self.get_y()
        self.rect(10, y, 190, block_height, 'F')
        self.set_xy(12, y + 3)
        for line in lines:
            self.cell(0, 4.5, line[:120], new_x="LMARGIN", new_y="NEXT")
            self.set_x(12)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def add_table(self, headers, rows):
        self.set_font('Helvetica', 'B', 9)
        n_cols = len(headers)
        col_width = 190 / n_cols
        # Calculer les largeurs intelligemment
        if n_cols <= 3:
            col_widths = [190 / n_cols] * n_cols
        elif n_cols == 4:
            col_widths = [30, 55, 55, 50]
        elif n_cols == 5:
            col_widths = [20, 42, 42, 42, 44]
        else:
            col_widths = [190 / n_cols] * n_cols

        # En-tête
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            w = col_widths[i] if i < len(col_widths) else col_width
            self.cell(w, 7, h.strip(), border=1, fill=True, align='C')
        self.ln()

        # Lignes
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        for row_idx, row in enumerate(rows):
            if row_idx % 2 == 0:
                self.set_fill_color(236, 240, 241)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                w = col_widths[i] if i < len(col_widths) else col_width
                self.cell(w, 6, cell.strip()[:40], border=1, fill=True)
            self.ln()
        self.ln(4)

    def add_image_safe(self, path, w=160):
        if os.path.exists(path):
            self.image(path, x=25, w=w)
            self.ln(8)
        else:
            self.body_text(f"[Image non trouvée : {path}]")


def generate_journal_pdf():
    pdf = JournalPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    outputs_dir = os.path.join(base_dir, 'outputs')

    # ===== TITRE =====
    pdf.chapter_title("Journal de bord — Personne B")
    pdf.body_text("Projet : HAI716I Projet 2 — Tournoi de Dilemme du Prisonnier Itéré")
    pdf.body_text("Date de début : 13 novembre 2026")
    pdf.body_text("Deadline : Dimanche 15 novembre 2026, 23h59")
    pdf.ln(5)

    # ===== 1. PROTOCOLE =====
    pdf.chapter_title("1. Protocole", level=2)
    pdf.add_table(
        ['Paramètre', 'Valeur', 'Justification'],
        [
            ['Seed aléatoire', '42', 'Reproductibilité (énoncé)'],
            ['Tours/partie', '200', 'Format Axelrod (énoncé)'],
            ['Parties/paire', '5', 'Format Axelrod (énoncé)'],
            ['Format tournoi', 'Round-robin', 'Tous contre tous'],
        ]
    )

    pdf.chapter_title("Matrice de gains", level=3)
    pdf.add_table(
        ['', 'Adversaire: C', 'Adversaire: D'],
        [
            ['Je joue C', '(3, 3)', '(0, 5)'],
            ['Je joue D', '(5, 0)', '(2, 2)'],
        ]
    )
    pdf.body_text("T=5 > R=3 > P=2 > S=0 et 2R=6 > T+S=5 : dilemme du prisonnier vérifié.")

    pdf.chapter_title("Répartition du travail", level=3)
    pdf.body_text("Personne A (Heythem) : Moteur du tournoi (engine.py, gains.py), stratégies ALL-D et RANDOM, README.")
    pdf.body_text("Personne B (Moi) : Stratégies TIT-FOR-TAT, TESTER, JOSS, scripts d'expériences, tests, journal.")

    # ===== 2. STRATÉGIES =====
    pdf.add_page()
    pdf.chapter_title("2. Stratégies implémentées — Étape 1", level=2)

    strategies = [
        ("ALL-D — Toujours Trahir", 
         "Joue D à chaque tour, sans exception.",
         "Triviale, Axelrod 1980",
         "Ne se fait jamais exploiter. Max 5 pts/tour vs coopérateurs.",
         "Mutuelle défection = 2 pts/tour. Perd la coopération (3,3).",
         "Personne A"),
        ("RANDOM — Aléatoire 50/50",
         "Joue C ou D au hasard avec probabilité 50%.",
         "Baseline, Axelrod 1980",
         "Imprévisible.",
         "Score moyen faible, ne tire pas parti de la coopération.",
         "Personne A"),
        ("TIT-FOR-TAT — Oeil pour oeil",
         "Coopère au tour 0, puis copie le dernier coup adverse.",
         "Anatol Rapoport, Axelrod 1980 (gagnante)",
         "Gentille, rétorsive, pardonnante. Optimale si pop. coopérative.",
         "Vulnérable aux erreurs de JOSS (spirales de représailles).",
         "Moi (Personne B)"),
        ("TESTER — Le Testeur",
         "Trahit tour 0 pour tester. Si riposte -> TFT. Sinon -> exploite.",
         "Axelrod 1980",
         "Détecte et exploite les naïfs.",
         "Test initial coûte un tour face à TFT.",
         "Moi (Personne B)"),
        ("JOSS — Le Sournois",
         "TFT mais 10% de chance de trahir au lieu de coopérer.",
         "Axelrod 1980",
         "Vole des points par trahisons surprises.",
         "Déclenche des spirales de représailles avec TFT.",
         "Moi (Personne B)"),
    ]

    for name, regle, origine, force, faiblesse, par in strategies:
        pdf.chapter_title(name, level=3)
        pdf.add_table(
            ['Propriété', 'Description'],
            [
                ['Règle', regle],
                ['Origine', origine],
                ['Force', force],
                ['Faiblesse', faiblesse],
                ['Implémentée par', par],
            ]
        )

    # ===== 3. RÉSULTATS ÉTAPE 1 =====
    pdf.add_page()
    pdf.chapter_title("3. Résultats Étape 1 — Tournoi de base", level=2)

    pdf.chapter_title("3.1 Sortie du programme", level=3)
    pdf.code_block(
        "==================================================\n"
        "ÉTAPE 1 : TOURNOI DE BASE\n"
        "==================================================\n"
        "Seed: 42\n"
        "Parties par paire: 5\n"
        "Tours par partie: 200\n"
        "Stratégies: ['ALL-D', 'RANDOM', 'TIT-FOR-TAT', 'TESTER', 'JOSS']\n"
        "\n"
        "========================================\n"
        "CLASSEMENT FINAL\n"
        "========================================\n"
        "Rang  Stratégie              Score\n"
        "----------------------------------------\n"
        "1     ALL-D                   9545\n"
        "2     TIT-FOR-TAT             9109\n"
        "3     TESTER                  9003\n"
        "4     JOSS                    8714\n"
        "5     RANDOM                  8445\n"
        "========================================"
    )

    pdf.chapter_title("3.2 Classement", level=3)
    pdf.add_table(
        ['Rang', 'Stratégie', 'Score total', 'Moy/partie'],
        [
            ['1', 'ALL-D', '9545', '477.3'],
            ['2', 'TIT-FOR-TAT', '9109', '455.5'],
            ['3', 'TESTER', '9003', '450.2'],
            ['4', 'JOSS', '8714', '435.7'],
            ['5', 'RANDOM', '8445', '422.3'],
        ]
    )

    pdf.chapter_title("3.3 Graphique des scores", level=3)
    chart_path = os.path.join(outputs_dir, 'etape1_classement.png')
    pdf.add_image_safe(chart_path, w=150)

    pdf.chapter_title("3.4 Tests unitaires — 16/16 passés", level=3)
    pdf.code_block(
        "============================= test session starts ========\n"
        "platform win32 -- Python 3.12.10, pytest-9.2.0\n"
        "\n"
        "TestAllD::test_premier_tour PASSED           [  6%]\n"
        "TestAllD::test_toujours_D PASSED             [ 12%]\n"
        "TestRandom::test_retourne_C_ou_D PASSED      [ 18%]\n"
        "TestRandom::test_pas_toujours_pareil PASSED  [ 25%]\n"
        "TestTitForTat::test_premier_tour_coopere PASSED [ 31%]\n"
        "TestTitForTat::test_copie_cooperation PASSED [ 37%]\n"
        "TestTitForTat::test_copie_defection PASSED   [ 43%]\n"
        "TestTitForTat::test_sequence_complete PASSED  [ 50%]\n"
        "TestTitForTat::test_riposter_puis_pardonner PASSED [56%]\n"
        "TestTester::test_premier_tour_trahit PASSED  [ 62%]\n"
        "TestTester::test_deuxieme_tour_coopere PASSED [ 68%]\n"
        "TestTester::test_exploite_si_pas_riposte PASSED [75%]\n"
        "TestTester::test_tft_si_riposte PASSED       [ 81%]\n"
        "TestJoss::test_premier_tour_coopere PASSED   [ 87%]\n"
        "TestJoss::test_copie_defection PASSED        [ 93%]\n"
        "TestJoss::test_parfois_trahit_sur_coop PASSED [100%]\n"
        "\n"
        "=============== 16 passed in 0.08s ====================="
    )

    # ===== 4. ANALYSE TFT =====
    pdf.add_page()
    pdf.chapter_title("4. Analyse — TIT-FOR-TAT gagne-t-il ?", level=2)
    pdf.bold_text("Réponse : Non. C'est ALL-D qui gagne avec 9545 points.")
    pdf.ln(3)

    pdf.chapter_title("Pourquoi notre résultat diffère d'Axelrod 1980 ?", level=3)
    pdf.body_text(
        "Dans le tournoi original d'Axelrod, TIT-FOR-TAT gagnait car la population "
        "comptait 14 stratégies, dont beaucoup étaient coopératives ou semi-coopératives. "
        "TFT accumulait des gains mutuels élevés (3,3) avec ces partenaires."
    )
    pdf.body_text(
        "Dans notre tournoi à 5 stratégies, la situation est inverse :\n"
        "- ALL-D (pure trahison) ne perd jamais beaucoup : minimum 2 pts/tour.\n"
        "- TESTER et JOSS contiennent des composantes agressives.\n"
        "- RANDOM est imprévisible et ne récompense pas la coopération."
    )
    pdf.body_text(
        "TFT est pénalisé par chaque adversaire :\n"
        "- vs ALL-D : TFT coopère au tour 0 (score 0), puis mutuelle défection.\n"
        "  ALL-D gagne 5 pts au 1er tour.\n"
        "- vs JOSS : Les 10% de trahisons provoquent des spirales de représailles.\n"
        "- vs TESTER : TESTER trahit au tour 0, TFT riposte, handicap initial."
    )
    pdf.bold_text(
        "Conclusion : La composition de la population est déterminante. TFT excelle "
        "dans un environnement riche en coopérateurs, pas dans un groupe restreint "
        "et agressif comme le nôtre."
    )

    # ===== 5. IMPASSES =====
    pdf.chapter_title("5. Impasses et bugs rencontrés", level=2)

    pdf.chapter_title("Bug 1 — pytest confond tester() avec un fixture", level=3)
    pdf.body_text(
        "Problème : La fonction tester() de strategies.py est détectée par pytest comme "
        "un test potentiel (son nom commence par 'test'). pytest essaie de l'appeler "
        "comme un fixture, causant une erreur 'fixture historique_moi not found'."
    )
    pdf.body_text(
        "Solution : Renommer l'import dans le fichier de test "
        "(import tester as strat_tester) et configurer pytest.ini avec "
        "testpaths = tests pour limiter la collecte."
    )
    pdf.body_text(
        "Leçon : Éviter de nommer une fonction 'tester' dans un projet utilisant pytest."
    )

    pdf.chapter_title("Bug 2 — Dépendances PDF et portabilité", level=3)
    pdf.body_text(
        "Problème : WeasyPrint nécessite les bibliothèques GTK/Pango (libgobject) "
        "qui ne sont pas installées par défaut sur Windows."
    )
    pdf.body_text(
        "Solution : Utiliser fpdf2 à la place, qui est en Python pur et ne "
        "nécessite aucune dépendance système externe."
    )

    # ===== FICHIERS PRODUITS =====
    pdf.add_page()
    pdf.chapter_title("6. Fichiers produits — Étape 1", level=2)
    pdf.add_table(
        ['Fichier', 'Description'],
        [
            ['src/tournament/strategies.py', '5 stratégies de base'],
            ['src/experiments/step1_base.py', 'Script tournoi + export CSV'],
            ['tests/test_strategies.py', '16 tests unitaires (tous OK)'],
            ['outputs/etape1_classement.csv', 'Classement en CSV'],
            ['outputs/etape1_classement.png', 'Graphique en barres'],
            ['outputs/etape1_sortie_console.txt', 'Capture sortie console'],
            ['outputs/etape1_tests_console.txt', 'Capture sortie tests'],
            ['journal/journal_B.md', 'Journal (source Markdown)'],
            ['journal/journal_B.pdf', 'Journal (ce PDF)'],
        ]
    )

    # ========================================================================
    # ÉTAPE 2 — NOUVELLES STRATÉGIES + TOURNOI ÉLARGI
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title("7. Stratégies implémentées — Étape 2 (4 nouvelles)", level=2)

    strategies_etape2 = [
        ("GRIM TRIGGER (Personne A)",
         "Coopère tant que l'adversaire n'a jamais joué D. Au 1er D adverse, bascule en ALL-D définitif.",
         "Friedman 1971",
         "Coopération mutuelle parfaite (3,3) si adversaire coopère. Inexploitable.",
         "Impardonnable : une seule erreur/bruit = défection éternelle. Ne pardonne jamais.",
         "Personne A (Heythem)"),
        ("PAVLOV / Win-Stay Lose-Shift (Personne A)",
         "Tour 0: C. Si gain ≥ 3 (R/T) -> répète (Win-Stay). Si gain < 3 (P/S) -> change (Lose-Shift).",
         "Kraines & Kraines 1989",
         "S'adapte dynamiquement : maintient coopération, exploite naïfs, robuste au bruit.",
         "Peut entrer en cycles d'exploitation mutuelle contre certains adversaires.",
         "Personne A (Heythem)"),
        ("TFT-2T / Tit-For-Two-Tats (Personne B)",
         "Tour 0: C. Pardonne 1er D adverse. Ne riposte (D) qu'après 2 D consécutifs. Re-coopère si adv. re-coopère.",
         "Axelrod 1984 (The Evolution of Cooperation)",
         "Évite les spirales de représailles accidentelles (bruit). Plus tolérante que TFT.",
         "Trop tolérante : exploitée par ALL-D et TESTER qui comprennent qu'ils peuvent trahir une fois.",
         "Moi (Personne B)"),
        ("PROBER (Personne B)",
         "Tour 0: D (test). Tours 1-2: C,C. Si adv. riposte (D au tour 1 OU 2) -> TFT. Sinon -> exploite en alternant D/C.",
         "Li 2011 / variante Axelrod",
         "Identifie rapidement naïfs vs fermes. Exploite les naïfs, joue prudemment (TFT) contre les fermes.",
         "Test initial (D tour 0) coûte 3 pts vs coopérateurs. Handicap vs TFT/ALL-D au démarrage.",
         "Moi (Personne B)"),
    ]

    for name, regle, origine, force, faiblesse, par in strategies_etape2:
        pdf.chapter_title(name, level=3)
        pdf.add_table(
            ['Propriété', 'Description'],
            [
                ['Règle', regle],
                ['Origine', origine],
                ['Force', force],
                ['Faiblesse', faiblesse],
                ['Implémentée par', par],
            ]
        )

    # ===== 8. RÉSULTATS ÉTAPE 2 =====
    pdf.add_page()
    pdf.chapter_title("8. Résultats Étape 2 — Tournoi élargi (9 stratégies)", level=2)

    pdf.chapter_title("8.1 Sortie du programme", level=3)
    pdf.code_block(
        "==================================================\n"
        "ÉTAPE 2 : TOURNOI ÉLARGI (9 stratégies)\n"
        "==================================================\n"
        "Seed: 42\n"
        "Parties par paire: 5\n"
        "Tours par partie: 200\n"
        "Stratégies: ['ALL-D', 'RANDOM', 'TIT-FOR-TAT', 'TESTER', 'JOSS',\n"
        "  'GRIM', 'PAVLOV', 'TFT-2T', 'PROBER']\n"
        "\n"
        "========================================\n"
        "CLASSEMENT FINAL\n"
        "========================================\n"
        "Rang  Stratégie              Score\n"
        "----------------------------------------\n"
        "1     TIT-FOR-TAT            21104\n"
        "2     GRIM                   20489\n"
        "3     PROBER                 20347\n"
        "4     TESTER                 19843\n"
        "5     PAVLOV                 19403\n"
        "6     ALL-D                  19120\n"
        "7     TFT-2T                 18630\n"
        "8     JOSS                   18293\n"
        "9     RANDOM                 17785\n"
        "========================================"
    )

    pdf.chapter_title("8.2 Classement détaillé", level=3)
    pdf.add_table(
        ['Rang', 'Stratégie', 'Score', 'Moy/partie', 'Origine'],
        [
            ['1', 'TIT-FOR-TAT', '21104', '469.0', 'Base'],
            ['2', 'GRIM', '20489', '455.3', 'A'],
            ['3', 'PROBER', '20347', '452.2', 'B'],
            ['4', 'TESTER', '19843', '441.0', 'Base'],
            ['5', 'PAVLOV', '19403', '431.2', 'A'],
            ['6', 'ALL-D', '19120', '424.9', 'Base'],
            ['7', 'TFT-2T', '18630', '414.0', 'B'],
            ['8', 'JOSS', '18293', '406.5', 'Base'],
            ['9', 'RANDOM', '17785', '395.2', 'Base'],
        ]
    )

    pdf.chapter_title("8.3 Graphiques", level=3)
    pdf.body_text("Classement complet (9 stratégies) :")
    chart_path = os.path.join(outputs_dir, 'etape2_classement.png')
    pdf.add_image_safe(chart_path, w=150)

    pdf.body_text("Comparatif Étape 1 vs Étape 2 (5 stratégies communes) :")
    chart_path2 = os.path.join(outputs_dir, 'etape2_comparaison.png')
    pdf.add_image_safe(chart_path2, w=150)

    # ===== 9. ANALYSE COMPARATIVE =====
    pdf.add_page()
    pdf.chapter_title("9. Analyse comparative — Étape 1 vs Étape 2", level=2)

    pdf.chapter_title("9.1 Changement majeur : TIT-FOR-TAT redevient gagnante !", level=3)
    pdf.bold_text("Dans l'Étape 1 (5 stratégies hostiles), ALL-D dominait.")
    pdf.bold_text("Dans l'Étape 2 (9 stratégies), TIT-FOR-TAT gagne (21104) avec une large avance.")

    pdf.body_text(
        "L'ajout de GRIM, PROBER et PAVLOV a créé une population majoritairement "
        "coopérative/cond. coopérative (5 sur 9 stratégies coopèrent avec TFT). "
        "TFT accumule ainsi des scores élevés (3,3) contre 4 nouveaux partenaires, "
        "doublant presque son avantage."
    )

    pdf.add_table(
        ['Facteur', 'Étape 1 (5 strat.)', 'Étape 2 (9 strat.)'],
        [
            ['Partenaires coop. pour TFT', '0 (TESTER, JOSS trahissent)', '4 (GRIM, PROBER->TFT, PAVLOV, TFT-2T)'],
            ['Score TFT', '9109 (2ème)', '21104 (1er, +132%)'],
            ['Score ALL-D', '9545 (1er)', '19120 (6ème, +100% seulement)'],
        ]
    )

    pdf.chapter_title("9.2 Performance des nouvelles stratégies (Personne B)", level=3)

    pdf.bold_text("PROBER (3ème place - 20347) — EXCELLENT !")
    pdf.body_text(
        "Batte ALL-D, TESTER, JOSS, TFT-2T, RANDOM. Perd seulement vs TFT, GRIM, PAVLOV (très peu). "
        "Stratégie 'intelligente' : sonde puis s'adapte optimalement."
    )

    pdf.bold_text("TFT-2T (7ème place - 18630) — DÉCEVANTE")
    pdf.body_text(
        "Perd vs TFT, GRIM, PROBER, TESTER, PAVLOV, ALL-D. "
        "Trop tolérante : se fait exploiter par ALL-D (ne riposte qu'au 2ème D). "
        "Contre TESTER : TESTER trahit tour 0 -> TFT-2T pardonne -> TESTER exploite. "
        "Leçon : Dans un environnement hostile, la tolérance excessive est punie."
    )

    pdf.chapter_title("9.3 Évolution des scores (facteur ×2.2 dû aux 8 adversaires vs 4)", level=3)
    pdf.add_table(
        ['Stratégie', 'Étape 1', 'Étape 2', 'Ratio', 'Interprétation'],
        [
            ['TIT-FOR-TAT', '9109', '21104', '2.32', 'Meilleure progression - profite des nouveaux coop.'],
            ['GRIM', '—', '20489', '—', 'Très forte en pop. coopérative'],
            ['PROBER', '—', '20347', '—', 'Excellente adaptation'],
            ['TESTER', '9003', '19843', '2.20', 'Progression standard'],
            ['PAVLOV', '—', '19403', '—', 'Correcte'],
            ['ALL-D', '9545', '19120', '2.00', 'Pire progression - perd avantage 1er tour'],
            ['TFT-2T', '—', '18630', '—', 'Sous-performe'],
            ['JOSS', '8714', '18293', '2.10', 'Standard'],
            ['RANDOM', '8445', '17785', '2.11', 'Standard'],
        ]
    )

    # ===== 10. TESTS UNITAIRES =====
    pdf.add_page()
    pdf.chapter_title("10. Tests unitaires — 31/31 passés", level=2)
    pdf.code_block(
        "============================= test session starts ========\n"
        "platform win32 -- Python 3.12.10, pytest-9.2.0\n"
        "collected 31 items\n"
        "\n"
        "TestAllD::test_premier_tour PASSED             [  3%]\n"
        "TestAllD::test_toujours_D PASSED               [  6%]\n"
        "TestRandom::test_retourne_C_ou_D PASSED        [  9%]\n"
        "TestRandom::test_pas_toujours_pareil PASSED    [ 12%]\n"
        "TestTitForTat::test_premier_tour_coopere PASSED [ 16%]\n"
        "TestTitForTat::test_copie_cooperation PASSED   [ 19%]\n"
        "TestTitForTat::test_copie_defection PASSED     [ 22%]\n"
        "TestTitForTat::test_sequence_complete PASSED   [ 25%]\n"
        "TestTitForTat::test_riposter_puis_pardonner PASSED [ 29%]\n"
        "TestTester::test_premier_tour_trahit PASSED    [ 32%]\n"
        "TestTester::test_deuxieme_tour_coopere PASSED  [ 35%]\n"
        "TestTester::test_exploite_si_pas_riposte PASSED [ 38%]\n"
        "TestTester::test_tft_si_riposte PASSED         [ 41%]\n"
        "TestJoss::test_premier_tour_coopere PASSED     [ 45%]\n"
        "TestJoss::test_copie_defection PASSED          [ 48%]\n"
        "TestJoss::test_parfois_trahit_sur_coop PASSED  [ 51%]\n"
        "TestGrim::test_premier_tour_coopere PASSED     [ 54%]\n"
        "TestGrim::test_coopere_tant_que_pas_de_D PASSED [ 58%]\n"
        "TestGrim::test_bascule_apres_premier_D PASSED  [ 61%]\n"
        "TestPavlov::test_premier_tour_coopere PASSED   [ 64%]\n"
        "TestPavlov::test_win_stay PASSED               [ 67%]\n"
        "TestPavlov::test_lose_shift PASSED             [ 70%]\n"
        "TestTFT2T::test_premier_tour_coopere PASSED    [ 74%]\n"
        "TestTFT2T::test_pardonne_premier_D PASSED      [ 77%]\n"
        "TestTFT2T::test_ripote_apres_deux_D PASSED     [ 80%]\n"
        "TestTFT2T::test_recoopere_apres_ripote PASSED  [ 83%]\n"
        "TestProber::test_premier_tour_trahit PASSED    [ 87%]\n"
        "TestProber::test_deuxieme_tour_coopere PASSED  [ 90%]\n"
        "TestProber::test_troisieme_tour_coopere PASSED [ 93%]\n"
        "TestProber::test_passe_en_tft_si_riposte PASSED [ 96%]\n"
        "TestProber::test_exploite_si_pas_riposte PASSED [100%]\n"
        "\n"
        "=============== 31 passed in 0.11s ====================="
    )

    # ===== 11. FICHIERS PRODUITS ÉTAPE 2 =====
    pdf.add_page()
    pdf.chapter_title("11. Fichiers produits — Étape 2", level=2)
    pdf.add_table(
        ['Fichier', 'Description'],
        [
            ['src/tournament/strategies.py', '9 stratégies (5 base + 2 A + 2 B)'],
            ['src/experiments/step2_new.py', 'Script tournoi élargi + graphiques'],
            ['src/experiments/generate_charts.py', 'Génération 3 graphiques'],
            ['tests/test_strategies.py', '31 tests unitaires (tous OK)'],
            ['outputs/etape2_classement.csv', 'Classement 9 strat. en CSV'],
            ['outputs/etape2_classement.png', 'Graphique classement 9 strat. (couleurs origine)'],
            ['outputs/etape2_comparaison.png', 'Graphique comparatif Étape 1 vs 2'],
            ['outputs/etape2_sortie_console.txt', 'Capture sortie console complète'],
            ['outputs/etape2_tests_console.txt', 'Capture sortie tests 31'],
            ['journal/journal_B.md', 'Journal (source Markdown, mis à jour)'],
            ['journal/journal_B.pdf', 'Journal (ce PDF, complet Étape 1+2)'],
        ]
    )

    # Sauvegarder
    pdf_path = os.path.join(base_dir, 'journal', 'journal_B.pdf')
    pdf.output(pdf_path)
    print(f"PDF généré : {pdf_path}")


if __name__ == "__main__":
    generate_journal_pdf()
