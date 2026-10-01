# Training-Data Disclosure — AMP Challenge 2027 Submission

| Source | Role | License / terms |
|---|---|---|
| DAMP (github.com/vinayprabhu/DAMP), df_damp_195625x57.tsv | APEX 1.0/1.1 predicted MIC oracle columns for 12 panel strains; seed mining | Author's own dataset (V. Prabhu) |
| AMPversity 1.0 (Zenodo 21968308): df_ampversity, biomni, claude TSVs | Experimental per-strain MIC labels (notes parsing), hemolysis dose-response | CC-BY 4.0 (author's own dataset) |
| MarLys / MLAMP_db.json | Reference-eligible set (39,488), descriptor-conformity targets, AMP discriminator positives | CC-0 |
| Competition starter kit data/antibacterial.fasta (39,448 seqs) | Novelty screen reference (exact-match ban + Levenshtein 0.8) | MarLys-derived, per competition terms |
| DBAASP | Referenced for MIC label provenance within Ampversity notes | CC-BY 4.0 |

No other sequence or label data were used. No test-panel strains were queried beyond
the sources above. Label transformations: ug/mL → uM via residue-sum molecular weight;
median aggregation per (sequence, strain, level); right-censoring at 64 uM (MIC) and
128 uM (HC50); nothing imputed.
