
# **REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems**
<p align="center">
  ⬇️ <a href="https://github.com/genglongling/REALM-Bench?tab=readme-ov-file">Github</a>  
  📃 <a href="https://arxiv.org/abs/2502.18836">Paper</a>  
  🌐 <a href="https://example.com/project">Project Page</a>
</p>

This repository provides a comprehensive benchmark for evaluating multi-agent planning systems across **4 agent frameworks** and **11 real-world planning scenarios**. It implements **6 standard evaluation metrics** for assessing planning quality, optimality, coordination, constraint satisfaction, resource usage, and adaptation to disruptions.  
  
1. **11 Real-World Planning Scenarios** covering diverse domains:
   - **P11**: Job Shop Scheduling (JSSP) - Combinatorial optimization
   - **P1-P2**: Campus Tours - Single/multi-agent routing
   - **P3-P4**: Urban Ride-Sharing - Vehicle routing with disruptions
   - **P5-P6**: Event Logistics - Wedding/Thanksgiving coordination
   - **P7**: Disaster Relief - Resource allocation under uncertainty
   - **P8-P9**: Disruption Handling - Reactive replanning scenarios
   - **P10**: Supply Chain - Large-scale industrial planning

2. **6 Standard Evaluation Metrics** for comprehensive assessment:
   - **Planning Quality (Accuracy)** - Goal satisfaction rates
   - **Planning Optimality (Makespan)** - Cost/time efficiency
   - **Coordination Effectiveness** - Inter-agent consistency
   - **Constraint Satisfaction Rate** - Constraint adherence
   - **Resource Usage Rate** - Memory, time, and token utilization
   - **Adaptation to Disruption** - Replanning success rates

3. **4 Multi-Agent Frameworks** with standardized integration:
   - **LangGraph** - State machine-based orchestration
   - **AutoGen** - Conversational AI framework
   - **CrewAI** - Multi-agent collaboration
   - **OpenAI Swarm Agent** - Swarm-based coordination

