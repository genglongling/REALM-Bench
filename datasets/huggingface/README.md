---
license: cc-by-4.0
language:
  - en
tags:
  - job-shop-scheduling
  - operations-research
  - scheduling
  - combinatorial-optimization
  - benchmark
  - multi-agent
  - planning
task_categories:
  - other
size_categories:
  - 10M<n<100M
pretty_name: REALM-Bench JSSP
dataset_info:
  features:
    - name: tier
      dtype: string
    - name: instances
      dtype: string
  config_name: default
  splits:
    - name: J1
      num_examples: 109
    - name: J2
      num_examples: 109
    - name: J3
      num_examples: 100
    - name: J4
      num_examples: 100
---

# REALM-Bench — Job Shop Scheduling (JSSP) Dataset

This Hugging Face dataset hosts the **clean JSSP benchmark** from [REALM-Bench](https://github.com/genglongling/REALM-Bench): a real-world planning benchmark for LLMs and multi-agent systems ([paper](https://arxiv.org/abs/2502.18836)).

All instances use a **single unified JSON schema**, organized into four tiers (**J1–J4**) as four files under `JSSP/`.

## Dataset files

| File | Tier | Instances | Description |
|------|------|-----------|-------------|
| [`JSSP/J1.json`](JSSP/J1.json) | J1 | 109 | Static benchmarks (DMU, TA, ABZ, SWV, YN) |
| [`JSSP/J2.json`](JSSP/J2.json) | J2 | 109 | J1 instances + dynamic disruptions |
| [`JSSP/J3.json`](JSSP/J3.json) | J3 | 100 | Large-scale static (200 jobs × 50 machines) |
| [`JSSP/J4.json`](JSSP/J4.json) | J4 | 100 | Large-scale + multiple disruptions |

**Total: 418 job-shop scheduling instances**

## Problem tiers

- **J1** — Classic static JSSP from standard OR benchmarks (minimize makespan).
- **J2** — Same problems as J1 with disruptions (machine breakdown, power outage, supply delay, etc.); tests reactive replanning.
- **J3** — Industry-scale static instances (larger job and machine counts).
- **J4** — J3 scale with multiple simultaneous disruptions; highest difficulty tier.

## Data format

Each `J*.json` file has this structure:

```json
{
  "tier": "J1",
  "format_version": "1.0",
  "description": "Static JSSP benchmarks (DMU, TA, ABZ, SWV, YN)",
  "objective": "minimize_makespan",
  "num_instances": 109,
  "instances": [
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
        "objective": "minimize_makespan"
      }
    }
  ]
}
```

- **jobs** — Ordered operations per job; **machine** is 1-based; **processing_time** is a positive integer.
- **disruptions** — Empty for J1/J3; list of events for J2/J4.

See [`JSSP/README.md`](JSSP/README.md) for additional field notes.

## Usage

### Download with `huggingface_hub`

```python
from huggingface_hub import hf_hub_download
import json

path = hf_hub_download(
    repo_id="GloriaGeng/REALM-Bench",
    filename="JSSP/J1.json",
    repo_type="dataset",
)
with open(path) as f:
    data = json.load(f)

print(f"Tier {data['tier']}: {data['num_instances']} instances")
for inst in data["instances"][:3]:
    print(inst["instance_id"], inst["num_jobs"], inst["num_machines"])
```

### Load all tiers

```python
from huggingface_hub import hf_hub_download
import json

for tier in ("J1", "J2", "J3", "J4"):
    path = hf_hub_download("GloriaGeng/REALM-Bench", f"JSSP/{tier}.json", repo_type="dataset")
    with open(path) as f:
        d = json.load(f)
    print(tier, d["num_instances"], "instances,", d["objective"])
```

### Clone the dataset

```bash
git clone https://huggingface.co/datasets/GloriaGeng/REALM-Bench
```

## Benchmark families (J1 / J2)

| Family | Typical size | Source |
|--------|----------------|--------|
| DMU | 20×15 – 50×20 | Demirkol, Mehta, Uzsoy |
| TA | 15×15 – 100×20 | Taillard |
| ABZ | 20×15 | Adams, Balas, Zawack |
| SWV | 20×10 – 50×10 | Storer, Vaccari, Van de Velde |
| YN | 20×20 | Yamada, Nakano |

## Citation

If you use this dataset, please cite REALM-Bench:

```bibtex
@misc{geng2025realmbenchbenchmarkevaluatingmultiagent,
  title={REALM-Bench: A Benchmark for Evaluating Multi-Agent Systems on Real-world, Dynamic Planning and Scheduling Tasks},
  author={Longling Geng and Edward Y. Chang},
  year={2025},
  eprint={2502.18836},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2502.18836},
}
```

## Links

- **GitHub:** https://github.com/genglongling/REALM-Bench  
- **Paper:** https://arxiv.org/abs/2502.18836  
- **JSSP subfolder docs:** [JSSP/README.md](JSSP/README.md)

## License

| Component | License |
|-----------|---------|
| **Code** (REALM-Bench repository, evaluation framework) | [MIT](https://opensource.org/licenses/MIT) |
| **Dataset** (this JSSP release on Hugging Face) | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) |

Benchmark instance data may additionally follow the licensing of original sources (OR-Library, Taillard, etc.) where applicable.
