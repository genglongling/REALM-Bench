import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from .calculator import CalculatorTool
from crewai import Agent, Crew, Process, Task
from ..db.database import get_schema, get_table
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from ..prompt_templates.router_template import SYSTEM_PROMPT as MANAGER_SYSTEM_PROMPT
from ..prompt_templates.sql_generator_template import SYSTEM_PROMPT as SQL_SYSTEM_PROMPT
from .sql_query import SQLQueryTool

load_dotenv()

def run_crewai(query):
    """Run CrewAI for JSSP or general problems"""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    # Check if this is a JSSP problem
    if "Job Shop Scheduling Problem" in query or "JSSP" in query:
        return run_jssp_crewai(query, llm)
    else:
        # Original general-purpose implementation
        return run_general_crewai(query, llm)

def run_jssp_crewai(query, llm):
    """Run CrewAI specifically for JSSP problems"""
    # Job scheduler agent
    job_scheduler_agent = Agent(
        role="Job Scheduler",
        goal="Create initial schedules for individual jobs in JSSP problems.",
        backstory="""You are a job scheduling specialist for Job Shop Scheduling Problems.
        Your expertise includes:
        - Creating initial schedules for individual jobs
        - Considering job precedence constraints
        - Analyzing machine requirements and operation durations
        - Optimizing job-level scheduling decisions
        
        Provide detailed scheduling analysis and initial job schedules.""",
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    
    # Machine coordinator agent
    machine_coordinator_agent = Agent(
        role="Machine Coordinator",
        goal="Resolve machine conflicts and optimize machine utilization in JSSP.",
        backstory="""You are a machine coordination specialist for Job Shop Scheduling Problems.
        Your expertise includes:
        - Identifying machine conflicts between different jobs
        - Resolving scheduling conflicts
        - Optimizing machine utilization
        - Ensuring no overlapping operations on the same machine
        
        Provide conflict resolution strategies and machine optimization solutions.""",
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    
    # Supervisor agent
    supervisor_agent = Agent(
        role="JSSP Supervisor",
        goal="Coordinate all agents and provide the final optimized JSSP solution.",
        backstory="""You are the supervisor for Job Shop Scheduling Problems.
        Your responsibilities include:
        - Coordinating with Job Scheduler and Machine Coordinator agents
        - Collecting and synthesizing all scheduling information
        - Resolving any remaining conflicts
        - Optimizing the overall makespan
        - Providing the final coordinated schedule
        
        Ensure all constraints are satisfied and provide the minimum makespan solution.""",
        allow_delegation=True,
        verbose=True,
        llm=llm,
    )
    
    # Validation agent - COMMENTED OUT
    # validation_agent = Agent(
    #     role="JSSP Validation Agent",
    #     goal="Validate the final schedule to ensure all constraints are satisfied.",
    #     backstory="""You are a validation specialist for Job Shop Scheduling Problems.
    #     Your responsibilities include:
    #     - Checking job precedence constraints (operations within each job must be in order)
    #     - Verifying machine constraints (no overlapping operations on the same machine)
    #     - Validating makespan calculations
    #     - Ensuring all jobs are completed
    #     - Reporting any constraint violations
    #     
    #     ALWAYS start your response with "YES" if all constraints are satisfied, or "NO" if any constraints are violated.
    #     Then provide a detailed validation report with constraint satisfaction status.""",
    #     allow_delegation=False,
    #     verbose=True,
    #     llm=llm,
    # )

    jssp_task = Task(
        description=query,
        expected_output="A complete JSSP solution with optimized schedule and minimum makespan value.",
        agent=supervisor_agent,
    )
    
    # validation_task = Task(
    #     description="Validate the final JSSP schedule to ensure all constraints are satisfied.",
    #     expected_output="A detailed validation report confirming constraint satisfaction.",
    #     agent=validation_agent,
    # )

    crew = Crew(
        agents=[job_scheduler_agent, machine_coordinator_agent, supervisor_agent],  # validation_agent commented out
        tasks=[jssp_task],  # validation_task commented out
        process=Process.sequential,
        manager_agent=supervisor_agent,
    )
    result = crew.kickoff()
    return result.raw

def run_general_crewai(query, llm):
    """Original general-purpose CrewAI implementation"""
    calculator_tool = CalculatorTool()
    sql_query_tool = SQLQueryTool()

    calculator_agent = Agent(
        role="Calculator",
        goal="Perform basic arithmetic operations (+, -, *, /) on two integers.",
        backstory="You are a helpful assistant that can perform basic arithmetic operations (+, -, *, /) "
        "on two integers.",
        tools=[calculator_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    data_analyzer_agent = Agent(
        role="Data Analyzer",
        goal="Provide insights, trends, or analysis based on the data and prompt.",
        backstory="You are a helpful assistant that can provide insights, trends, or analysis based on "
        "the data and prompt.",
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    sql_query_agent = Agent(
        role="SQL Query",
        goal="Generate a SQL query based on a user prompt and runs it on the database.",
        backstory=SQL_SYSTEM_PROMPT.format(SCHEMA=get_schema(), TABLE=get_table()),
        tools=[sql_query_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )

    system_message = (
        "First, identify and make all necessary agent calls based on the user prompt. "
        "Ensure that you gather and aggregate the results from these agent calls. "
        "Once all agent calls are completed and the final result is ready, return it in a single message."
        "If the task is about finding any trends, use the SQL Query Agent first, to retrieve the data "
        "for Data Analyzer Agent."
    )
    manager_agent = Agent(
        role="Manager",
        goal=system_message,
        backstory=MANAGER_SYSTEM_PROMPT,
        allow_delegation=True,
        verbose=True,
        llm=llm,
    )

    user_query_task = Task(
        description=query,
        expected_output="Once all agent calls are completed and the final result is ready, return it "
        "in a single message.",
        agent=manager_agent,
    )

    crew = Crew(
        agents=[calculator_agent, data_analyzer_agent, sql_query_agent],
        tasks=[user_query_task],
        process=Process.sequential,
        manager_agent=manager_agent,
    )
    result = crew.kickoff()
    return result.raw
