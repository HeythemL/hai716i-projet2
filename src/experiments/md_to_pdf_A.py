"""
Convertit journal_A.md en journal_A.pdf avec fpdf2.
Version générique pour tout markdown simple.
"""
import os
import sys
from fpdf import FPDF


class SimplePDF(FPDF):
    def normalize_text(self, text):
        if isinstance(text, str):
            text = text.replace('—', '-').replace('–', '-').replace('—', '-')
            text = text.replace('’', "'").replace('‘', "'")
            text = text.replace('“', '"').replace('”', '"')
            text = text.replace('🥇', '1.').replace('🥈', '2.').replace('🥉', '3.')
            text = text.replace('✅', '[OK]').replace('❌', '[X]')
            text = text.replace('≥', '>=').replace('≤', '<=')
            text = text.replace('→', '->').replace('×', 'x')
            # Handle accents
            for a, b in [('é', 'e'), ('è', 'e'), ('ê', 'e'), ('à', 'a'),
                         ('ù', 'u'), ('ô', 'o'), ('î', 'i'), ('ç', 'c'),
                         ('â', 'a'), ('ï', 'i'), ('œ', 'oe'), ('æ', 'ae')]:
                text = text.replace(a, b).replace(a.upper(), b.upper())
        return super().normalize_text(text)

    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, 'HAI716I Projet 2 - Journal de bord - Personne A (Heythem)', align='C')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


def markdown_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = SimplePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 11)

    in_code_block = False
    code_lines = []

    for line in lines:
        line = line.rstrip('\n')

        # Code block handling
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                # Output code block
                pdf.set_font('Courier', '', 8)
                pdf.set_fill_color(240, 240, 240)
                for cl in code_lines:
                    pdf.cell(0, 4, pdf.normalize_text(cl), new_x="LMARGIN", new_y="NEXT", fill=True)
                pdf.ln(3)
                pdf.set_font('Helvetica', '', 11)
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Headers
        if line.startswith('# '):
            pdf.set_font('Helvetica', 'B', 18)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 12, pdf.normalize_text(line[2:].strip()), new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(52, 152, 219)
            pdf.set_line_width(0.8)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(6)
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith('## '):
            pdf.set_font('Helvetica', 'B', 14)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 10, pdf.normalize_text(line[3:].strip()), new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(189, 195, 199)
            pdf.set_line_width(0.3)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith('### '):
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 8, pdf.normalize_text(line[4:].strip()), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)

        # Horizontal rule
        elif line.strip() == '---':
            pdf.ln(3)
            pdf.set_draw_color(189, 195, 199)
            pdf.set_line_width(0.3)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

        # Table handling (simple markdown tables)
        elif '|' in line and line.count('|') >= 2:
            # Check if it's a separator line
            if all(c in '|:- ' for c in line):
                continue  # Skip separator
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                pdf.set_font('Helvetica', '', 9)
                col_width = 190 / len(cells)
                for cell in cells:
                    pdf.cell(col_width, 5, pdf.normalize_text(cell)[:40], border=1, align='C')
                pdf.ln(5)

        # Bold text
        elif '**' in line:
            pdf.set_font('Helvetica', '', 11)
            parts = line.split('**')
            for i, part in enumerate(parts):
                if i % 2 == 1:
                    pdf.set_font('Helvetica', 'B', 11)
                else:
                    pdf.set_font('Helvetica', '', 11)
                pdf.write(5, pdf.normalize_text(part))
            pdf.ln(5)

        # Bullet points
        elif line.strip().startswith('- '):
            pdf.set_font('Helvetica', '', 11)
            pdf.cell(8, 5, '')
            pdf.cell(0, 5, pdf.normalize_text(line.strip()[2:]), new_x="LMARGIN", new_y="NEXT")

        # Checkbox items
        elif '- [x]' in line.lower() or '- [ ]' in line.lower():
            pdf.set_font('Helvetica', '', 11)
            checkbox = '[OK]' if '[x]' in line.lower() else '[  ]'
            text = line.replace('[x]', '').replace('[X]', '').replace('[ ]', '').strip()
            if text.startswith('- '):
                text = text[2:]
            pdf.cell(8, 5, '')
            pdf.cell(0, 5, f'{checkbox} {pdf.normalize_text(text)}', new_x="LMARGIN", new_y="NEXT")

        # Regular paragraph
        elif line.strip():
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(0, 5, pdf.normalize_text(line))

        # Empty line
        else:
            pdf.ln(3)

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf.output(pdf_path)
    print(f"PDF genere : {pdf_path}")


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        md_path = sys.argv[1]
        pdf_path = sys.argv[2]
    else:
        md_path = 'journal/journal_A.md'
        pdf_path = 'journal/journal_A.pdf'
    markdown_to_pdf(md_path, pdf_path)