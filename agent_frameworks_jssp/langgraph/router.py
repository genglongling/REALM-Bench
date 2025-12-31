import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from .analyze_data import data_analyzer
from langgraph.checkpoint.memory import MemorySaver
from .generate_sql_query import generate_and_run_sql_query
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from ..prompt_templates.router_template import SYSTEM_PROMPT

load_dotenv()

tools = [generate_and_run_sql_query, data_analyzer]
# Set Anthropic API key for LangGraph with Claude-4
if "ANTHROPIC_API_KEY" in os.environ:
    model = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0, anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]).bind_tools(tools)
else:
    model = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0).bind_tools(tools)


# if the last message has a tool call, then we continue to the tools node
# otherwise, we stop
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def create_agent_graph():
    workflow = StateGraph(MessagesState)

    tool_node = ToolNode(tools)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
    )
    workflow.add_edge("tools", "agent")

    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app


def run_agent(query):
    """Run LangGraph agent for JSSP or general problems"""
    # Check if this is a JSSP problem
    if "Job Shop Scheduling Problem" in query or "JSSP" in query:
        return run_jssp_langgraph(query)
    else:
        # Original general-purpose implementation
        return run_general_langgraph(query)

def run_jssp_langgraph(query):
    """Run LangGraph specifically for JSSP problems with 3 real agents"""
    
    print("🤖 LangGraph Multi-Agent Coordination Started")
    print("📋 Problem: Job Shop Scheduling Problem (JSSP)")
    
    # Create 3 real agents with distinct roles
    agents = []
    
    # 1. Job Scheduler Agent - handles all job scheduling
    print("🔧 Job Scheduler Agent: Creating initial job schedules")
    job_scheduler_prompt = f"""You are a Job Scheduler Agent specialized in JSSP problems.
    {query}
    
    Your task: Create initial schedules for all jobs with start/end times and machine assignments.
    Provide specific scheduling details for each job operation.
    Output format: "Job Scheduler Analysis: [detailed scheduling analysis]" """
    
    app1 = create_agent_graph()
    job_scheduler_response = run_single_agent_workflow(app1, job_scheduler_prompt)
    print(f"🔍 DEBUG: Job Scheduler full response: {job_scheduler_response}")
    agents.append(f"Job Scheduler Agent: {job_scheduler_response}")
    
    # 2. Machine Coordinator Agent - resolves conflicts
    print("⚙️ Machine Coordinator Agent: Resolving machine conflicts")
    machine_coordinator_prompt = f"""You are a Machine Coordinator Agent specialized in JSSP problems.
    {query}
    
    Your task: Resolve machine conflicts and optimize machine utilization.
    Identify scheduling conflicts and provide conflict resolution strategies.
    Output format: "Machine Coordinator Analysis: [conflict resolution and optimization]" """
    
    app2 = create_agent_graph()
    machine_coordinator_response = run_single_agent_workflow(app2, machine_coordinator_prompt)
    print(f"🔍 DEBUG: Machine Coordinator full response: {machine_coordinator_response}")
    agents.append(f"Machine Coordinator Agent: {machine_coordinator_response}")
    
    # 3. Supervisor Agent - coordinates final solution
    print("👑 Supervisor Agent: Coordinating final solution")
    supervisor_prompt = f"""You are a Supervisor Agent specialized in JSSP problems.
    {query}
    
    Your task: Coordinate all schedules and provide the final optimized JSSP solution.
    Aggregate job schedules, resolve remaining conflicts, and calculate final makespan.
    Output format: "Supervisor Final Coordination: [final schedule with makespan: XXXX]" """
    
    app3 = create_agent_graph()
    supervisor_response = run_single_agent_workflow(app3, supervisor_prompt)
    print(f"🔍 DEBUG: Supervisor full response: {supervisor_response}")
    agents.append(f"Supervisor Agent: {supervisor_response}")
    
    # 4. Validation Agent - validates constraints - COMMENTED OUT
    # print("✅ Validation Agent: Validating constraints")
    # validation_prompt = f"""You are a Validation Agent specialized in JSSP problems.
    # {query}
    # 
    # Your task: Validate the final schedule to ensure all constraints are satisfied.
    # Check job precedence constraints, machine constraints, and makespan calculations.
    # ALWAYS start your response with "YES" if all constraints are satisfied, or "NO" if any constraints are violated.
    # Output format: "YES/NO - Validation Report: [constraint satisfaction status and violations]" """
    # 
    # app4 = create_agent_graph()
    # validation_response = run_single_agent_workflow(app4, validation_prompt)
    # print(f"🔍 DEBUG: Validation full response: {validation_response}")
    # agents.append(f"Validation Agent: {validation_response}")
    
    # Combine all real agent responses
    combined_response = "\n\n".join([
        "=== LANGGRAPH REAL AGENTS ===",
        "\n".join(agents),
        "\n=== FRAMEWORK ===",
        "Framework: LangGraph with 3 Real Agents"  # Updated from 4 to 3
    ])
    
    print("🎉 LangGraph coordination completed successfully")
    return combined_response

def run_single_agent_workflow(app, prompt):
    """Run a single agent workflow with timeout"""
    import signal
    import asyncio
    from langchain_core.messages import HumanMessage, SystemMessage
    
    def timeout_handler(signum, frame):
        raise TimeoutError("LangGraph execution timed out")
    
    # Set a 120-second timeout for individual agents
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(120)
    
    try:
        final_state = asyncio.run(app.ainvoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={"configurable": {"thread_id": 42, "recursion_limit": 3}}
        ))
        signal.alarm(0)
        return final_state["messages"][-1].content
    except TimeoutError:
        signal.alarm(0)
        return f"Agent response (timeout after 120s): {prompt[:100]}..."


def run_general_langgraph(query):
    """Run LangGraph for general queries"""
    app = create_agent_graph()
    
    # Add timeout and iteration limit to prevent infinite loops
    import signal
    import time
    
    def timeout_handler(signum, frame):
        raise TimeoutError("LangGraph execution timed out")
    
    # Set a 30-second timeout for general queries
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30)
    
    try:
        # Use async invoke for proper async handling
        import asyncio
        final_state = asyncio.run(app.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": 42, "recursion_limit": 5}}
        ))
        signal.alarm(0)  # Cancel the alarm
        return final_state["messages"][-1].content
    except TimeoutError:
        signal.alarm(0)  # Cancel the alarm
        return "LangGraph general query response (timeout after 30s)"