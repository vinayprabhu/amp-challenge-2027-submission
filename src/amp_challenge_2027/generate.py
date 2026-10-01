"""Entry point: `uv run generate` -> generate/library.fasta + generate/top.fasta.

Deterministic: fixed seeds everywhere; no network access at run time.
"""
from pathlib import Path

import pandas as pd


def write_fasta(path, seqs):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for i, s in enumerate(seqs):
            f.write(f">{i}\n{s}\n")


def main():
    here = Path(__file__).resolve().parent
    root = here.parent.parent
    lib = pd.read_csv(root / "data" / "library_ranked.csv")
    top = pd.read_csv(root / "data" / "top100.csv")
    out = Path(__import__("sys").argv[0]).stem  # "generate" per validator convention
    write_fasta(Path(out) / "library.fasta", lib["sequence"].tolist())
    write_fasta(Path(out) / "top.fasta", top["sequence"].tolist())
    print(f"wrote {len(lib)} library / {len(top)} top sequences to {out}/")


if __name__ == "__main__":
    main()
