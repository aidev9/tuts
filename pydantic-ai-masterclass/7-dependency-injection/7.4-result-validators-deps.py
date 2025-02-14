import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.messages import (ModelMessage, ModelResponse, TextPart)
from dataclasses import dataclass
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
# This example demonstrates how to use result validators with dependencies in PydanticAI. The use case is a team of medical agents providing a diagnosis for a patient case. The agents are expected to take the patient's symptoms, evaluate the patient's condition, and provide a clear and helpful response.

case_description = """**Patient Case Report**

    **Patient Information:**
    - Name: Jeremy Irons, Jr. II
    - DoB: 01/01/1980
    - Sex: M
    - Weight: 180 lbs (81.6 kg)  
    - Height: 5'11" (180 cm)  
    - BMI: 25.1 kg/m²  
    - Occupation: Office Manager  
    - Chief Complaint: Chest pain

    **History of Present Illness:**  
    Jeremy Irons, Jr. II, a 45-year-old male, presented to the emergency department with complaints of intermittent chest pain over the past three days. The pain is described as a tightness in the center of the chest, radiating to the left arm and jaw. The episodes last approximately 10-15 minutes and occur both at rest and during exertion. He also reports mild shortness of breath and occasional dizziness. He denies nausea, vomiting, fever, or recent infections.

    **Past Medical History:**  
    - Hypertension (diagnosed 5 years ago)  
    - Hyperlipidemia (diagnosed 3 years ago)  
    - Mild gastroesophageal reflux disease (GERD)  
    - No prior history of myocardial infarction or stroke

    **Family History:**  
    - Father: Died at 67 from myocardial infarction  
    - Mother: Alive, 79, history of hypertension  
    - Sibling: One older brother (58), history of type 2 diabetes and coronary artery disease  

    **Lifestyle and Social History:**  
    - Smoker: 1 pack per day for 30 years  
    - Alcohol: Occasional, 2-3 drinks per week  
    - Diet: High in processed foods, moderate red meat intake, low vegetable consumption  
    - Exercise: Sedentary lifestyle, occasional walking  
    - Stress: High occupational stress  

    **Medications:**  
    - Amlodipine 10 mg daily  
    - Atorvastatin 20 mg daily  
    - Omeprazole 20 mg daily  

    **Physical Examination:**  
    - General: Alert, mildly anxious  
    - Vital Signs:
    - Blood Pressure: 148/92 mmHg
    - Heart Rate: 88 bpm
    - Respiratory Rate: 18 breaths/min
    - Temperature: 98.6°F (37°C)
    - Oxygen Saturation: 98% on room air  
    - Cardiovascular: No murmurs, rubs, or gallops; regular rate and rhythm  
    - Respiratory: Clear breath sounds bilaterally  
    - Abdomen: Soft, non-tender, no hepatosplenomegaly  
    - Extremities: No edema or cyanosis  

    **Laboratory Results:**  
    - Complete Blood Count (CBC): Normal  
    - Lipid Panel:
    - Total Cholesterol: 240 mg/dL (high)
    - LDL: 160 mg/dL (high)
    - HDL: 38 mg/dL (low)
    - Triglycerides: 180 mg/dL (high)  
    - Blood Glucose: 105 mg/dL (fasting, borderline high)  
    - Hemoglobin A1C: 5.8% (prediabetes)  
    - Troponin: 0.02 ng/mL (normal)  
    - Electrolytes: Normal  
    - Kidney Function: Normal creatinine and eGFR  

    **Diagnostic Tests:**  
    - **Electrocardiogram (ECG):** Mild ST depression in lead II, III, and aVF  
    - **Chest X-ray:** No acute abnormalities  
    - **Echocardiogram:** Normal left ventricular function, no significant valve abnormalities  
    - **Stress Test:** Positive for inducible ischemia  
    - **Coronary Angiography (Pending for Further Evaluation)**
"""

cardiology_agent_system_prompt = """
You are a highly specialized Cardiologist, trained to assist healthcare professionals and patients in diagnosing, managing, and understanding  cardiovascular diseases. You provide evidence-based recommendations, interpret neurological test results, and suggest treatment pathways in alignment with guidelines from the American Heart Association (AHA) and European Society of Cardiology (ESC).

Take the patient case from the context.

Provide a detailed diagnosis based on the patient's symptoms, medical history, and test results. Include a clear assessment, treatment plan, and prognosis.
"""

neurology_agent_system_prompt = """
You are a highly specialized Neurologist, trained to assist healthcare professionals and patients in diagnosing, managing, and understanding neurological conditions. You provide evidence-based recommendations, interpret neurological test results, and suggest treatment pathways in alignment with guidelines from the American Academy of Neurology (AAN) and other reputable sources.

Take the patient case from the context.

Provide a detailed diagnosis based on the patient's symptoms, medical history, and test results. Include a clear assessment, treatment plan, and prognosis.
"""

gastroenterology_agent_system_prompt = """
You are a highly specialized Gastroenterologist, designed to assist healthcare professionals and patients in diagnosing, managing, and understanding gastrointestinal (GI) conditions. You provide evidence-based insights, interpret diagnostic results, and suggest treatment pathways in alignment with guidelines from the American College of Gastroenterology (ACG) and other reputable sources.

Take the patient case from the context.

Provide a detailed diagnosis based on the patient's symptoms, medical history, and test results. Include a clear assessment, treatment plan, and prognosis.
"""

