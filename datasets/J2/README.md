# J2: JSSP Basic with Disruptions Dataset

## Overview
This dataset extends J1 (JSSP Basic) with dynamic disruptions requiring reactive replanning capabilities.

## Problem Statement
Building on J1, this variant introduces dynamic disruptions requiring reactive replanning capabilities. Disruptions include machine breakdowns, power outages, supply chain delays, emergency shutdowns, and weather effects, each lasting different durations. The objective remains makespan minimization while adapting to real-time changes in system availability.

## Data Sources
- **Base Dataset**: J1 instances (DMU, TA, ABZ, SWV, YN)
- **Disruption Scenarios**: Generated disruption events with various types and durations

## Dataset Structure
```
J2/
├── disruptions/     # Disruption scenarios applied to J1 instances
├── processed/       # J1 instances with disruptions added
└── README.md        # This file
```

## Data Format
Each instance extends J1 format with:
- **Base JSSP Instance**: Original job-shop scheduling problem from J1
- **Disruptions**: List of disruption events with:
  - **Type**: machine_breakdown, power_outage, supply_delay, emergency_shutdown, weather_effect
  - **Machine/Resource**: Affected machine or resource ID
  - **Start Time**: When disruption occurs
  - **Duration**: How long disruption lasts
  - **Impact**: Severity and affected operations

## Disruption Types

1. **Machine Breakdown**: Machine becomes unavailable for a duration
2. **Power Outage**: Affects multiple machines in a region
3. **Supply Chain Delay**: Material/resource shortage affecting operations
4. **Emergency Shutdown**: Complete facility shutdown
5. **Weather Effect**: External factor affecting transportation/supply

## Generation Instructions

### Option 1: Generate Disruptions from J1 Instances
```bash
python generate_disruptions.py --base_dataset ../J1 --output disruptions/
```

### Option 2: Process Specific J1 Instance
```bash
python generate_disruptions.py --base_instance ../J1/DMU/cscmax_20_15_1.txt --output processed/
```

## Usage
See `examples/evaluation_example.py` for how to load and use these datasets.

