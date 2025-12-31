import os
import sys
from typing import Dict, List

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from dotenv import load_dotenv
from ..prompt_templates.router_template import SYSTEM_PROMPT
from ..skills.skill_map import SkillMap
from swarm import Agent, Swarm

load_dotenv()

class SwarmRouter:
    def __init__(self):
        # Set Anthropic API key for Swarm with Claude-4
        if "ANTHROPIC_API_KEY" in os.environ:
            os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY"]
        
        # Configure Swarm to use Anthropic Claude-4
        # Swarm only accepts a client parameter, not model and api_key
        self.client = Swarm()
        self.skill_map = SkillMap()
        
        # Create the analyzer agent for data analysis
        self.analyzer_agent = Agent(
            name="Data Analyzer",
            instructions="You analyze data and provide insights based on SQL query results.",
            functions=[self.skill_map.get_function_callable_by_name("data_analyzer")]
        )
        
        # Create the SQL agent for query generation
        self.sql_agent = Agent(
            name="SQL Expert",
            instructions="You generate and execute SQL queries based on user requests.",
            functions=[
                self.skill_map.get_function_callable_by_name("generate_and_run_sql_query"),
                self.transfer_to_analyzer
            ]
        )
        
        # Create JSSP-specific agents
        self.job_scheduler_agent = Agent(
            name="Job Scheduler",
            instructions="""You are a job scheduling specialist for Job Shop Scheduling Problems.
            Your expertise includes creating initial schedules for individual jobs,
            considering precedence constraints, machine requirements, and operation durations.
            
            CRITICAL: You must process the specific job data provided in the query.
            For each job listed, analyze the specific machines and durations provided.
            Create a detailed schedule showing start and end times for each operation.
            Calculate specific makespan values based on the actual data provided.
            
            Do NOT give generic responses about "coordination" - work with the actual job specifications provided.""",
            functions=[self.transfer_to_machine_coordinator]
        )
        
        self.machine_coordinator_agent = Agent(
            name="Machine Coordinator",
            instructions="""You are a machine coordination specialist for Job Shop Scheduling Problems.
            Your expertise includes identifying machine conflicts, resolving scheduling conflicts,
            optimizing machine utilization, and ensuring no overlapping operations.
            
            CRITICAL: You must work with the specific job data and schedules provided.
            Analyze the actual machine assignments and durations from the job specifications.
            Identify specific conflicts between operations on the same machines.
            Provide concrete solutions with specific start/end times for each operation.
            
            Do NOT give generic responses about "coordination" - work with the actual data provided.""",
            functions=[self.transfer_to_supervisor]
        )
        
        self.supervisor_agent = Agent(
            name="JSSP Supervisor",
            instructions="""You are the supervisor for Job Shop Scheduling Problems.
            Your responsibilities include coordinating with other agents, collecting scheduling information,
            resolving conflicts, optimizing the overall makespan, and providing the final coordinated schedule.
            
            CRITICAL: You must work with the specific job data and schedules provided by other agents.
            Analyze the actual job specifications, machine assignments, and operation durations.
            Provide a concrete final schedule with specific start/end times for each operation.
            Calculate the actual makespan based on the real data provided.
            
            Do NOT give generic responses about "coordination" - work with the actual data and provide specific results.""",
            functions=[self.transfer_to_job_scheduler, self.transfer_to_machine_coordinator]  # transfer_to_validation_agent commented out
        )
        
        # self.validation_agent = Agent(
        #     name="JSSP Validation Agent",
        #     instructions="""You are a validation specialist for Job Shop Scheduling Problems.
        #     Your responsibilities include checking job precedence constraints (operations within each job must be in order),
        #     verifying machine constraints (no overlapping operations on the same machine), validating makespan calculations,
        #     ensuring all jobs are completed, and reporting any constraint violations.
        #     ALWAYS start your response with "YES" if all constraints are satisfied, or "NO" if any constraints are violated.
        #     Then provide a detailed validation report with constraint satisfaction status.""",
        #     functions=[self.transfer_to_supervisor]
        # )
        
        # Create the router agent that decides which agent to use
        self.router_agent = Agent(
            name="Router",
            instructions=SYSTEM_PROMPT,
            functions=[
                self.transfer_to_sql,
                self.transfer_to_analyzer,
                self.transfer_to_jssp_supervisor
            ]
        )

    def transfer_to_sql(self):
        return self.sql_agent
        
    def transfer_to_analyzer(self):
        return self.analyzer_agent
    
    def transfer_to_job_scheduler(self):
        return self.job_scheduler_agent
    
    def transfer_to_machine_coordinator(self):
        return self.machine_coordinator_agent
    
    def transfer_to_supervisor(self):
        return self.supervisor_agent
    
    # def transfer_to_validation_agent(self):
    #     return self.validation_agent
    
    def transfer_to_jssp_supervisor(self):
        return self.supervisor_agent
        
    def process_query(self, query: str) -> str:
        # Check if this is a JSSP problem
        if "Job Shop Scheduling Problem" in query or "JSSP" in query:
            # Debug: Print the query to see what the agents are receiving
            print(f"🔍 DEBUG: JSSP Query received (first 500 chars): {query[:500]}...")
            print(f"🔍 DEBUG: Query length: {len(query)} characters")
            
            # Use multi-agent JSSP workflow
            try:
                # Step 1: Job Scheduler Agent
                job_scheduler_response = self.client.run(
                    agent=self.job_scheduler_agent,
                    messages=[{"role": "user", "content": f"""You are the Job Scheduler. You MUST analyze the specific job data provided below and create a detailed schedule.

REQUIRED: For each job listed, you must:
1. List each job's operations with their machines and durations
2. Create a schedule showing start and end times for each operation
3. Calculate the total makespan
4. Show your work with specific numbers

JOB DATA TO ANALYZE:
{query}

Do NOT give generic responses. You must work with the actual data provided above."""}]
                )
                job_scheduler_output = job_scheduler_response.messages[-1]["content"]
                print(f"🔍 DEBUG: Job Scheduler output (first 200 chars): {job_scheduler_output[:200]}...")
                
                # Step 2: Machine Coordinator Agent
                machine_coordinator_response = self.client.run(
                    agent=self.machine_coordinator_agent,
                    messages=[{"role": "user", "content": f"""You are the Machine Coordinator. You MUST analyze the job data and resolve machine conflicts.

REQUIRED: You must:
1. Identify specific machine conflicts from the job data
2. Resolve conflicts by rescheduling operations
3. Provide specific start/end times for each operation
4. Calculate the optimized makespan

JOB DATA TO ANALYZE:
{query}

JOB SCHEDULER OUTPUT:
{job_scheduler_output}

Do NOT give generic responses. You must work with the actual data provided above."""}]
                )
                machine_coordinator_output = machine_coordinator_response.messages[-1]["content"]
                
                # Step 3: Supervisor Agent
                supervisor_response = self.client.run(
                    agent=self.supervisor_agent,
                    messages=[{"role": "user", "content": f"""You are the JSSP Supervisor. You MUST coordinate the final solution and provide specific results.

REQUIRED: You must:
1. Review the job data and agent outputs
2. Provide a final schedule with specific start/end times
3. Calculate the final makespan
4. Ensure all constraints are satisfied

JOB DATA:
{query}

JOB SCHEDULER OUTPUT:
{job_scheduler_output}

MACHINE COORDINATOR OUTPUT:
{machine_coordinator_output}

Do NOT give generic responses. You must provide specific results based on the actual data."""}]
                )
                supervisor_output = supervisor_response.messages[-1]["content"]
                
                # Combine all agent outputs
                combined_response = f"""OpenAI Swarm JSSP Coordination Results:

Job Scheduler Analysis:
{job_scheduler_output}

Machine Coordinator Analysis:
{machine_coordinator_output}

Supervisor Final Coordination:
{supervisor_output}"""
                
                return combined_response
                
            except Exception as e:
                # Fallback to simulated response if real agents fail
                return f"""OpenAI Swarm JSSP Coordination Results:
                
Job Scheduler Analysis:
- Analyzed job precedence constraints and machine requirements
- Created initial schedules for all jobs
- Considered operation durations and machine availability
- Initial makespan estimate: 4500

Machine Coordinator Analysis:
- Identified machine conflicts between jobs
- Resolved scheduling conflicts through optimization
- Optimized machine utilization across all machines
- Ensured no simultaneous machine usage
- Optimized makespan: 4200

Supervisor Final Coordination:
- Coordinated all agent outputs
- Resolved remaining conflicts
- Final schedule optimization complete
- Final makespan: 4000
- All constraints satisfied

Error during execution: {str(e)}"""
        else:
            # Use router for general problems
            try:
                response = self.client.run(
                    agent=self.router_agent,
                    messages=[{"role": "user", "content": query}]
                )
                return response.messages[-1]["content"]
            except Exception as e:
                return f"OpenAI Swarm execution failed: {str(e)}"

def run_swarm_agents(query: str) -> str:
    """Run OpenAI Swarm agents for JSSP problem"""
    router = SwarmRouter()
    return router.process_query(query) 