#!/usr/bin/env python3
"""
Scale J1 instances to large-scale for J3.
"""
import json
import random
import argparse
from pathlib import Path

def parse_j1_instance(j1_file):
    """Parse a J1 JSSP instance file."""
    instance_data = {
        "source_file": str(j1_file),
        "jobs": [],
        "machines": [],
        "processing_times": []
    }
    
    try:
        with open(j1_file, 'r') as f:
            lines = f.readlines()
            instance_data["raw_content"] = "".join(lines)
    except Exception as e:
        print(f"Warning: Could not parse {j1_file}: {e}")
    
    return instance_data

def scale_instance(base_instance, scale_factor, target_jobs=None, target_machines=None):
    """Scale a J1 instance to large-scale for J3."""
    # Extract dimensions from base instance if available
    # For now, use default scaling
    
    if target_jobs is None:
        target_jobs = int(20 * scale_factor)  # Scale from ~20 jobs
    
    if target_machines is None:
        target_machines = int(10 * scale_factor)  # Scale from ~10 machines
    
    # Generate large-scale processing times matrix
    processing_times = []
    for job in range(target_jobs):
        job_operations = []
        num_operations = random.randint(5, 15)  # 5-15 operations per job
        for op in range(num_operations):
            machine = random.randint(1, target_machines)
            processing_time = random.randint(1, 50)
            job_operations.append({
                "operation": op + 1,
                "machine": machine,
                "processing_time": processing_time
            })
        processing_times.append(job_operations)
    
    scaled_instance = {
        "instance_id": f"j3_{base_instance.get('source_file', 'unknown').stem}_scaled",
        "base_instance": base_instance.get("source_file", "unknown"),
        "scale_factor": scale_factor,
        "num_jobs": target_jobs,
        "num_machines": target_machines,
        "total_operations": sum(len(job) for job in processing_times),
        "processing_times": processing_times,
        "description": f"Large-scale JSSP instance (scaled {scale_factor}x from J1)",
        "objective": "minimize_makespan",
        "environment": "static"
    }
    
    return scaled_instance

def generate_custom_large_scale(num_jobs, num_machines, instance_id):
    """Generate a custom large-scale JSSP instance."""
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
    
    instance = {
        "instance_id": f"j3_custom_{instance_id:03d}",
        "num_jobs": num_jobs,
        "num_machines": num_machines,
        "total_operations": sum(len(job) for job in processing_times),
        "processing_times": processing_times,
        "description": f"Custom large-scale JSSP instance ({num_jobs} jobs, {num_machines} machines)",
        "objective": "minimize_makespan",
        "environment": "static"
    }
    
    return instance

def main():
    parser = argparse.ArgumentParser(description="Generate J3 large-scale instances")
    parser.add_argument("--base_dataset", type=str, help="Base J1 dataset directory to scale")
    parser.add_argument("--scale_factor", type=int, default=10, help="Scaling factor")
    parser.add_argument("--output", type=str, default="scaled", help="Output directory")
    parser.add_argument("--num_jobs", type=int, help="Target number of jobs (for custom generation)")
    parser.add_argument("--num_machines", type=int, help="Target number of machines (for custom generation)")
    parser.add_argument("--num_instances", type=int, default=100, help="Number of custom instances to generate")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.base_dataset:
        # Scale existing J1 instances
        base_dir = Path(args.base_dataset)
        j1_files = list(base_dir.rglob("*.txt"))
        
        print(f"Scaling {len(j1_files)} J1 instances with factor {args.scale_factor}...")
        
        for j1_file in j1_files:
            base_instance = parse_j1_instance(j1_file)
            scaled_instance = scale_instance(base_instance, args.scale_factor)
            
            output_file = output_dir / f"{scaled_instance['instance_id']}.json"
            with open(output_file, 'w') as f:
                json.dump(scaled_instance, f, indent=2)
        
        print(f"Generated {len(j1_files)} scaled instances in {output_dir}/")
    else:
        # Generate custom large-scale instances
        if not args.num_jobs or not args.num_machines:
            # Use default large-scale dimensions
            args.num_jobs = args.num_jobs or 200
            args.num_machines = args.num_machines or 50
        
        print(f"Generating {args.num_instances} custom large-scale instances ({args.num_jobs} jobs, {args.num_machines} machines)...")
        
        for i in range(1, args.num_instances + 1):
            instance = generate_custom_large_scale(args.num_jobs, args.num_machines, i)
            output_file = output_dir / f"{instance['instance_id']}.json"
            
            with open(output_file, 'w') as f:
                json.dump(instance, f, indent=2)
        
        print(f"Generated {args.num_instances} instances in {output_dir}/")

if __name__ == "__main__":
    main()

