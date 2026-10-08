# Pre-specified analysis plan: "Whose startup does the AI back?"

This deposit contains the analysis plan that was frozen before data collection
for the study *Whose startup does the AI back? An algorithm audit of reputation
and demographic signals in LLM-assisted crowdfunding*, together with the frozen
design and the evidence that dates them.

## What this deposit is, and what it is not

- The plan (`analysis_plan.md`), the randomized design (`trials.parquet`,
  `campaigns.parquet`, seed 20260709), and their SHA-256 hashes
  (`design_meta.json`) were frozen in the authors' version-controlled repository
  on **9 July 2026 at 17:09 UTC** (commit `ae9cf35`, tag `prereg-v1`).
- The first model call (pilot) was made on **10 July 2026 at 08:25 UTC**, 15
  hours later; the first confirmatory call at 08:41 UTC; the last call on
  14 July 2026.
- The plan states that it would be deposited on OSF before data collection.
  **That deposit was not made.** This deposit was assembled in October 2026,
  during peer review; it was supplied to the journal as a supplementary file and
  is made public on publication. The timestamps above are self-recorded (version
  control and API logs), not certified by a registry. The study is therefore
  described as following a *pre-specified analysis plan*, not as *preregistered*.
- `provenance_and_deviations.pdf` lists every deviation from the plan.

## Files

| File | Content |
|---|---|
| `analysis_plan.md` | The plan, byte-identical to the frozen version |
| `design_meta.json` | Design metadata and the SHA-256 hashes of the plan and design files, as frozen |
| `trials.parquet`, `campaigns.parquet` | The frozen randomized design (3,024 main-arm trials x 5 campaign cards) |
| `version_history_to_prereg-v1.txt` | Commit hashes, dates and messages up to the freeze (author fields omitted for blind review) |
| `commits_touching_analysis_plan.txt` | The commits that created or edited the plan (none after the freeze) |
| `provenance_and_deviations.pdf` | Provenance record, deviation table, and the plan reproduced verbatim |
| `verify_hashes.py` | Recomputes the SHA-256 hashes and compares them with `design_meta.json` |

## Verify

```
python verify_hashes.py
```

Expected: all three hashes match.

Analysis code and raw model outputs are added on publication.
