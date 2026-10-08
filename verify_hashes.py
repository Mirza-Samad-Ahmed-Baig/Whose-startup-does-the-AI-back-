"""Recompute SHA-256 hashes of the frozen files and compare with design_meta.json."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = {"analysis_plan_md": "analysis_plan.md",
         "trials": "trials.parquet",
         "campaigns": "campaigns.parquet"}

frozen = json.loads((HERE / "design_meta.json").read_text(encoding="utf-8"))["sha256"]
ok = True
for key, name in FILES.items():
    digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    match = digest == frozen[key]
    ok &= match
    print(f"{name:20s} {'MATCH' if match else 'MISMATCH'}  {digest}")
print("All hashes match." if ok else "At least one hash does not match.")
