#!/usr/bin/env python
"""EOS access-barrier ledger validator.

Fails closed (exit 1) if any record is missing required fields,
has an unknown access_class or evidence_status, or lacks a next_route.
"""

import json, sys
from pathlib import Path

SCHEMA_ACCESS_CLASSES = {
    "open", "authenticated-public", "archive-partial", "account-gated",
    "private-permission", "deleted", "paywalled", "robots-limited",
    "captcha-limited", "metadata-only", "nonpublic",
}
SCHEMA_EVIDENCE_STATUSES = {
    "unresolved", "partial", "captured", "documented", "verified",
    "non_recoverable",
}
REQUIRED = [
    "source_id", "platform", "url", "query", "date",
    "access_class", "evidence_status", "next_route",
    "evidentiary_consequence",
]

def validate(path: Path):
    bad = []
    n = 0
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            bad.append({"line": i, "error": f"json: {e}"})
            continue
        n += 1
        for k in REQUIRED:
            if not obj.get(k):
                bad.append({"line": i, "source_id": obj.get("source_id"), "error": f"missing {k}"})
        if obj.get("access_class") not in SCHEMA_ACCESS_CLASSES:
            bad.append({"line": i, "source_id": obj.get("source_id"), "error": f"bad access_class {obj.get('access_class')}"})
        if obj.get("evidence_status") not in SCHEMA_EVIDENCE_STATUSES:
            bad.append({"line": i, "source_id": obj.get("source_id"), "error": f"bad evidence_status {obj.get('evidence_status')}"})
    return n, bad

if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("research/_drafts/wolverine-sources/access-barrier-ledger.jsonl")
    n, bad = validate(path)
    print(f"records: {n}")
    print(f"errors:  {len(bad)}")
    for b in bad[:25]:
        print(json.dumps(b, ensure_ascii=False))
    sys.exit(1 if bad else 0)