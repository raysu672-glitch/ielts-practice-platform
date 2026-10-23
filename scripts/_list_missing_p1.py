# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

def norm(s):
    s=s.lower().strip().replace("'", "'").replace("'", "'")
    return re.sub(r'[^a-z0-9]+','',s)

heat=json.loads(Path('_p1_heat_parsed.json').read_text(encoding='utf-8'))
clue=json.loads(Path('_p1_clue_index.json').read_text(encoding='utf-8'))['index']
missing=[]
matched=0
for cat in heat:
    for topic in cat['topics']:
        for q in topic['questions']:
            k=norm(q)
            if k in clue:
                matched+=1
            else:
                missing.append((cat['id'], topic['topicEn'], q))
print('matched', matched, 'missing', len(missing))
lines=[]
for cid, top, q in missing:
    lines.append(f'{cid}\t{top}\t{q}')
Path('_p1_missing_clues.txt').write_text('\n'.join(lines), encoding='utf-8')
print('wrote', len(lines))
