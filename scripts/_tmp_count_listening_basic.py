import re
from pathlib import Path

text = Path("sources/tinglidanciceshi/js/modules.js").read_text(encoding="utf-8")
m = re.search(r"var allWordsListeningBasic\s*=\s*\[(.*?)\];", text, re.S)
body = m.group(1)
words = re.findall(r'"([^"]+)"', body)
print("count", len(words))
print("unique", len(set(words)))
print("first", words[:3])
print("last", words[-3:])
