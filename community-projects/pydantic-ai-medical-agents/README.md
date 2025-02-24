# **MedAgent AI - Multi-Agent Medical Analysis System**

## **Overview**
MedAgent AI is a multi-agent medical assistant that processes patient documents to generate structured diagnoses and medical reports. The system utilizes **Pydantic** to define specialized medical agents, each focusing on different medical fields. A reporting agent compiles findings, and a summary agent provides a patient-friendly version of the report.

---

## **Key Features**

### **1. Multi-Agent Medical Analysis**
- Specialized AI agents for different medical fields (e.g., Cardiology, Neurology, Radiology, etc.).
- Each agent extracts relevant insights based on medical documents.
- **Smart Agent Selection:** The system intelligently selects the most relevant medical specialists for each case, improving efficiency and accuracy.

### **2. Report Generation Workflow**
- An **Agent Selector** determines the necessary medical specialties based on the patient's information.
- Relevant **Medical Agents** analyze the case and provide diagnoses.
- A **Summary Agent** simplifies medical terminology for patients.

### **3. Document Processing**
- Accepts PDFs, scanned images, or structured medical data.

### **5. Confidence Scoring & Cross-Validation**
- Each agent assigns confidence scores to its diagnoses.

### **5. Interactive UI & Agent Visualization**
- Built using **Gradio** for an intuitive interface
- Patient data input through JSON editor
- Real-time medical analysis with specialist assessments
- Patient-friendly summary generation
- Interactive agent graph visualization showing system architecture

---

## **System Architecture**

### **1. Input Layer**
- **Document Uploads:** Users submit medical documents (PDF, text, images).
- **User Inputs:** Users specify additional context (symptoms, history, etc.).

### **2. Processing Layer**
- **OCR/NLP Module:** Vision model extracts structured text from medical reports.
- **Agent Selector:** Analyzes the patient case and intelligently selects relevant medical specialties.
- **Medical Agents:** Specialized AI agents analyze text and generate insights for the selected specialties.
- **Summary Agent:** Converts findings into a patient-friendly explanation.

### **3. Output Layer**
- **Structured JSON Response:** Detailed medical analysis with findings, confidence scores, and recommendations from the selected specialists.
- **Patient Summary Report:** Simplified version for non-experts.

---

## **Setup Instructions (Using Poetry)**

### **1. Install Poetry**
```sh
pip install poetry
```

### **2. Initialize Virtual Environment & Install Dependencies**
```sh
poetry install
```

### **3. Set Up Environment Variables**
Create a `.env` file with the following configuration:

```sh
# OpenRouter/OpenAI API Keys
OPENROUTER_API_KEY=your_openrouter_key_here
OPENAI_API_KEY=your_openai_key_here

# Medical model configuration
MEDICAL_API_KEY=your_medical_api_key
MEDICAL_BASE_URL=https://openrouter.ai/api/v1
MEDICAL_MODEL=openai/gpt-4o-mini

# Vision model configuration
VISION_API_KEY=your_vision_api_key
VISION_BASE_URL=https://openrouter.ai/api/v1    
VISION_MODEL=openai/gpt-4o-mini
```

Modify accordingly if not using openrouter

Optional: For local model deployment using Ollama, uncomment and configure:
```sh
# LOCAL MEDICAL CONFIG
# MEDICAL_BASE_URL=http://localhost:11434/v1
# MEDICAL_MODEL=llama2

# LOCAL VISION CONFIG
# VISION_BASE_URL=http://localhost:11434/v1
# VISION_MODEL=llava
```

### **4. Run the Gradio UI**
```sh
poetry run python -m app
```

The default port for Gradio is 7860. When you run the Gradio UI, it will be accessible at: http://127.0.0.1:7860
You can open this URL in your web browser to interact with the application.

The UI provides:
- Patient data input through a JSON editor (with sample data)
- Real-time analysis from multiple medical specialists
- Patient-friendly summary generation
- Interactive visualization of agent relationships

---

## **Creating and Integrating Medical Agents**

To add a new medical specialist agent to the system, follow these steps:

### **1. Create a New Agent File**
- Create a new Python file in the `ai_medagents/agents/medical/` directory.
- Name the file according to the specialty (e.g., `cardiology.py`, `neurology.py`).

### **2. Implement the Agent Class**
- Define a new class that inherits from the `MedicalAgent` base class (in `ai_medagents/agents/base.py`).
- Create a specialized system prompt (using a multi-line string) that defines:
    - The agent's role and expertise
    - Core capabilities (clinical assessment, diagnostic interpretation, etc.)
    - Treatment recommendation guidelines (referencing relevant medical societies)
    - Risk stratification for specific conditions
    - Behavior and tone guidelines (precise language, empathy, avoiding direct prescriptions)
- Initialize the agent with the system prompt in the `__init__` method.

**Example (`cardiology.py`):**
```python
from agents.base import MedicalAgent

CARDIOLOGY_PROMPT = """
You are a highly knowledgeable and empathetic Cardiologist...
(rest of the prompt)
"""

class CardiologyAgent(MedicalAgent):
    """Specialized agent for cardiology analysis and diagnosis"""
    
    def __init__(self):
        super().__init__(system_prompt=CARDIOLOGY_PROMPT)
```

### **3. Update the Analysis Workflow (`graph.py`)**

- Import the new agent class at the top of `ai_medagents/graph.py`.
- Add the agent to the `specialists` dictionary in `graph.py`.

**Example:**
```python
# In graph.py
from agents.medical.cardiology import CardiologyAgent

# ... (other imports)

@dataclass
class SpecialistsCoordinatorNode(BaseNode[GraphState]):
    # ...
    async def run(
        self,
        ctx: GraphRunContext[GraphState]
    ) -> Union['ValidationNode', 'ErrorNode']:
        # ...
        specialists = {
            'cardiology': CardiologyAgent,
            # ... (other agents)
        }
# ...
```

### **4. Restart the Application**
After making these changes, restart the Gradio application to include the new agent in the analysis workflow.
