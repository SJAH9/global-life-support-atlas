#!/usr/bin/env python3
"""Build the static web atlas."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.build_atlas import DATA, OUTPUT, ROOT, WEB, build


def generate() -> Path:
    payload = build()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source in WEB.iterdir():
        if source.is_file():
            shutil.copy2(source, OUTPUT / source.name)
    shutil.copy2(DATA / "raw" / "world.geojson", OUTPUT / "world.geojson")
    (OUTPUT / "data.js").write_text("window.LIFE_SUPPORT_DATA=" + json.dumps(payload, separators=(",", ":")) + ";\n", encoding="utf-8")
    (ROOT / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=outputs/web/"><a href="outputs/web/">Open the Global Life-Support Atlas</a>\n', encoding="utf-8")
    return OUTPUT / "index.html"


if __name__ == "__main__":
    print(generate())
