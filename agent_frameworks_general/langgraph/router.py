import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from analyze_data import data_analyzer
from langgraph.checkpoint.memory import MemorySaver
from generate_sql_query import generate_and_run_sql_query
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from prompt_templates.router_template import SYSTEM_PROMPT

load_dotenv()

tools = [generate_and_run_sql_query, data_analyzer]
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)


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
    app = create_agent_graph()

    final_state = app.invoke(
        {"messages": [HumanMessage(content=query), SystemMessage(content=SYSTEM_PROMPT)]},
        config={"configurable": {"thread_id": 42}},
    )
    
    # Get the raw output from the agent
    raw_output = final_state["messages"][-1].content
    
    # Try to parse the output for structured data
    try:
        import json
        import re
        
        # Look for JSON-like structures in the output
        json_pattern = r'\{[^{}]*"goals"[^{}]*\}'
        json_match = re.search(json_pattern, raw_output, re.DOTALL)
        
        if json_match:
            parsed = json.loads(json_match.group())
            return {
                "goals": parsed.get("goals", []),
                "constraints": parsed.get("constraints", []),
                "schedule": parsed.get("schedule", []),
                "raw_output": raw_output
            }
        else:
            # If no structured data found, try to extract goals and constraints from text
            goals = []
            constraints = []
            schedule = []
            
            # Simple extraction patterns
            if "goal" in raw_output.lower() or "objective" in raw_output.lower():
                goals = ["Task completed based on agent response"]
            
            if "constraint" in raw_output.lower() or "limit" in raw_output.lower():
                constraints = ["Constraints considered in planning"]
            
            if "schedule" in raw_output.lower() or "timeline" in raw_output.lower():
                schedule = [{"task": "Scheduled task", "time": "TBD"}]
            
            return {
                "goals": goals,
                "constraints": constraints,
                "schedule": schedule,
                "raw_output": raw_output
            }
            
    except Exception as e:
        # Fallback to basic structure if parsing fails
        return {
            "goals": [],
            "constraints": [],
            "schedule": [],
            "raw_output": raw_output,
            "error": str(e)
        }
