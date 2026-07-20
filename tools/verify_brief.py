#!/usr/bin/env python
"""Fail-closed claim/source gate for EOS Research HTML briefs."""

import argparse
import json
import re
from pathlib import Path


REQUIRED_SOURCE_FIELDS = ("citation", "reference_id", "evidence_level", "claims", "claim_ids", "verification_note")


def text_only(html):
    return re.sub(r"<[^>]+>", " ", html)


def cited_numbers(html):
    numbers = set()
    for contents in re.findall(r"<sup[^>]*>(.*?)</sup>", html, flags=re.IGNORECASE | re.DOTALL):
        numbers.update(int(value) for value in re.findall(r"\b\d+\b", contents))
    return numbers


def reference_entries(html):
    section = re.search(
        r'<div\b[^>]*class=["\'][^"\']*references-list[^"\']*["\'][^>]*>(.*?)</div>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    reference_html = section.group(1) if section else html
    return re.findall(r"(<li\b[^>]*>.*?</li>)", reference_html, flags=re.IGNORECASE | re.DOTALL)


def source_identifier(source):
    return source.get("doi") or source.get("pmid") or ""


def verify_brief(brief_path, registry_path):
    html = Path(brief_path).read_text(encoding="utf-8")
    registry = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    sources_list = registry.get("sources", [])
    citation_ids = [int(item["citation"]) for item in sources_list]
    sources = {int(item["citation"]): item for item in sources_list}
    cited = cited_numbers(html)
    first_appearance = []
    for contents in re.findall(r"<sup[^>]*>(.*?)</sup>", html, flags=re.IGNORECASE | re.DOTALL):
        for value in re.findall(r"\b\d+\b", text_only(contents)):
            citation = int(value)
            if citation not in first_appearance:
                first_appearance.append(citation)
    errors = []
    expected_order = list(range(1, len(first_appearance) + 1))
    if first_appearance != expected_order:
        errors.append(f"citations are not numbered by first appearance: {first_appearance}")
    for contents in re.findall(r"<sup[^>]*>(.*?)</sup>", html, flags=re.IGNORECASE | re.DOTALL):
        numeric = {int(value) for value in re.findall(r"\b\d+\b", text_only(contents))}
        linked = {int(value) for value in re.findall(r'href=["\']#ref(\d+)["\']', contents, flags=re.IGNORECASE)}
        if numeric != linked:
            errors.append(f"superscript citations must be linked to matching references: numbers={sorted(numeric)}, links={sorted(linked)}")
    section = re.search(r'<div\b[^>]*class=["\'][^"\']*references-list[^"\']*["\'][^>]*>(.*?)</div>', html, flags=re.IGNORECASE | re.DOTALL)
    listed = reference_entries(html) if section else []
    rendered_reference_ids = [
        match.group(1)
        for entry in listed
        if (match := re.search(r'id=["\']([^"\']+)["\']', entry, flags=re.IGNORECASE))
    ]
    if len(rendered_reference_ids) != len(set(rendered_reference_ids)):
        errors.append("duplicate rendered reference id")
    if len(listed) > len(sources_list):
        errors.append("uncatalogued reference entry")
    if not section:
        errors.append("missing dedicated references-list container")
    if len(citation_ids) != len(set(citation_ids)):
        errors.append("duplicate registry citation")
    doi_ids = [str(item.get("doi", "")).lower() for item in sources_list if item.get("doi")]
    pmid_ids = [str(item.get("pmid", "")) for item in sources_list if item.get("pmid")]
    if len(doi_ids) != len(set(doi_ids)) or len(pmid_ids) != len(set(pmid_ids)):
        errors.append("duplicate source identifier")
    claim_map = {}
    claim_pattern = re.compile(
        r'<(?P<tag>[a-z][a-z0-9]*)\b[^>]*data-claim-id=["\'](?P<claim>[^"\']+)["\'][^>]*>(?P<body>.*?)</(?P=tag)>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    for match in claim_pattern.finditer(html):
        for citation in cited_numbers(match.group("body")):
            claim_map.setdefault(citation, set()).add(match.group("claim"))

    for citation in sorted(cited):
        source = sources.get(citation)
        if not source:
            errors.append(f"citation {citation} has no registry record")
            continue
        for field in REQUIRED_SOURCE_FIELDS:
            if not source.get(field):
                errors.append(f"citation {citation} is missing {field}")
        rendered_claim_ids = claim_map.get(citation, set())
        registered_claim_ids = set(source.get("claim_ids", []))
        if rendered_claim_ids != registered_claim_ids:
            missing = sorted(rendered_claim_ids - registered_claim_ids)
            extra = sorted(registered_claim_ids - rendered_claim_ids)
            errors.append(
                f"citation {citation} claim_ids mismatch; missing={missing}, extra={extra}"
            )
        if not source_identifier(source):
            errors.append(f"citation {citation} is missing doi or pmid")
        if citation > len(listed):
            errors.append(f"citation {citation} has no listed reference")
            continue
        reference_markup = listed[citation - 1]
        reference_text = text_only(reference_markup)
        if source.get("reference_id") and not re.search(r'id=["\']' + re.escape(source["reference_id"]) + r'["\']', reference_markup):
            errors.append(f"citation {citation} does not map to its rendered reference")
        if source.get("doi") and source["doi"].lower() not in reference_markup.lower():
            errors.append(f"citation {citation} DOI does not match its listed reference")
        if source.get("pmid") and str(source["pmid"]) not in reference_text:
            errors.append(f"citation {citation} PMID does not match its listed reference")

    for citation in sorted(sources):
        if citation not in cited:
            errors.append(f"registry citation {citation} is not cited in the brief")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Verify EOS claim/source registry coverage.")
    parser.add_argument("brief", type=Path)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    errors = verify_brief(args.brief, args.registry)
    if errors:
        print("SOURCE VERIFICATION FAILED")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("SOURCE VERIFICATION PASSED")


if __name__ == "__main__":
    main()
