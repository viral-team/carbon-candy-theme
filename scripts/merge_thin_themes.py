#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEMES_DIR = HERE / '..' / 'themes'

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def merge(base, thin):
    # merge colors: add keys from base that are missing in thin
    base_colors = base.get('colors', {})
    thin_colors = thin.get('colors', {})
    for k, v in base_colors.items():
        if k not in thin_colors:
            thin_colors[k] = v
    if thin_colors:
        thin['colors'] = thin_colors

    # tokenColors: if missing or empty in thin, copy from base
    if not thin.get('tokenColors'):
        if base.get('tokenColors'):
            thin['tokenColors'] = base.get('tokenColors')

    # semanticTokenColors: copy if missing
    if 'semanticTokenColors' not in thin and 'semanticTokenColors' in base:
        thin['semanticTokenColors'] = base['semanticTokenColors']

    # semanticHighlighting: copy if missing
    if 'semanticHighlighting' not in thin and 'semanticHighlighting' in base:
        thin['semanticHighlighting'] = base['semanticHighlighting']

    # Ensure icon.foreground uses the theme's main accent color
    accent_keys = [
        'pickerGroup.foreground',
        'activityBar.foreground',
        'textLink.foreground',
        'button.background',
        'progressBar.background',
        'extensionButton.foreground',
        'activityBarBadge.background',
        'selection.background',
        'foreground'
    ]
    accent = None
    for k in accent_keys:
        if k in base_colors:
            accent = base_colors[k]
            break

    def add_alpha(hexcolor, alpha='b3'):
        if not isinstance(hexcolor, str):
            return hexcolor
        h = hexcolor.strip()
        if h.startswith('#') and len(h) == 7:
            return h + alpha
        return h

    if accent:
        thin_colors['icon.foreground'] = add_alpha(accent)

    return thin

def main():
    themes_path = (HERE / '..' / 'themes').resolve()
    for p in themes_path.glob('*.json'):
        name = p.name
        if name.endswith('-thin-border.json'):
            base_name = name.replace('-thin-border.json', '.json')
            base_path = themes_path / base_name
            if not base_path.exists():
                print('base not found for', name)
                continue
            print('Merging', base_name, '->', name)
            base = load(base_path)
            thin = load(p)
            merged = merge(base, thin)
            save(p, merged)

if __name__ == '__main__':
    main()
