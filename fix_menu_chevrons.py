#!/usr/bin/env python3
"""
Fix menu chevron inconsistencies.
When submenu has 'show' class, chevron should be 'bi-chevron-up'
When submenu doesn't have 'show' class, chevron should be 'bi-chevron-down'
"""

import re
from pathlib import Path

def fix_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all menu-submenu pairs
    # Pattern: button with chevron -> div with submenu class
    
    original = content
    
    # Pattern 1: chevron-down + submenu show (incorrect)
    pattern1 = r'(<button[^>]*?>.*?<i[^>]*?bi bi-chevron-down[^>]*?</i>.*?</button>\s*<div class="submenu show")'
    replacement1 = lambda m: m.group(1).replace('bi-chevron-down', 'bi-chevron-up')
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # Pattern 2: chevron-up + submenu without show (incorrect) 
    pattern2 = r'(<button[^>]*?>.*?<i[^>]*?bi bi-chevron-up[^>]*?</i>.*?</button>\s*<div class="submenu"(?!\s+show))'
    replacement2 = lambda m: m.group(1).replace('bi-chevron-up', 'bi-chevron-down')
    content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

templates_dir = Path('interfaces/web/templates')
modified = []

for html_file in sorted(templates_dir.glob('*.html')):
    if fix_template(html_file):
        modified.append(html_file.name)
        print(f"✓ {html_file.name}")

print(f"\nTotal fixed: {len(modified)}")
