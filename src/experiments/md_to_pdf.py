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
            text = text.replace('—', '-').replace('–', '-').replace('’', "'").replace('“', '"').replace('”', '"')
            text = text.replace('🥇', '1.').replace('🥈', '2.').replace('🥉', '3.').replace('✅', '[OK]')
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

    # Sauvegarder
    pdf_path = os.path.join(base_dir, 'journal', 'journal_B.pdf')
    pdf.output(pdf_path)
    print(f"PDF généré : {pdf_path}")


if __name__ == "__main__":
    generate_journal_pdf()