primary_care_agent_system_prompt = """
You are a Primary Care Physician, acting as an advanced diagnostic assistant capable of analyzing and synthesizing information from various medical specialists to arrive at a detailed, evidence-based final diagnosis. Your role is to function as a primary care physician (PCP) with expertise in integrating findings from cardiologists, neurologists, gastroenterologists and other specialists to provide a holistic assessment of a patient’s health.

Take the patient case from the context.

Provide a detailed diagnosis based on the patient's symptoms, medical history, and test results. Include a clear assessment, treatment plan, and prognosis.
"""

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
ollama_model = OpenAIModel(model_name='deepseek-r1', base_url='http://localhost:11434/v1')

class PatientCase(BaseModel):
    """PatientCase model - includes patient ID, full name, date of birth, sex, weight and case description"""
    
    patient_id: str
    name: str
    dob: str
    sex: str
    weight: int
    case_description: str

# Define the output model
class Diagnosis(BaseModel):
    """Diagnosis model - includes patient ID, full name and diagnosis - a detailed write up of the patient's condition, assessment, plan and prognosis. Must be a detailed response."""
    
    patient_id: str
    name: str
    diagnosis: str
    

@dataclass
class Deps:
    """Dependencies for the agent"""
    case: PatientCase

# Define the agents
neurology_agent = Agent(model=model, result_type=Diagnosis, system_prompt=neurology_agent_system_prompt, deps_type=Deps, retries=5)
cardiology_agent = Agent(model=model, result_type=Diagnosis, system_prompt=cardiology_agent_system_prompt, deps_type=Deps, retries=5)
gastroenterology_agent = Agent(model=model, result_type=Diagnosis, system_prompt=gastroenterology_agent_system_prompt, deps_type=Deps, retries=5)
primary_care_agent = Agent(model=model, result_type=Diagnosis, system_prompt=primary_care_agent_system_prompt, deps_type=Deps, retries=5)
reasoning_agent = Agent(model=ollama_model, system_prompt=primary_care_agent_system_prompt, deps_type=Deps, retries=5)

@primary_care_agent.system_prompt
@cardiology_agent.system_prompt
@neurology_agent.system_prompt
@gastroenterology_agent.system_prompt
def get_system_prompt(ctx: RunContext[Deps]) -> str:
    return f"The patient case is {ctx.deps.case}."

# Define the result validator
@cardiology_agent.result_validator
@neurology_agent.result_validator
@gastroenterology_agent.result_validator
@primary_care_agent.result_validator
async def result_validator_deps(ctx: RunContext[Deps], data: str) -> str:
    if type(data) is not Diagnosis:
        print(Fore.RED, 'Data type mismatch.')
        raise ModelRetry('Return data type mismatch.')
    if (ctx.deps.case.patient_id != data.patient_id):
        print(Fore.RED, 'Data content mismatch.', ctx.deps.case.patient_id, data.patient_id)
        raise ModelRetry('Patient ID or Patient name mismatch.')
    return data

# Run the agents
try:
    # Initialize the message history
    message_history: list[ModelMessage] = []
    
    # Create a customer profile
    case = PatientCase(patient_id="123-678-900", name="Jeremy Irons, Jr. II", dob="01/01/1980", sex="M", weight=180, case_description=case_description)
    
    # Create dependencies
    deps = Deps(case=case)
    
    # Ask the question
    question = "What is the diagnosis?"

    # Run the neurology agent
    result = neurology_agent.run_sync(question, deps=deps)
    print(Fore.GREEN, f"Neurology: {result.data.diagnosis}\n")
    message = ModelResponse(parts=[TextPart(content=result.data.diagnosis, part_kind='text')], timestamp=datetime.now().isoformat(), kind='response')
    message_history.append(message)

    # Run the gastroenterology agent
    result = gastroenterology_agent.run_sync(question, deps=deps)
    print(Fore.BLUE, f"Gastroenterology: {result.data.diagnosis}\n")
    message = ModelResponse(parts=[TextPart(content=result.data.diagnosis, part_kind='text')], timestamp=datetime.now().isoformat(), kind='response')
    message_history.append(message)

    # Run the cardiology agent
    result = cardiology_agent.run_sync(question, deps=deps)
    print(Fore.RED, f"Cardiology: {result.data.diagnosis}\n")
    message = ModelResponse(parts=[TextPart(content=result.data.diagnosis, part_kind='text')], timestamp=datetime.now().isoformat(), kind='response')
    message_history.append(message)

    # Run the Primary Care Physician agent
    result = primary_care_agent.run_sync(question, deps=deps)
    print(Fore.YELLOW, f"Primary care medicine: {result.data.diagnosis}\n")
    message = ModelResponse(parts=[TextPart(content=result.data.diagnosis, part_kind='text')], timestamp=datetime.now().isoformat(), kind='response')
    message_history.append(message)

    result = reasoning_agent.run_sync(question, deps=deps, message_history=message_history)
    print(Fore.WHITE, '-----------------------------------')
    print(Fore.WHITE, f"Final report: {result.data}")
    print(Fore.WHITE, '-----------------------------------')

except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)