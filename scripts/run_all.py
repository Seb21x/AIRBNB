"""Execute every notebook in a fresh kernel; stop on the first execution error."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="*", help="Optional notebook filenames, otherwise all")
    args = parser.parse_args()
    os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]
    os.environ["MPLBACKEND"] = "Agg"
    paths = [ROOT / "notebooks" / name for name in args.notebooks] if args.notebooks else sorted((ROOT / "notebooks").glob("*.ipynb"))
    results = []
    for path in paths:
        print(f"Executing {path.name}", flush=True)
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        start = time.monotonic()
        client = NotebookClient(notebook, timeout=600, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT / "notebooks")}})
        client.execute()
        assert not any(o.output_type == "error" for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
        nbformat.write(notebook, path)
        results.append({"notebook": path.name, "status": "passed", "seconds": round(time.monotonic()-start, 2),
                        "code_cells": sum(c.cell_type == "code" for c in notebook.cells)})
        print(f"Passed {path.name} ({results[-1]['seconds']} s)", flush=True)
    output = ROOT / "tables" / ("execution.json" if not args.notebooks else "execution_selected.json")
    output.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
