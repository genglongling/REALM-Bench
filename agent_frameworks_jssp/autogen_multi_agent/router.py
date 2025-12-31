import os
import sys
import asyncio

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_agentchat.tools import AgentTool
from dotenv import load_dotenv

load_dotenv()


def run_autogen_agents(query: str):
    """Router: Run AutoGen agents for JSSP or general tasks"""
    model_client = AnthropicChatCompletionClient(
        model="claude-sonnet-4-20250514",
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    if "Job Shop Scheduling Problem" in query or "JSSP" in query:
        return asyncio.run(run_jssp_autogen_agents(query, model_client))
    else:
        return asyncio.run(run_general_autogen_agents(query, model_client))


async def run_jssp_autogen_agents(query: str, model_client):
    """Run AutoGen multi-agent setup for JSSP problems and return Supervisor’s final response"""
    try:
        # Specialist agents
        job_scheduler = AssistantAgent(
            name="Job_Scheduler",
            model_client=model_client,
            system_message=(
                "You are a Job Scheduling Agent. Analyze precedence constraints and machine requirements, "
                "then produce a concrete schedule with start/end times for each operation."
            )
        )

        machine_coordinator = AssistantAgent(
            name="Machine_Coordinator",
            model_client=model_client,
            system_message=(
                "You are a Machine Coordinator. Detect conflicts across jobs, resolve overlaps, "
                "and optimize machine utilization."
            )
        )

        supervisor = AssistantAgent(
            name="Supervisor",
            model_client=model_client,
            system_message=(
                "You are a Supervisor. Merge the outputs from Job Scheduler and Machine Coordinator, "
                "ensure all constraints are respected, and output the FINAL optimized schedule. "
                "End with: Final Makespan: [number]."
            )
        )
        
        # validation_agent = AssistantAgent(
        #     name="Validation_Agent",
        #     model_client=model_client,
        #     system_message=(
        #         "You are a Validation Agent. Check the final schedule for constraint violations: "
        #         "1) Job precedence constraints (operations within each job must be in order), "
        #         "2) Machine constraints (no overlapping operations on the same machine), "
        #         "3) Makespan calculations. "
        #         "ALWAYS start your response with 'YES' if all constraints are satisfied, or 'NO' if any constraints are violated. "
        #         "Then provide a detailed validation report with constraint satisfaction status."
        #     )
        # )

        # Wrap agents as tools
        job_scheduler_tool = AgentTool(job_scheduler, return_value_as_last_message=True)
        machine_coordinator_tool = AgentTool(machine_coordinator, return_value_as_last_message=True)
        supervisor_tool = AgentTool(supervisor, return_value_as_last_message=True)
        # validation_tool = AgentTool(validation_agent, return_value_as_last_message=True)  # commented out

        # Coordinator
        coordinator = AssistantAgent(
            name="JSSP_Coordinator",
            model_client=model_client,
            system_message=(
                "You are the JSSP Coordinator. Use the Job Scheduler, Machine Coordinator, and Supervisor tools "
                "to solve the scheduling problem step by step. Provide the final optimized schedule and makespan."
            ),
            tools=[job_scheduler_tool, machine_coordinator_tool, supervisor_tool],  # validation_tool commented out
            max_tool_iterations=10
        )

        # Run coordinator with streaming, collect all messages
        messages = []
        async for message in coordinator.run_stream(task=query):
            messages.append(message)

        if messages:
            # Return the full conversation for debugging
            full_conversation = []
            for msg in messages:
                if hasattr(msg, 'content'):
                    full_conversation.append(f"Message: {msg.content}")
                else:
                    full_conversation.append(f"Message: {str(msg)}")
            
            return "\n".join(full_conversation)

        return "No response generated."

    except Exception as e:
        return f"AutoGen JSSP execution failed: {str(e)}"


async def run_general_autogen_agents(query: str, model_client):
    """Simple fallback for non-JSSP queries"""
    try:
        assistant = AssistantAgent(
            name="General_Agent",
            model_client=model_client,
            system_message="Answer general queries clearly and concisely."
        )
        response = await assistant.run(task=query)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        return f"AutoGen general execution failed: {str(e)}"
