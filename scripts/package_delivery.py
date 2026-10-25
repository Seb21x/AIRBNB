"""Package all project assets, code, data and report into deliverables/airbnb_submission.zip."""
import hashlib
import json
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
ZIP_PATH = DELIVERABLES / "airbnb_submission.zip"

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "scratch",
    "deliverables",
    "airbnb_analysis.egg-info",
    "__pycache__",
    ".ipynb_checkpoints",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".DS_Store",
    ".aux",
    ".out",
    ".fls",
    ".fdb_latexmk",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def should_include(rel_path: Path) -> bool:
    parts = rel_path.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return False
    if rel_path.name.startswith(".DS_Store"):
        return False
    if rel_path.suffix in EXCLUDE_EXTS:
        return False
    if rel_path.name == "report.log":
        return False
    return True


def package():
    DELIVERABLES.mkdir(exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    files_to_pack = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Filter directories in place to prevent descending into excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            full_path = Path(dirpath) / f
            rel_path = full_path.relative_to(ROOT)
            if should_include(rel_path):
                files_to_pack.append(rel_path)

    files_to_pack.sort()

    print(f"Creating archive {ZIP_PATH.name} with {len(files_to_pack)} files...")
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in files_to_pack:
            full = ROOT / rel
            zf.write(full, arcname=str(rel))

    # Verify ZIP integrity
    print("Verifying ZIP integrity...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        bad_file = zf.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupt file in ZIP: {bad_file}")
        infolist = zf.infolist()
        total_uncompressed = sum(info.file_size for info in infolist)
        total_compressed = sum(info.compress_size for info in infolist)

    zip_hash = sha256_file(ZIP_PATH)
    pdf_path = ROOT / "report" / "report.pdf"
    pdf_hash = sha256_file(pdf_path) if pdf_path.exists() else None

    manifest = {
        "archive_name": ZIP_PATH.name,
        "archive_size_bytes": ZIP_PATH.stat().st_size,
        "archive_sha256": zip_hash,
        "files_count": len(files_to_pack),
        "total_uncompressed_bytes": total_uncompressed,
        "total_compressed_bytes": total_compressed,
        "pdf_report": {
            "path": "report/report.pdf",
            "size_bytes": pdf_path.stat().st_size if pdf_path.exists() else None,
            "sha256": pdf_hash,
        },
    }

    manifest_path = DELIVERABLES / "delivery_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    print("=" * 60)
    print("PACKAGING COMPLETE")
    print(f"Archive:       {ZIP_PATH}")
    print(f"Size:          {ZIP_PATH.stat().st_size / (1024*1024):.2f} MB")
    print(f"Files:         {len(files_to_pack)}")
    print(f"Archive SHA256:{zip_hash}")
    print(f"PDF SHA256:    {pdf_hash}")
    print(f"Manifest:      {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    package()
