# **MedAgent AI - Multi-Agent Medical Analysis System**

## **Overview**
MedAgent AI is a multi-agent medical assistant that processes patient documents to generate structured diagnoses and medical reports. The system utilizes **Pydantic AI** to define specialized medical agents, each focusing on different medical fields. A reporting agent compiles findings, and a summary agent provides a patient-friendly version of the report. Users can integrate their own OpenRouter API keys for custom AI processing.

---

## **Key Features**

### **1. Multi-Agent Medical Analysis**
- Specialized AI agents for different medical fields (e.g., Cardiology, Neurology, Radiology, etc.).
- Each agent extracts relevant insights based on medical documents.

### **2. Report Generation Workflow**
- A **Report Writing Agent** consolidates findings into a structured report.
- A **Summary Agent** simplifies medical terminology for patients.

### **3. User-Provided API Keys**
- Users can enter their **OpenRouter API key** to utilize custom AI models.

### **4. Document Processing**
- Accepts PDFs, scanned images, or structured medical data.

### **5. Confidence Scoring & Cross-Validation**
- Each agent assigns confidence scores to its diagnoses.
- Cross-agent validation ensures accuracy.

### **6. Interactive UI & Agent Visualization**
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
- **API Key Handling:** Users provide an OpenRouter API key for custom LLM processing.

### **2. Processing Layer**
- **OCR/NLP Module:** Vision model Extracts structured text from medical reports.
- **Medical Agents:** Specialized AI agents analyze text and generate insights.
- **Report Writing Agent:** Aggregates insights into a structured report.
- **Summary Agent:** Converts findings into a patient-friendly explanation.

### **3. Output Layer**
- **Structured JSON Response:** Detailed medical analysis with findings, confidence scores, and recommendations.
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
Create a `.env` file with your OpenRouter API key:
```sh
OPENROUTER_API_KEY=your_api_key_here
```

### **4. Run the Gradio UI**
```sh
poetry run python -m app
```

The UI provides:
- Patient data input through a JSON editor (with sample data)
- Real-time analysis from multiple medical specialists
- Patient-friendly summary generation
- Interactive visualization of agent relationships
