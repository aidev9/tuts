from datetime import datetime
from colorama import Fore
from dotenv import load_dotenv

from ai_medagents.patient import PatientCase
from ai_medagents.agents.medical.cardiology import CardiologyAgent
from ai_medagents.agents.medical.neurology import NeurologyAgent
from ai_medagents.agents.medical.gastroenterology import GastroenterologyAgent
from ai_medagents.agents.summary import SummaryAgent

# Load environment variables
load_dotenv()

# Sample patient case
SAMPLE_CASE = {
    "patient_id": 123456,
    "name": "John Doe",
    "age": 54,
    "sex": "Male",
    "weight": 81.6,  # kg
    "height": 180.0,  # cm
    "bmi": 25.1,
    "occupation": "Office Manager",
    "chief_complaint": "Chest pain",
    
    "present_illness": """
    Presented to the emergency department with complaints of intermittent chest pain over the past three days. 
    The pain is described as a tightness in the center of the chest, radiating to the left arm and jaw. 
    Episodes last approximately 10-15 minutes and occur both at rest and during exertion. 
    Also reports mild shortness of breath and occasional dizziness.
    """,
    
    "past_medical_history": [
        "Hypertension (diagnosed 5 years ago)",
        "Hyperlipidemia (diagnosed 3 years ago)",
        "Mild gastroesophageal reflux disease (GERD)"
    ],
    
    "family_history": [
        "Father: Died at 67 from myocardial infarction",
        "Mother: Alive, 79, history of hypertension",
        "Sibling: One older brother (58), history of type 2 diabetes and coronary artery disease"
    ],
    
    "medications": [
        "Amlodipine 10 mg daily",
        "Atorvastatin 20 mg daily",
        "Omeprazole 20 mg daily"
    ],
    
    "vital_signs": {
        "blood_pressure": "148/92 mmHg",
        "heart_rate": "88 bpm",
        "respiratory_rate": "18 breaths/min",
        "temperature": "37.0 C",
        "oxygen_saturation": "98% on room air"
    },
    
    "physical_findings": {
        "cardiovascular": "No murmurs, rubs, or gallops; regular rate and rhythm",
        "respiratory": "Clear breath sounds bilaterally",
        "abdomen": "Soft, non-tender, no hepatosplenomegaly",
        "extremities": "No edema or cyanosis"
    },
    
    "laboratory_results": {
        "lipid_panel": {
            "total_cholesterol": "240 mg/dL (high)",
            "ldl": "160 mg/dL (high)",
            "hdl": "38 mg/dL (low)",
            "triglycerides": "180 mg/dL (high)"
        },
        "blood_glucose": "105 mg/dL (fasting, borderline high)",
        "hba1c": "5.8% (prediabetes)",
        "troponin": "0.02 ng/mL (normal)",
        "cbc": "Normal",
        "electrolytes": "Normal",
        "kidney_function": "Normal creatinine and eGFR"
    },
    
    "diagnostic_tests": {
        "ecg": "Mild ST depression in lead II, III, and aVF",
        "chest_xray": "No acute abnormalities",
        "echocardiogram": "Normal left ventricular function, no significant valve abnormalities",
        "stress_test": "Positive for inducible ischemia"
    },
    
    "lifestyle": {
        "smoking": "1 pack per day for 30 years",
        "alcohol": "2-3 drinks per week",
        "diet": "High in processed foods, moderate red meat intake, low vegetable consumption",
        "exercise": "Sedentary lifestyle, occasional walking"
    },
    
    "social_history": {
        "occupation_stress": "High",
        "living_situation": "Lives with spouse",
        "support_system": "Good family support"
    },
    
    "case_id": "CARD-2024-001"
}

def main():
    try:
        # Create patient case
        case = PatientCase(**SAMPLE_CASE)
        
        # Initialize agents
        cardio_agent = CardiologyAgent()
        neuro_agent = NeurologyAgent()
        gastro_agent = GastroenterologyAgent()
        summary_agent = SummaryAgent()
        
        # Collect specialist diagnoses
        print("Analyzing patient case...")
        
        specialists = {
            'Cardiology': cardio_agent,
            'Neurology': neuro_agent,
            'Gastroenterology': gastro_agent
        }
        
        diagnoses = []
        for specialty, agent in specialists.items():
            result = agent.analyze(case)
            diagnoses.append(result)
            print(f"\n{specialty} Assessment:")
            print(f"Diagnosis: {result.diagnosis}")
            print(f"Confidence: {result.confidence_score}")
        
        # Create and print patient summary
        print("\nCreating Patient Summary...")
        summary = summary_agent.create_summary(case=case, diagnoses=diagnoses)
        
        print("\nPATIENT SUMMARY REPORT")
        print("-" * 20)
        print(f"Patient: {summary.name} (ID: {summary.patient_id})")
        print(f"Date: {summary.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print("\nKey Findings:", summary.main_findings)
        
        sections = {
            'Important Points': summary.key_points,
            'Lifestyle Recommendations': summary.lifestyle_recommendations,
            'Next Steps': summary.follow_up_steps
        }
        
        for title, items in sections.items():
            print(f"\n{title}:")
            print("\n".join(f"• {item}" for item in items))
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
