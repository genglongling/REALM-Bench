# J3: JSSP Large-scale, Sequential Planning Dataset

## Overview
This dataset contains large-scale JSSP instances scaled to industry-realistic dimensions with significantly more jobs, machines, and operations.

## Problem Statement
This variant scales J1 to industry-realistic dimensions with significantly more jobs, machines, and operations. The increased problem size tests algorithmic scalability and computational efficiency while maintaining the static environment assumption. The objective is makespan minimization under resource constraints typical of manufacturing environments.

## Data Sources
- **Scaled J1 Instances**: Large-scale versions of J1 benchmark instances
- **Industry Benchmarks**: Real-world manufacturing scheduling instances
- **Generated Large-scale**: Custom generated large-scale scenarios

## Dataset Structure
```
J3/
├── scaled/          # Scaled-up versions of J1 instances
├── industry/        # Industry-realistic large-scale instances
├── custom/          # Generated large-scale instances
└── README.md        # This file
```

## Data Format
Each instance contains:
- **Jobs**: 50-500 jobs (vs 5-50 in J1)
- **Machines**: 20-100 machines (vs 3-20 in J1)
- **Operations**: 100-5000 operations total
- **Processing Times**: Extended processing time matrices
- **Constraints**: Same as J1 but at larger scale

## Scale Characteristics

- **Small-scale (J1)**: 5-50 jobs, 3-20 machines
- **Medium-scale (J3)**: 50-200 jobs, 20-50 machines
- **Large-scale (J3)**: 200-500 jobs, 50-100 machines
- **Industry-scale (J3)**: 500+ jobs, 100+ machines

## Generation Instructions

### Option 1: Scale Existing J1 Instances
```bash
python scale_j1_instances.py --base_dataset ../J1 --scale_factor 10 --output scaled/
```

### Option 2: Generate Custom Large-scale Instances
```bash
python generate_large_scale_instances.py --num_jobs 200 --num_machines 50 --num_instances 100
```

## Usage
See `examples/evaluation_example.py` for how to load and use these datasets.

