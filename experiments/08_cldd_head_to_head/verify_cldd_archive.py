#!/usr/bin/env python3
"""Verify the upstream CLDD dataset archive without training any models."""
from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path

archive = Path(sys.argv[1])
if not archive.is_file() or archive.stat().st_size == 0:
    raise SystemExit("Dataset archive missing or empty")

sha = hashlib.sha256()
with archive.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
        sha.update(chunk)

with zipfile.ZipFile(archive) as zf:
    bad = zf.testzip()
    if bad:
        raise SystemExit(f"ZIP CRC failure: {bad}")
    entries = [
        {"name": i.filename, "size": i.file_size, "compressed_size": i.compress_size}
        for i in zf.infolist() if not i.is_dir()
    ]
    names = [e["name"].lower() for e in entries]
    fashion = [n for n in names if "rotated_fashion_mnist_data.pt" in n]
    if not fashion:
        raise SystemExit("Expected rotated_fashion_mnist_data.pt not found in archive")
    report = {
        "archive": archive.name,
        "bytes": archive.stat().st_size,
        "sha256": sha.hexdigest(),
        "zip_crc": "passed",
        "fashion_mnist_tensor_archive": fashion,
        "entry_count": len(entries),
        "entries": entries,
    }
    Path("cldd_archive_manifest.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
