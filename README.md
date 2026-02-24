# MIDAS v23.7: Joseph D. Arico Strategic Suite

The MIDAS Project Mission Statement
Vision Statement
"The Minimax-based Interactive Dynamic Assessment Simulation (MIDAS) project is dedicated to the advancement of non-linear strategic modeling. Our mission is to provide an open-source framework that moves beyond binary 'win-loss' outcomes, focusing instead on Systemic Resilience and Structural Integrity. By quantifying the friction of geopolitical and technological conflict, MIDAS empowers analysts to visualize the 'brittleness' of modern centers of gravity in the face of stochastic 'Black Swan' shocks."

— Joseph D. Arico, Lead Architect

MIDAS (Minimax-based Interactive Dynamic Assessment Simulation) is a comprehensive analytical platform designed to model the systemic decay of global actors across ten high-stakes flashpoints.

## 🚀 Getting Started with MIDAS v23.7
Follow these steps to initialize your first strategic simulation using the Minimax-based Interactive Dynamic Assessment Simulation suite.

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system. You will also need the following libraries:

Bash
pip install numpy matplotlib pillow
### 2. Local Setup
Clone the Repository:

Bash
git clone https://github.com/jd0613-byte/MIDAS-Strategic-Simulation.git
cd MIDAS-Strategic-Simulation
Verify Data Integrity: Ensure that both MIDAS_v23_7.py and scenarios.json are present in the root directory.

### 3. Running Your First Simulation
Launch the Engine: ```bash
python MIDAS_v23_7.py

Configure the Parameters: * Select a Flashpoint (e.g., UKRAINE_ATTR) from the dropdown menu.

Choose an AI Doctrine (e.g., CAUTIOUS) to define the actor's risk profile.

Ensure Black Swan Events is toggled ON to test for non-linear resilience.

Execute: Click EXECUTE SIMULATION.

Analyze the Feed: Observe the live decay graph. Look for the Sawtooth recovery spikes in attrition scenarios or yellow Black Swan markers indicating a systemic shock.

### 4. Exporting Intelligence
Once the simulation reaches a terminal state (collapse or turn limit), a Post-Action Briefing will generate in the report window.

Review the "THE WHY" section for a qualitative root-cause analysis.

Click SAVE BRIEFING REPORT to export this data as a timestamped .txt file for your records.


## 🚀 Strategic Overview
MIDAS utilizes a minimax-inspired assessment engine to calculate "Structural Integrity" based on friction, doctrine, and non-linear shocks.



## 📈 System Resilience: The Black Swan Engine
Version 23.6 introduces the **Black Swan Event Toggle**, allowing analysts to inject sudden, asymmetrical shocks (25-45% integrity loss) into the simulation. This tests not just the endurance of a system, but its fundamental resilience.



## 📂 Flashpoint Scenarios
1.  **Taiwan Strait Crisis**: Amphibious invasion and blockade logic.
2.  **Ukraine Attrition**: Sawtooth aid recovery and industrial endurance.
3.  **Kessler Event**: Debris cascades and technological interconnectedness.
4.  **Currency War**: Economic reserve hegemony and debt weaponization.
5.  ...and 6 more specialized strategic environments.



## 🛠️ Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run simulation: `python MIDAS_v23_6.py`
3. Review Post-Action Reports (PAR) for Root Cause Analysis (The "Why").

## 🆕 Version 23.7: The Modular Intelligence Update

The latest version of **MIDAS** (**M**inimax-based **I**nteractive **D**ynamic **A**ssessment **S**imulation) introduces a modular architecture designed for high-level strategic research.

### 🛠️ Key Architectural Changes:
* **Data/Logic Decoupling:** Strategic flashpoints are now stored in `scenarios.json`. This allows for rapid scenario expansion without modifying the simulation engine.
* **Resilience Analytics:** Enhanced modeling of systemic "brittleness" through the updated Black Swan engine.
* **Production-Ready Error Handling:** Integrated path verification to ensure stable execution across different OS environments.

### 📂 Repository Structure:
* `MIDAS_v23_7.py`: Core Simulation & Visualization Engine.
* `scenarios.json`: The Intelligence Database (10+ scenarios).
* `requirements.txt`: Environment dependencies.
