#!/usr/bin/env python3
"""Validate observations and build the deployable Life-Support Atlas payload."""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
WEB = ROOT / "web"
OUTPUT = ROOT / "outputs" / "web"
REQUIRED = {"region_id","region_name","iso3","year","domain","indicator_id","value","unit","direction","normalization_min","normalization_max","source_id","source_version","source_url","retrieved_at","provenance_status","notes"}
ALLOWED_PROVENANCE = {"official","modeled","estimated","imputed","community-submitted","reviewed"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def regions_from_geometry() -> list[dict]:
    geometry = load_json(DATA / "raw" / "world.geojson")
    regions = []
    for feature in geometry["features"]:
        props = feature["properties"]
        name = props.get("ADMIN") or props.get("NAME")
        iso3 = props.get("ADM0_A3") or props.get("ISO_A3") or ""
        regions.append({"id": iso3 if iso3 != "-99" else name.lower().replace(" ", "-"), "name": name, "iso3": iso3})
    return sorted(regions, key=lambda item: item["name"])


def load_observations(domain_ids: set[str]) -> list[dict]:
    with (DATA / "observations.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != REQUIRED:
            raise ValueError("observations.csv fields do not match the published contract")
        rows = []
        for line, row in enumerate(reader, 2):
            if row["domain"] not in domain_ids:
                raise ValueError(f"line {line}: unknown domain {row['domain']}")
            if row["provenance_status"] not in ALLOWED_PROVENANCE:
                raise ValueError(f"line {line}: invalid provenance status")
            if not row["source_version"] or not row["source_url"] or not row["retrieved_at"]:
                raise ValueError(f"line {line}: incomplete provenance")
            for key in ("value", "normalization_min", "normalization_max"):
                row[key] = float(row[key])
            row["year"] = int(row["year"])
            low, high = row["normalization_min"], row["normalization_max"]
            if high <= low or row["direction"] not in {"higher-is-resilient", "lower-is-resilient"}:
                raise ValueError(f"line {line}: invalid normalization rule")
            scaled = min(1.0, max(0.0, (row["value"] - low) / (high - low)))
            row["normalized"] = scaled if row["direction"] == "higher-is-resilient" else 1 - scaled
            rows.append(row)
    return rows


def score_regions(regions: list[dict], domains: list[dict], observations: list[dict]) -> list[dict]:
    latest: dict[tuple[str,str,str],dict] = {}
    for row in observations:
        key = row["region_id"], row["domain"], row["indicator_id"]
        if key not in latest or row["year"] > latest[key]["year"]:
            latest[key] = row
    grouped = defaultdict(lambda: defaultdict(list))
    for (region_id, domain, _), row in latest.items():
        grouped[region_id][domain].append(row)
    domain_ids = [domain["id"] for domain in domains]
    output = []
    for region in regions:
        scores = {domain: (sum(item["normalized"] for item in grouped[region["id"]][domain]) / len(grouped[region["id"]][domain]) if grouped[region["id"]][domain] else None) for domain in domain_ids}
        complete = all(scores[domain] is not None for domain in domain_ids)
        nested = math.prod(max(scores[domain], 0.001) for domain in domain_ids) ** (1 / len(domain_ids)) if complete else None
        output.append({**region,"score":nested,"domains":scores,"observations":sum(len(rows) for rows in grouped[region["id"]].values()),"complete_domains":sum(value is not None for value in scores.values())})
    return output


def build() -> dict:
    project = load_json(ROOT / "project.json")
    domains = load_json(DATA / "domains.json")["domains"]
    sources = load_json(DATA / "SOURCES.json")["sources"]
    observations = load_observations({item["id"] for item in domains})
    regions = score_regions(regions_from_geometry(), domains, observations)
    return {"project":project,"domains":domains,"sources":sources,"regions":regions,"observations":observations,"summary":{"regions":len(regions),"scored_regions":sum(item["score"] is not None for item in regions),"observations":len(observations),"generated":date.today().isoformat()},"method":{"aggregation":"indicator arithmetic mean within domain; geometric mean across all nine domains","missingness":"no composite score until all nine domains are observed","carbon":"retained as an energy and industrial-system condition; never substituted for life-support resilience"}}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
