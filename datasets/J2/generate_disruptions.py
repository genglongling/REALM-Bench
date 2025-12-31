#!/usr/bin/env python3
"""
Generate disruption scenarios for J2 (JSSP Basic with Disruptions).
Adds disruptions to J1 instances.
"""
import json
import random
import argparse
from pathlib import Path
import os

DISRUPTION_TYPES = [
    "machine_breakdown",
    "power_outage",
    "supply_delay",
    "emergency_shutdown",
    "weather_effect"
]

def parse_j1_instance(j1_file):
    """Parse a J1 JSSP instance file."""
    # This is a simplified parser - actual JSSP format may vary
    instance_data = {
        "source_file": str(j1_file),
        "jobs": [],
        "machines": [],
        "processing_times": []
    }
    
    # Try to read as text file (standard JSSP format)
    try:
        with open(j1_file, 'r') as f:
            lines = f.readlines()
            # Parse header if available
            # This is a template - actual parsing depends on JSSP file format
            instance_data["raw_content"] = "".join(lines[:10])  # Store first 10 lines
    except Exception as e:
        print(f"Warning: Could not parse {j1_file}: {e}")
    
    return instance_data

def generate_disruption_scenario(base_instance, num_disruptions=1):
    """Generate disruption scenarios for a base J1 instance."""
    disruptions = []
    
    for i in range(num_disruptions):
        disruption_type = random.choice(DISRUPTION_TYPES)
        
        if disruption_type == "machine_breakdown":
            disruption = {
                "type": "machine_breakdown",
                "machine_id": random.randint(1, 10),  # Assuming 1-10 machines
                "start_time": random.randint(10, 100),
                "duration": random.randint(5, 30),
                "impact": "machine_unavailable"
            }
        elif disruption_type == "power_outage":
            disruption = {
                "type": "power_outage",
                "affected_machines": random.sample(range(1, 11), k=random.randint(2, 5)),
                "start_time": random.randint(20, 150),
                "duration": random.randint(10, 60),
                "impact": "multiple_machines_unavailable"
            }
        elif disruption_type == "supply_delay":
            disruption = {
                "type": "supply_delay",
                "resource": random.choice(["material_A", "material_B", "material_C"]),
                "start_time": random.randint(0, 50),
                "duration": random.randint(15, 45),
                "shortage_percentage": random.uniform(0.2, 0.5),
                "impact": "resource_shortage"
            }
        elif disruption_type == "emergency_shutdown":
            disruption = {
                "type": "emergency_shutdown",
                "facility": "main_facility",
                "start_time": random.randint(30, 120),
                "duration": random.randint(20, 90),
                "impact": "complete_shutdown"
            }
        else:  # weather_effect
            disruption = {
                "type": "weather_effect",
                "affected_operations": random.sample(range(1, 20), k=random.randint(3, 8)),
                "start_time": random.randint(15, 100),
                "duration": random.randint(30, 120),
                "severity": random.choice(["moderate", "severe"]),
                "impact": "transportation_delays"
            }
        
        disruptions.append(disruption)
    
    return disruptions

def create_j2_instance(j1_file, output_file, num_disruptions=1):
    """Create a J2 instance from a J1 instance with disruptions."""
    base_instance = parse_j1_instance(j1_file)
    disruptions = generate_disruption_scenario(base_instance, num_disruptions)
    
    j2_instance = {
        "instance_id": output_file.stem,
        "base_instance": base_instance,
        "disruptions": disruptions,
        "description": "JSSP Basic with Disruptions (J2)",
        "objective": "minimize_makespan_with_adaptation"
    }
    
    return j2_instance

def main():
    parser = argparse.ArgumentParser(description="Generate J2 disruption scenarios from J1 instances")
    parser.add_argument("--base_dataset", type=str, default="../J1", help="Base J1 dataset directory")
    parser.add_argument("--base_instance", type=str, help="Single J1 instance file to process")
    parser.add_argument("--output", type=str, default="disruptions", help="Output directory")
    parser.add_argument("--num_disruptions", type=int, default=1, help="Number of disruptions per instance")
    parser.add_argument("--disruption_types", nargs="+", default=DISRUPTION_TYPES, help="Types of disruptions to generate")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.base_instance:
        # Process single instance
        j1_file = Path(args.base_instance)
        if not j1_file.exists():
            print(f"Error: {j1_file} does not exist")
            return
        
        output_file = output_dir / f"{j1_file.stem}_disrupted.json"
        j2_instance = create_j2_instance(j1_file, output_file, args.num_disruptions)
        
        with open(output_file, 'w') as f:
            json.dump(j2_instance, f, indent=2)
        
        print(f"Created J2 instance: {output_file}")
    else:
        # Process all instances in base dataset
        base_dir = Path(args.base_dataset)
        
        # Find all J1 instance files
        j1_files = []
        for ext in ['*.txt', '*.json']:
            j1_files.extend(base_dir.rglob(ext))
        
        print(f"Found {len(j1_files)} J1 instances to process...")
        
        for j1_file in j1_files:
            # Skip if already processed
            if 'disrupted' in j1_file.name:
                continue
            
            output_file = output_dir / f"{j1_file.stem}_disrupted.json"
            j2_instance = create_j2_instance(j1_file, output_file, args.num_disruptions)
            
            with open(output_file, 'w') as f:
                json.dump(j2_instance, f, indent=2)
        
        print(f"Generated {len(j1_files)} J2 instances in {output_dir}/")

if __name__ == "__main__":
    main()