4. **Comprehensive Evaluation Framework** with:
   - Automated benchmarking across frameworks
   - Statistical analysis and visualization
   - Detailed performance reporting
   - Extensible architecture for new frameworks/tasks  

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
  python agent_frameworks/openai_swarm_agent/main.py
  ```  
- **Using AutoGen**  
  - Ensure **Docker** is installed ([Get Docker](https://docs.docker.com/get-started/get-docker/))  
  - Start Docker before running AutoGen-based agents

### **3️⃣ Running Evaluation Benchmark**
Evaluate multi-agent planning performance across frameworks:

- **Run full benchmark evaluation**  
  ```bash
  python run_evaluation.py
  ```  
- **Run specific frameworks/tasks**  
  ```bash
  python run_evaluation.py --frameworks langgraph,crewai --tasks P11,P1,P2
  ```  
- **Run with mock runners for testing**  
  ```bash
  python run_evaluation.py --mock
  ```  
- **Run example evaluation**  
  ```bash
  python examples/evaluation_example.py
  ```  

---

## **📂 Project Structure**  
```
📦 REALM-Bench
│── 📂 design_patterns
│   ├── reflection.ipynb        # Reflection-based agent
│   ├── planning.ipynb          # Planning-based agent
│   ├── tool_use.ipynb          # Tool-using agent
│   ├── multiagent.ipynb        # Multi-agent collaboration
│   ├── multiagent-P0-P10.ipynb # Real-world examples P0-P10
│── 📂 agent_frameworks
│   ├── autogen_multi_agent/    # AutoGen-based implementation
│   ├── crewai_multi_agent/     # CrewAI-based implementation
│   ├── openai_swarm_agent/     # Swarm-based implementation
│   ├── langgraph/              # LangGraph-based implementation
│── 📂 evaluation
│   ├── metrics.py              # Standard evaluation metrics
│   ├── task_definitions.py     # 11 task definitions
│   ├── evaluator.py            # Main evaluation framework
│   ├── framework_runners.py    # Framework integration
│   └── README.md               # Evaluation documentation
│── 📂 examples
│   └── evaluation_example.py   # Usage examples
│── run_evaluation.py           # Main evaluation runner
│── .env                        # API keys & environment variables
│── requirements.txt            # Dependencies
│── README.md                   # Documentation
```

---

## **📊 Problem Datasets & Public Data Sources**

This benchmark includes 11 real-world planning problems. Below is a comprehensive summary of available public datasets for each problem type:

| Problem | Name | Category | Public Datasets | Dataset Links | Data Type | Size |
|---------|------|----------|-----------------|---------------|-----------|------|
| **P11** | Job Shop Scheduling (JSSP) | Scheduling | • OR-Library JSSP<br>• Beasley JSSP<br>• Taillard JSSP | • [OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/jsspinfo.html)<br>• [Beasley JSSP](https://www.researchgate.net/publication/220463473_OR-Library_distributing_test_problems_by_electronic_mail)<br>• [Taillard JSSP](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html) | Benchmark instances | 82 instances |
| **P1** | Single-Agent Campus Tour | Routing | • TSPLIB<br>• Custom campus layouts | • [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)<br>• [VRP datasets](http://vrp.galgos.inf.puc-rio.br/index.php/en/) | TSP/VRP instances | 100+ instances |
| **P2** | Multi-Group Campus Tours | Scheduling | • VRP with Time Windows<br>• Solomon datasets | • [Solomon VRP](http://web.cba.neu.edu/~msolomon/problems.htm)<br>• [Gehring & Homberger](http://www.bernabe.dorronsoro.es/vrp/) | VRP-TW instances | 56 instances |
| **P3** | Urban Ride-Sharing (URS) | Routing | • NYC Taxi Trip Data<br>• Chicago Taxi Data<br>• Uber Movement Data | • [NYC Taxi Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)<br>• [Chicago Taxi Data](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew)<br>• [Uber Movement](https://movement.uber.com/) | Real trip data | 100M+ trips |
| **P4** | URS with Disruptions | Routing | • NYC Taxi + Traffic Data<br>• Chicago Traffic Incidents | • [NYC Traffic](https://data.cityofnewyork.us/Transportation/Traffic-Incidents/)<br>• [Chicago Traffic](https://data.cityofchicago.org/Transportation/Traffic-Crashes/)<br>• [BTS Airline Delays](https://www.transtats.bts.gov/Tables.asp?QO_VQ=EFD) | Trip + disruption data | 10M+ records |
| **P5** | Wedding Logistics | Logistics | • Airport Pickup Data<br>• Event Planning Templates | • [Airport Traffic](https://www.transtats.bts.gov/)<br>• [Event Planning APIs](https://developers.google.com/maps/documentation/directions) | Synthetic + real data | Custom generation |
| **P6** | Thanksgiving Dinner Planning | Logistics | • Airport Traffic Data<br>• Recipe Preparation Times | • [BTS Airport Data](https://www.transtats.bts.gov/Tables.asp?QO_VQ=EFD)<br>• [Recipe APIs](https://spoonacular.com/food-api) | Traffic + recipe data | Custom generation |
| **P7** | Disaster Relief | Resource Allocation | • UN OCHA Datasets<br>• FEMA Disaster Data<br>• Humanitarian OSM | • [UN OCHA](https://data.humdata.org/)<br>• [FEMA Data](https://www.fema.gov/openfema-data-page)<br>• [Humanitarian OSM](https://www.hotosm.org/) | Disaster response data | 1000+ events |
| **P8** | Disruption Handling | Replanning | • Airline Delay Data<br>• Traffic Incident Data | • [BTS Airline Delays](https://www.transtats.bts.gov/Tables.asp?QO_VQ=EFD)<br>• [City Traffic APIs](https://developers.google.com/maps/documentation/traffic) | Delay/incident data | 1M+ records |
| **P9** | Advanced Disruption Handling | Replanning | • Multi-modal Disruption Data<br>• Weather Impact Data | • [Weather APIs](https://openweathermap.org/api)<br>• [Transit APIs](https://developers.google.com/maps/documentation/directions) | Multi-source data | Custom generation |
| **P10** | Supply Chain | Industrial Planning | • OR-Library Supply Chain<br>• MIPLIB<br>• TSPLIB | • [OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/)<br>• [MIPLIB](https://miplib.zib.de/)<br>• [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) | Optimization instances | 1000+ instances |

### **Dataset Generation Strategy**

For comprehensive benchmarking, we recommend a **hybrid approach**:

1. **Public Datasets (30%)** - Use real-world data where available
2. **Synthetic Generation (70%)** - Create diverse scenarios for consistent evaluation

### **Dataset Categories**

- **📊 Benchmark Instances** - Standard optimization problems (P11, P10)
- **🚗 Real Trip Data** - Actual transportation records (P3, P4)
- **🏢 Campus/Urban Layouts** - Geographic and spatial data (P1, P2)
- **🎉 Event Planning** - Logistics and coordination scenarios (P5, P6)
- **🚨 Disaster Response** - Emergency management data (P7)
- **⚠️ Disruption Events** - Real-time incident data (P8, P9)

### **Data Sources by Category**

| Category | Primary Sources | Data Format | Access |
|----------|----------------|-------------|---------|
| **Transportation** | NYC/Chicago Open Data, BTS | CSV, JSON | Public APIs |
| **Optimization** | OR-Library, MIPLIB | Text files | Direct download |
| **Geographic** | OpenStreetMap, Google Maps | GeoJSON, APIs | Public APIs |
| **Disaster** | UN OCHA, FEMA | CSV, APIs | Public APIs |
| **Events** | Custom generation | JSON | Synthetic |

---

## **📜 Citation**  

If you find this repository helpful, please cite the following paper:  

```
REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems  
Anonymous Author(s)  
```

---

