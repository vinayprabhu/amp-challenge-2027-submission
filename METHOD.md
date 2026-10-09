# Method Summary — AMP Challenge 2027 Submission

## Overview
Seed-inpainted guided demasking with a trained head ensemble, followed by explicit
multi-objective ranking with weight-sensitivity robustness.

## Pipeline
1. **Coverage audit** (pre-generation gate): 16/20 strain-level predictors assembled
   (floor: 10). Sources: DAMP APEX 1.0/1.1 oracles (12 strains) + Ampversity
   experimental MIC notes (4 additional strains: 2, 3, 8, 16).
2. **Training data**: DAMP frame (195,625 sequences, APEX oracle MIC columns);
   Ampversity 1.0 notes parsed for experimental per-strain MICs (104,569 records →
   32,335 median-aggregated training rows) and hemolysis (330 direct HC50 + 388
   interpolated + 2,660 right-censored); MarLys reference-eligible set (39,488) for
   conformity targets and the AMP discriminator positives.
3. **Guide heads**: MLPs on concat[h_i, e_a] over ESM-C 300M embeddings (hidden width
   960; `biohub/ESMC-300M`, Cambrian Open license). 26 heads: strain-level MIC (16 strains), species-
   level MIC (10 species), serovar (Typhimurium), HC50, AMP discriminator.
   CV: greedy single-linkage clustering at Levenshtein ratio 0.8, 3 folds.
   CV metrics: log10-MAE 0.37–0.58, Spearman rho 0.15–0.59 (p17-strain rho=-0.13 is
   the weakest head; its species head rho=0.31 backs it up).
4. **Generation**: seed-inpainted guided demasking (ProteinGuide/TAG-style first-order
   guidance: one LM forward per demasking step; guide = weighted ensemble of trained
   heads, HC50 negated to select low hemolysis). Seeds from a MAP-Elites diversity
   archive over the DAMP eligible non-reference set (519 seeds, bins over length ×
   charge × hydrophobic moment). Unguided high-mask demasking provides library backfill.
5. **Ranking** (explicit arithmetic in src/ranking.py):
   potency_A = -log10(MIC50_A/64); success = fraction of strains with MIC <= 16 uM;
   SW = HC50/MIC50_BROAD; R = weighted sum with w = {broad 1, gn 1, gp 1, mdr 1,
   sel 1, succ 1, conf 0.5}. Robustness: 200-sample Dirichlet sweep over the six main
   weights; top-100 favors worst-case rank. MIC clamped at 64 uM, HC50 at 128 uM
   (assay ceilings, right-censored).
6. **Assembly**: Levenshtein pre-screen vs the 39,448-sequence reference (ratio > 0.8
   demoted below rank 150); greedy diversity guard (<= 0.85 internal identity) within
   the top-100; rank depth 150 for replacements.

## Known limitations (documented, not hidden)
- AMP discriminator uses scrambled-sequence negatives: composition leakage; it acts as
  a composition prior, not a true AMP/non-AMP boundary.
- Proxy strains (7, 10, 13) inherit same-species head predictions; MDR status of the
  proxy strain may under-estimate resistance.
- Hemolysis labels are thin (586 fit rows); censored rows reserved for evaluation.
- Pilot-scale heads were trained on ESM-2 8M embeddings; the full-scale run uses
  ESM-C 300M (H_DIM=960) with the same recipe. ESM-2 650M is the documented fallback.

## AI-assistant disclosure
This submission was prepared with the assistance of an AI research assistant (Biomni
by Phylo) for data curation, label extraction, model training, generation, ranking,
and pipeline engineering, under human direction and review (V. Prabhu). All training
data sources and licenses are listed in DATA_DISCLOSURE.md.

## Post-hoc APEX-anchored re-rank (v3, 2026-10-01)
Independent multi-model screening (APEX 1.0/1.1 per-strain MIC, macrel + ai4amp AMP-probability
consensus) showed the guided-demasking heads were adversarially exploited: the original top-100
was dominated by Lys/Glu-rich heptad-repeat sequences. The top-100 was rebuilt deterministically:
1. composition gates (length 12-50, net charge >= +4, acidic fraction \<= 5%, hydrophobic fraction
30-75%, no homopolymers > 4);

2. predicted HC50 \>= 25 uM;

3. (macrel+ai4amp)/2 AMP consensus \>= 0.3;

 4. panel-mean APEX 1.0/1.1 MIC \<= 100 uM over the 18/20 panel strains with APEX coverage
(proxy mapping per panel.py);

5. Levenshtein reference screen vs antibacterial.fasta (cutoff 0.8);

6. Rank by panel-mean APEX MIC (tie-breaks: HC50 desc, internal R desc, sequence);

7. Greedy diversity selection (Levenshtein <= 0.85). Ranking uses the panel-strain mean, not the all-strain median, because the challenge assays the fixed 20-strain panel and medians over non-panel strains
mask weak strains.

Label provenance: panel oracle MIC columns are APEX-derived per-strain values
(damp_inference.py, kind=MIC_uM), so the re-rank re-aligns selection with the training-label
definition. All steps deterministic. 

AI assistance (Biomni by Phylo) under human direction.
