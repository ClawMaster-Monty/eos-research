import re

# Read the Minimax packet
with open("C:\\Users\\monty\\eos-research\\research\\_drafts\\The COSMOS Multivitamin Trial by Minimax M3.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Parse sections
section_map = {}
current_key = "preamble"
buffer = []

for line in content.split('\n'):
    m = re.match(r'^## (\d+\..+)$', line)
    if m:
        section_map[current_key] = '\n'.join(buffer)
        current_key = m.group(1).strip()
        buffer = []
    else:
        buffer.append(line)
section_map[current_key] = '\n'.join(buffer)

for k in list(section_map.keys())[:5]:
    text = section_map[k][:200].strip()
    print(f"[{k[:60]}]: {text[:120]}")

print(f"\n\nTotal sections: {len(section_map)}")
print(f"Section keys:")
for k in section_map:
    print(f"  {k[:80]}")
