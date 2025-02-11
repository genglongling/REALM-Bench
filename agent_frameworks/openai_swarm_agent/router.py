import os
import sys
from typing import Dict, List

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from dotenv import load_dotenv
from prompt_templates.router_template import SYSTEM_PROMPT
from skills.skill_map import SkillMap
from swarm import Agent, Swarm

load_dotenv()

class SwarmRouter:
    def __init__(self):
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
        
        # Create the router agent that decides which agent to use
        self.router_agent = Agent(
            name="Router",
            instructions=SYSTEM_PROMPT,
            functions=[
                self.transfer_to_sql,
                self.transfer_to_analyzer
            ]
        )

    def transfer_to_sql(self):
        return self.sql_agent
        
    def transfer_to_analyzer(self):
        return self.analyzer_agent
        
    def process_query(self, query: str) -> str:
        response = self.client.run(
            agent=self.router_agent,
            messages=[{"role": "user", "content": query}]
        )
        return response.messages[-1]["content"] 