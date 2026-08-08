# -*- coding: utf-8 -*-
import json
import re
import os

def structure_explanation(text):
    if not text:
        return ""

    # 1. Flow Diagrams: X ↓ Y ↓ Z -> X \n ↓ \n Y \n ↓ \n Z
    # Better: Use the user's requested format:
    # X
    # ↓
    # Y
    # ↓
    # Z
    structured = text.replace(' ↓ ', '\n↓\n')

    # 2. Bolding: Identify key terms and wrap in **
    # Keywords provided by user: "Ring lesion detected", "Perform MR spectroscopy", "Analyze peaks", "Narrow diagnosis"
    # Also general medical terms
    keywords = [
        "Ring lesion detected", "Perform MR spectroscopy", "Analyze peaks", "Narrow diagnosis",
        "Tuberculoma", "Abscess", "Tumor", "NCC", "Lipid", "Lactate", "Amino acids", "Choline", "NAA",
        "CSF CBNAAT", "TB meningitis", "PET", "B-scan"
    ]
    for kw in keywords:
        # Avoid double bolding
        pattern = rf'(?<!\*\*)\b({re.escape(kw)})\b(?!\*\*)'
        structured = re.sub(pattern, r'**\1**', structured, flags=re.IGNORECASE)

    # 3. Tables: Identify pipe-separated content and format as markdown tables
    # If the text already has | | pipes, we just need to ensure the separator line is there
    lines = structured.split('\n')
    new_lines = []
    in_table = False
    table_lines = []

    for line in lines:
        if '|' in line and line.count('|') >= 2:
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                if len(table_lines) >= 1:
                    # Add separator line if missing
                    has_sep = any('---' in tl for tl in table_lines)
                    if not has_sep:
                        # Create separator based on first row
                        cols = table_lines[0].count('|') - 1
                        if cols <= 0: cols = table_lines[0].count('|') + 1 # fallback
                        sep = '|' + '|'.join(['---'] * cols) + '|'
                        # Insert after first row (header)
                        table_lines.insert(1, sep)
                    new_lines.extend(table_lines)
                in_table = False
                table_lines = []
            new_lines.append(line)

    if in_table:
        if len(table_lines) >= 1:
            has_sep = any('---' in tl for tl in table_lines)
            if not has_sep:
                cols = table_lines[0].count('|') - 1
                if cols <= 0: cols = table_lines[0].count('|') + 1
                sep = '|' + '|'.join(['---'] * cols) + '|'
                table_lines.insert(1, sep)
            new_lines.extend(table_lines)

    return '\n'.join(new_lines).strip()

def main():
    base = os.path.dirname(__file__)
    # Read from with_imgs.json which has embedded images
    inp = os.path.join(base, 'with_imgs.json')
    out = os.path.join(base, 'merged_structured.json')

    if not os.path.exists(inp):
        print(f"Error: {inp} not found")
        return

    with open(inp, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {len(data)} questions...")

    for q in data:
        if 'ex' in q:
            q['ex'] = structure_explanation(q['ex'])

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"Saved structured explanations to {out}")

    # Also update core_btr.js
    js_out = os.path.join(base, '..', '..', 'questions', 'core_btr.js')
    with open(js_out, 'w', encoding='utf-8') as f:
        f.write('window.CORE_BTR = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
    print(f"Updated {js_out}")

if __name__ == "__main__":
    main()
