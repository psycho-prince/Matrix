#!/usr/bin/env python3
"""Verify the published CLDD benchmark archive (not the raw image task tensors)."""
from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path

archive = Path(sys.argv[1])
if not archive.is_file() or archive.stat().st_size == 0:
    raise SystemExit("CLDD archive missing or empty")

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
    names = [Path(e["name"]).name.lower() for e in entries]
    parquet = [n for n in names if n in {"cldd_a.parquet", "cldd_b.parquet"}]
    if not parquet:
        raise SystemExit(
            "No CLDD_A.parquet or CLDD_B.parquet found. "
            "This archive is the published benchmark dataset, not the raw Fashion-MNIST tensors."
        )
    report = {
        "archive": archive.name,
        "bytes": archive.stat().st_size,
        "sha256": sha.hexdigest(),
        "zip_crc": "passed",
        "benchmark_parquet_files": parquet,
        "entry_count": len(entries),
        "entries": entries,
        "note": "CLDD parquet contains recorded benchmark streams/results; it is not the raw rotated Fashion-MNIST training tensor archive."
    }
    Path("cldd_archive_manifest.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
