#!/usr/bin/env python3
"""
Generate large-scale JSSP instances with disruptions for J4.
Combines J3's scale with J2's disruptions.
"""
import json
import random
import argparse
from pathlib import Path

DISRUPTION_TYPES = [
    "machine_breakdown",
    "power_outage",
    "supply_delay",
    "emergency_shutdown",
    "weather_effect",
    "cascading_failure"
]

def load_j3_instance(j3_file):
    """Load a J3 large-scale instance."""
    try:
        with open(j3_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {j3_file}: {e}")
        return None

def generate_multiple_disruptions(base_instance, num_disruptions=3):
    """Generate multiple disruptions for a large-scale instance."""
    disruptions = []
    num_machines = base_instance.get("num_machines", 50)
    num_jobs = base_instance.get("num_jobs", 200)
    
    for i in range(num_disruptions):
        disruption_type = random.choice(DISRUPTION_TYPES)
        
        if disruption_type == "machine_breakdown":
            disruption = {
                "type": "machine_breakdown",
                "machine_id": random.randint(1, num_machines),
                "start_time": random.randint(50, 500),
                "duration": random.randint(10, 60),
                "impact": "machine_unavailable",
                "affected_jobs": random.sample(range(1, num_jobs + 1), k=random.randint(5, 20))
            }
        elif disruption_type == "power_outage":
            num_affected = random.randint(5, min(20, num_machines))
            disruption = {
                "type": "power_outage",
                "affected_machines": random.sample(range(1, num_machines + 1), k=num_affected),
                "start_time": random.randint(100, 800),
                "duration": random.randint(30, 120),
                "impact": "multiple_machines_unavailable",
                "affected_jobs": random.sample(range(1, num_jobs + 1), k=random.randint(20, 50))
            }
        elif disruption_type == "supply_delay":
            disruption = {
                "type": "supply_delay",
                "resource": random.choice(["material_A", "material_B", "material_C", "material_D"]),
                "start_time": random.randint(0, 200),
                "duration": random.randint(30, 90),
                "shortage_percentage": random.uniform(0.3, 0.6),
                "impact": "resource_shortage",
                "affected_operations": random.sample(range(1, 100), k=random.randint(10, 30))
            }
        elif disruption_type == "emergency_shutdown":
            disruption = {
                "type": "emergency_shutdown",
                "facility": random.choice(["facility_A", "facility_B", "main_facility"]),
                "start_time": random.randint(150, 600),
                "duration": random.randint(60, 180),
                "impact": "complete_shutdown",
                "affected_jobs": random.sample(range(1, num_jobs + 1), k=random.randint(30, 100))
            }
        elif disruption_type == "cascading_failure":
            # Cascading failure: one disruption triggers others
            primary_machine = random.randint(1, num_machines)
            disruption = {
                "type": "cascading_failure",
                "primary_machine": primary_machine,
                "start_time": random.randint(200, 700),
                "duration": random.randint(40, 100),
                "cascading_machines": random.sample(
                    [m for m in range(1, num_machines + 1) if m != primary_machine],
                    k=random.randint(2, 5)
                ),
                "impact": "cascading_system_failure",
                "affected_jobs": random.sample(range(1, num_jobs + 1), k=random.randint(40, 80))
            }
        else:  # weather_effect
            disruption = {
                "type": "weather_effect",
                "affected_operations": random.sample(range(1, 200), k=random.randint(20, 60)),
                "start_time": random.randint(100, 600),
                "duration": random.randint(60, 180),
                "severity": random.choice(["moderate", "severe", "extreme"]),
                "impact": "transportation_delays_and_supply_chain_disruption"
            }
        
        disruptions.append(disruption)
    
    return disruptions

def create_j4_instance(j3_instance, num_disruptions=3):
    """Create a J4 instance from a J3 instance with disruptions."""
    disruptions = generate_multiple_disruptions(j3_instance, num_disruptions)
    
    j4_instance = {
        "instance_id": f"j4_{j3_instance.get('instance_id', 'unknown')}_disrupted",
        "base_instance": j3_instance.get("instance_id", "unknown"),
        "num_jobs": j3_instance.get("num_jobs", 200),
        "num_machines": j3_instance.get("num_machines", 50),
        "total_operations": j3_instance.get("total_operations", 1000),
        "processing_times": j3_instance.get("processing_times", []),
        "disruptions": disruptions,
        "num_disruptions": len(disruptions),
        "description": "Large-scale JSSP with multiple disruptions (J4)",
        "objective": "minimize_makespan_with_adaptation",
        "environment": "dynamic",
        "complexity": "high"
    }
    
    return j4_instance

def generate_custom_j4(num_jobs, num_machines, num_disruptions, instance_id):
    """Generate a custom J4 instance from scratch."""
    # Generate processing times (simplified)
    processing_times = []
    for job in range(num_jobs):
        job_operations = []
        num_operations = random.randint(5, 20)
        for op in range(num_operations):
            machine = random.randint(1, num_machines)
            processing_time = random.randint(1, 100)
            job_operations.append({
                "operation": op + 1,
                "machine": machine,
                "processing_time": processing_time
            })
        processing_times.append(job_operations)
    
    base_instance = {
        "instance_id": f"j4_custom_base_{instance_id:03d}",
        "num_jobs": num_jobs,
        "num_machines": num_machines,
        "total_operations": sum(len(job) for job in processing_times),
        "processing_times": processing_times
    }
    
    j4_instance = create_j4_instance(base_instance, num_disruptions)
    j4_instance["instance_id"] = f"j4_custom_{instance_id:03d}"
    
    return j4_instance

def main():
    parser = argparse.ArgumentParser(description="Generate J4 large-scale instances with disruptions")
    parser.add_argument("--base_dataset", type=str, help="Base J3 dataset directory")
    parser.add_argument("--output", type=str, default="disrupted_large", help="Output directory")
    parser.add_argument("--num_disruptions", type=int, default=3, help="Number of disruptions per instance")
    parser.add_argument("--num_jobs", type=int, help="Number of jobs (for custom generation)")
    parser.add_argument("--num_machines", type=int, help="Number of machines (for custom generation)")
    parser.add_argument("--num_instances", type=int, default=100, help="Number of custom instances to generate")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.base_dataset:
        # Process J3 instances
        base_dir = Path(args.base_dataset)
        j3_files = list(base_dir.rglob("*.json"))
        
        print(f"Processing {len(j3_files)} J3 instances with {args.num_disruptions} disruptions each...")
        
        for j3_file in j3_files:
            j3_instance = load_j3_instance(j3_file)
            if j3_instance:
                j4_instance = create_j4_instance(j3_instance, args.num_disruptions)
                output_file = output_dir / f"{j4_instance['instance_id']}.json"
                
                with open(output_file, 'w') as f:
                    json.dump(j4_instance, f, indent=2)
        
        print(f"Generated {len(j3_files)} J4 instances in {output_dir}/")
    else:
        # Generate custom instances
        if not args.num_jobs or not args.num_machines:
            args.num_jobs = args.num_jobs or 200
            args.num_machines = args.num_machines or 50
        
        print(f"Generating {args.num_instances} custom J4 instances ({args.num_jobs} jobs, {args.num_machines} machines, {args.num_disruptions} disruptions)...")
        
        for i in range(1, args.num_instances + 1):
            instance = generate_custom_j4(args.num_jobs, args.num_machines, args.num_disruptions, i)
            output_file = output_dir / f"{instance['instance_id']}.json"
            
            with open(output_file, 'w') as f:
                json.dump(instance, f, indent=2)
        
        print(f"Generated {args.num_instances} instances in {output_dir}/")

if __name__ == "__main__":
    main()

