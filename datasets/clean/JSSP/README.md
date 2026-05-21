# REALM-Bench JSSP (clean)

Four JSON files only — one per tier — with all instances in a **unified schema**.

## Files

| File | Tier | Instances | Description |
|------|------|-----------|-------------|
| `J1.json` | J1 | 109 | Static benchmarks (DMU, TA, ABZ, SWV, YN) |
| `J2.json` | J2 | 109 | J1 + dynamic disruptions |
| `J3.json` | J3 | 100 | Large-scale static (200×50) |
| `J4.json` | J4 | 100 | Large-scale + disruptions |

## Top-level structure (each file)

```json
{
  "tier": "J1",
  "format_version": "1.0",
  "description": "...",
  "objective": "minimize_makespan",
  "num_instances": 109,
  "instances": [ ... ]
}
```

## Instance object (inside `instances`)

```json
{
  "instance_id": "rcmax_50_20_9",
  "tier": "J1",
  "num_jobs": 50,
  "num_machines": 20,
  "jobs": [
    [
      {"operation": 1, "machine": 19, "processing_time": 64},
      {"operation": 2, "machine": 16, "processing_time": 34}
    ]
  ],
  "disruptions": [],
  "metadata": {
    "source_file": "DMU/rcmax_50_20_9.txt",
    "benchmark": "DMU",
    "objective": "minimize_makespan",
    "description": "JSSP Basic (Static)"
  }
}
```

- **machine** — 1-based machine ID  
- **disruptions** — empty for J1/J3; events for J2/J4  

## Load in Python

```python
import json

with open("datasets/clean/JSSP/J1.json") as f:
    data = json.load(f)

for inst in data["instances"]:
    print(inst["instance_id"], inst["num_jobs"], inst["num_machines"])
```

## Rebuild

```bash
cd datasets && python3 build_jssp_dataset.py
```

Writes only `clean/JSSP/J1.json` … `J4.json`. Re-copy this README after rebuild if needed.

## Hugging Face

Upload `datasets/clean/JSSP/` to **GloriaGeng/REALM-Bench** on the Hugging Face Hub.
