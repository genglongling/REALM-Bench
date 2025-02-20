# Agentic Design Patterns and Orchestration

This repository provides
1. Notebooks demonstrating a from-scratch implementation of four common design patterns: reflection, planning, tool use, and multi-agent collaboration.
2. Code defining an agent class for each of these design patterns.
3. Ready-to-use implementations of simple agent use cases across four different agent frameworks (AutoGen, CrewAI, Swarm, and LangGraph). These implementations can serve as a baseline for developing custom use cases.


# How To Run
1) Follow these steps to get started:
- create virtual environment `python3 -m venv venv` OR set python==3.10+ for your venv on your editor
- activate the  virtual environment `source venv/bin/activate` (`venv\Scripts\activate` on windows)
- install the requirements `pip install -r requirements.txt` 
- create a `.env` files and add an openai key to it `OPENAI_API_KEY="sk-proj ...."`
- open "jupyter notebook" on terminal/editor and create your **specialized/taylored use case** in "design_patterns/multiagent.ipynb".


2) (Optional) Using on of the agent frameworks:
- execute the`main.py` of the one of the frameworks, e.g. `python agent_frameworks/openai_swarm_agent`
- For using Autogen you need to have docker running. I you do not have it installed on your system, download it from the website (https://docs.docker.com/get-started/get-docker/). Then install and open it.

# Citation

If you find this repository helpful, consider citing the following paper:

```
REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems
Longling Geng, Edward Y. Chang
```
