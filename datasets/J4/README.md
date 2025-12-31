# J4: JSSP Large-scale with Disruptions Dataset

## Overview
This dataset combines J3's large-scale complexity with J2's dynamic disruptions, representing the most challenging JSSP variant.

## Problem Statement
The most challenging variant combines J3's large-scale complexity with J2's dynamic disruptions. This tests both computational scalability and real-time adaptation capabilities under realistic industrial conditions. Multiple simultaneous disruptions and cascading effects require sophisticated reactive planning while optimizing makespan across the extended operation horizon.

## Data Sources
- **Base Dataset**: J3 large-scale instances
- **Disruption Scenarios**: Multiple simultaneous disruptions (from J2)
- **Cascading Effects**: Complex disruption interactions

## Dataset Structure
```
J4/
├── disrupted_large/  # J3 instances with disruptions added
├── cascading/        # Instances with cascading disruption effects
├── custom/           # Generated large-scale disruption scenarios
└── README.md         # This file
```

## Data Format
Each instance combines J3 and J2 formats:
- **Large-scale JSSP**: 50-500 jobs, 20-100 machines (from J3)
- **Multiple Disruptions**: 2-5 simultaneous disruptions (from J2)
- **Cascading Effects**: Disruptions that trigger other disruptions
- **Extended Horizon**: Longer operation horizon requiring adaptive planning

## Disruption Characteristics

- **Frequency**: Higher disruption rate than J2
- **Simultaneity**: Multiple disruptions occurring at once
- **Cascading**: Disruptions triggering secondary effects
- **Scale Impact**: Disruptions affecting multiple machines/jobs simultaneously

## Generation Instructions

### Option 1: Add Disruptions to J3 Instances
```bash
python generate_large_scale_disruptions.py --base_dataset ../J3/scaled --output disrupted_large/
```

### Option 2: Generate Custom Large-scale with Disruptions
```bash
python generate_custom_j4.py --num_jobs 200 --num_machines 50 --num_disruptions 3 --num_instances 100
```

## Usage
See `examples/evaluation_example.py` for how to load and use these datasets.

