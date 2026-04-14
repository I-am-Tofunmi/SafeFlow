import re

def update_dates(filepath, regex_pattern, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(f'({regex_pattern})', content)
    
    new_content = ""
    rep_idx = 0
    for i, part in enumerate(parts):
        if i % 2 == 1: # This is a match
            new_content += replacements[rep_idx % len(replacements)]
            rep_idx += 1
        else:
            new_content += part
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Update transaction.html
trx_replacements = [
    'Apr 14, 2026',
    'Apr 13, 2026',
    'Mar 30, 2026',
    'Feb 15, 2026',
    'Dec 22, 2025',
    'Nov 12, 2025',
    'Oct 10, 2025'
]
update_dates('frontends/transaction.html', r'[A-Z][a-z]{2} \d{1,2}, 202[3-6]', trx_replacements)

# Update homepage.html
with open('frontends/homepage.html', 'r', encoding='utf-8') as f:
    hp_content = f.read()
hp_content = hp_content.replace('Oct 23, 10:00 AM', 'Apr 11, 2026, 10:00 AM')
with open('frontends/homepage.html', 'w', encoding='utf-8') as f:
    f.write(hp_content)

print("Dates updated!")
