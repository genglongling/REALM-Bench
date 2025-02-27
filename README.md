
# **REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems**
<p align="center">
  ⬇️ <a href="https://github.com/genglongling/REALM-Bench?tab=readme-ov-file">Github</a>  
  📃 <a href="https://arxiv.org/abs/2502.18836">Paper</a>  
  🌐 <a href="https://example.com/project">Project Page</a>
</p>

This repository provides a broad extension of real-world use cases of Multi Agentic Design, Orchestration, and Planning in Real-World Scenerios. This framework serves as baselines for developing **customized multi-agent use cases**.  
  
1. **Notebooks** demonstrating a from-scratch implementation of four fundamental agentic design patterns:  
   - **Planning and Scheduling:** 1) Sequential planning, 2) Reactive planning, 3) Complex planning, 4) Others
   - **Tool Use:** 1) WriteToFile, 2) GoogleSearchAPI, 3) Other API (e.g. Financial), 4) Others
   - **Reflection**
   - **Memory**
   - **Reasoning**
   - **Forecasting**
   - **Math Induction, Calculation**
   - **Multi-Agent Collaboration**  
2. **Design Pattern and Modular Agent Classes**
   - implementing each design pattern in a simple, extensible, and applicable manner.  
3. **Multi-Agent Frameworks** across four different agent ecosystems:  
   - **AutoGen**  
   - **CrewAI**  
   - **Swarm**  
   - **LangGraph**  

---

## **🚀 How To Run**  

### **1️⃣ Setup Environment**  
Follow these steps to get started:  

- **Create a virtual environment**  
  ```bash
  python3 -m venv venv
  ```
  making sure your program using python==3.10+ for your venv on your editor.
  
- **Activate the virtual environment**  
  - macOS/Linux:  
    ```bash
    source venv/bin/activate
    ```  
  - Windows:  
    ```bash
    venv\Scripts\activate
    ```  
- **Install dependencies**  
  ```bash
  pip install -r requirements.txt
  ```  
- **Set up OpenAI API credentials**  
  - Create a `.env` file in the root directory  
  - Add your OpenAI API key:  
    ```env
    OPENAI_API_KEY="sk-proj-..."
    ```  
- **Run Jupyter Notebook**  
  ```bash
  jupyter notebook
  ```  
  - Open and modify `design_patterns/multiagent.ipynb` to create your **specialized multi-agent use case**.  

---

### **2️⃣ Running Multi-Agent Frameworks**
(Optional) You can execute agents using one of the frameworks:  

- **Run an agent framework**  
  ```bash
  python agent_frameworks/openai_swarm_agent.py
  ```  
- **Using AutoGen**  
  - Ensure **Docker** is installed ([Get Docker](https://docs.docker.com/get-started/get-docker/))  
  - Start Docker before running AutoGen-based agents  

---

## **📂 Project Structure**  
```
📦 Agentic-Design-Patterns
│── 📂 design_patterns
│   ├── reflection.ipynb        # Reflection-based agent
│   ├── planning.ipynb          # Planning-based agent
│   ├── tool_use.ipynb          # Tool-using agent
│   ├── multiagent.ipynb        # Multi-agent collaboration
│   ├── multiagent_examples.ipynb  # Real-world examples from P3-P11, Entry point for running agents
│── 📂 agent_frameworks
│   ├── autogen_multi_agent.py  # AutoGen-based implementation
│   ├── crewai_multi_agent.py   # CrewAI-based implementation
│   ├── swarm_agent.py          # Swarm-based implementation
│   ├── langgraph_agent.py      # LangGraph-based implementation
│── .env                        # API keys & environment variables
│── requirements.txt            # Dependencies
│── README.md                   # Documentation
```

---

## **📜 Citation**  

If you find this repository helpful, please cite the following paper:  

```
REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems  
Anonymous Author(s)  
```

---

