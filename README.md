# AMP Challenge 2027 Submission

Method: seed-inpainted guided demasking (ESM language model + trained MIC/HC50
guide heads) with diversity-archive backfill; explicit multi-objective ranking
with Dirichlet weight-sensitivity robustness.

## AI-assistant disclosure
This submission was prepared with the assistance of an AI research assistant
(Biomni by Phylo) used for data curation, model training, generation, and
pipeline engineering, under human direction and review. All training data
sources and licenses are disclosed in METHOD.md.

## Reproduce
    uv run generate
Outputs: generate/library.fasta (50,000 sequences), generate/top.fasta (100).
