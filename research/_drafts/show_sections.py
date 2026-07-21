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

for k, v in section_map.items():
    print(f"=== Section: {k[:70]} ===")
    print(v[:500])
    print(f"\n[... {len(v)} chars total]")
    print()
