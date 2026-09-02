# Global Life-Support Atlas

The Global Life-Support Atlas is a private-development mapping project that tests whether nested life-support resilience predicts harm and adaptation better than carbon metrics alone. It models regions through nine distinct domains: water, food, heat, soil, energy, transport, health, ecological integrity, and institutional capacity.

Carbon remains inside the model as an energy and industrial-system condition. Life encloses carbon.

## Development status

This repository is private before launch. `project.json` is the launch gate: public participation requires both a configured `launch_date` and `participation_enabled: true`. No public submission workflow should be enabled before both conditions are met.

The initial atlas intentionally contains no scored observations. It maps regions and validates the full data contract without presenting placeholder values as findings. A region receives a nested score only after all nine domains contain accepted evidence.

## Build

Python 3.10 or newer is sufficient; the static atlas has no Python package dependencies.

```bash
python3 -m src.generate_web_atlas
python3 -m unittest discover -s tests
python3 -m http.server 8770
```

Open `http://localhost:8770/outputs/web/`.

## Observation contract

Add source-bearing observations to `data/observations.csv`. Each row requires region and ISO identifiers, year, one of the nine domains, indicator ID, value and unit, resilience direction, explicit normalization bounds, source ID and version, source URL, retrieval date, provenance status, and notes.

Indicators average within each domain. Complete domain values combine through a geometric mean. Missing data are never converted to zero, carried forward implicitly, or filled for presentation. Missing any domain suppresses the composite score.

Candidate sources and their roles are in `data/SOURCES.json` and the generated Data page. Dataset licenses remain upstream; project software and original documentation are MIT licensed.
