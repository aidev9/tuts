import asyncio
import json
import gradio as gr
import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple

from ai_medagents.patient import PatientCase
from ai_medagents.agents.medical.cardiology import CardiologyAgent
from ai_medagents.agents.medical.neurology import NeurologyAgent
from ai_medagents.agents.medical.gastroenterology import GastroenterologyAgent
from ai_medagents.agents.summary import SummaryAgent
from ai_medagents.graph import generate_graph

# Constants
 # Sample patient data for the demo
SAMPLE_PATIENT_DATA = {
        "patient_id": 123456,
        "name": "John Doe",
        "age": 54,
        "sex": "Male",
        "weight": 81.6,
        "height": 180.0,
        "bmi": 25.1,
        "occupation": "Office Manager",
        "chief_complaint": "Chest pain",
        "present_illness": "Presented with intermittent chest pain over three days...",
        "past_medical_history": ["Hypertension", "Hyperlipidemia", "GERD"],
        "family_history": ["Father: MI at 67", "Mother: Hypertension"],
        "medications": ["Amlodipine 10mg", "Atorvastatin 20mg"],
        "vital_signs": {"blood_pressure": "148/92", "heart_rate": "88"},
        "physical_findings": {"cardiovascular": "Regular rhythm", "respiratory": "Clear"},
        "laboratory_results": {"lipids": "High", "glucose": "Normal"},
        "diagnostic_tests": {"ecg": "Normal", "chest_xray": "Clear"},
        "lifestyle": {"smoking": "Yes", "exercise": "Sedentary"},
        "social_history": {"stress": "High"},
        "case_id": "CARD-2024-001"
    }

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MedicalAnalyzer:
    """Handles medical analysis pipeline and agent coordination"""
    
    def __init__(self):
        self.specialists = {
            'Cardiology': CardiologyAgent(),
            'Neurology': NeurologyAgent(),
            'Gastroenterology': GastroenterologyAgent()
        }
        self.summary_agent = SummaryAgent()

    async def run_specialist_analysis(self, case: PatientCase) -> Tuple[List[Any], str]:
        """Run concurrent specialist analysis"""
        tasks = {
            specialty: asyncio.create_task(agent.analyze(case))
            for specialty, agent in self.specialists.items()
        }
        
        diagnoses = []
        specialist_results = []
        
        for specialty, task in tasks.items():
            try:
                result = await task
                diagnoses.append(result)
                specialist_results.append(self._format_specialist_result(specialty, result))
            except Exception as e:
                logger.error(f"Error in {specialty} analysis: {str(e)}")
                specialist_results.append(f"\n{specialty} Assessment Error: {str(e)}\n")
        
        return diagnoses, "\n".join(specialist_results)

    def _format_specialist_result(self, specialty: str, result: Any) -> str:
        """Format individual specialist results"""
        return f"\n{specialty} Assessment:\n" + \
               f"Diagnosis: {result.diagnosis}\n" + \
               f"Confidence: {result.confidence_score}\n" + \
               f"Recommendations:\n" + \
               "\n".join(f"• {rec}" for rec in result.recommendations) + "\n"

    def format_summary(self, summary: Any) -> str:
        """Format patient summary report"""
        return f"""PATIENT SUMMARY REPORT
{'-' * 20}
Patient: {summary.name} (ID: {summary.patient_id})
Date: {summary.timestamp.strftime('%Y-%m-%d %H:%M')}

Key Findings: {summary.main_findings}

Important Points:
{chr(10).join(f'• {point}' for point in summary.key_points)}

Lifestyle Recommendations:
{chr(10).join(f'• {rec}' for rec in summary.lifestyle_recommendations)}

Next Steps:
{chr(10).join(f'• {step}' for step in summary.follow_up_steps)}
"""

class MedAgentUI:
    """Handles Gradio interface setup and management"""
    
    def __init__(self):
        self.analyzer = MedicalAnalyzer()

    async def analyze_patient_case(self, patient_data: Dict[str, Any]) -> tuple[str, str, str]:
        """Process patient case and return analysis results"""
        try:
            case = PatientCase(**patient_data)
            logger.info(f"Analyzing case for {case.name} (ID: {case.patient_id})")
            
            # Run specialist analysis
            diagnoses, specialist_results = await self.analyzer.run_specialist_analysis(case)
            
            # Generate summary
            summary = await self.analyzer.summary_agent.create_summary(case=case, diagnoses=diagnoses)
            summary_text = self.analyzer.format_summary(summary)
            
            # Generate visualization
            graph = generate_graph()
            
            return specialist_results, summary_text, graph
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            return f"Error: {str(e)}", "", ""

    def create_interface(self) -> gr.Blocks:
        """Create and configure Gradio interface"""
        gr.close_all()

        with gr.Blocks(title="MedAgent AI") as interface:
            gr.Markdown("# MedAgent AI - Medical Analysis System")
            
            with gr.Tab("Patient Analysis"):
                with gr.Row():
                    with gr.Column():
                        with gr.Group("Required Information"):
                            required_info = gr.Textbox(
                                label="Required Patient Data",
                                value=json.dumps({
                                    "patient_id": SAMPLE_PATIENT_DATA["patient_id"],
                                    "name": SAMPLE_PATIENT_DATA["name"],
                                    "age": SAMPLE_PATIENT_DATA["age"],
                                    "sex": SAMPLE_PATIENT_DATA["sex"],
                                    "weight": SAMPLE_PATIENT_DATA["weight"],
                                    "height": SAMPLE_PATIENT_DATA["height"],
                                    "chief_complaint": SAMPLE_PATIENT_DATA["chief_complaint"],
                                    "present_illness": SAMPLE_PATIENT_DATA["present_illness"],
                                    "case_id": SAMPLE_PATIENT_DATA["case_id"]
                                }, indent=2),
                                lines=10,
                                show_copy_button=True
                            )
                        
                        with gr.Group("Additional Information (Optional)"):
                            additional_info = gr.Textbox(
                                label="Additional Medical Data",
                                value=json.dumps({
                                    "occupation": SAMPLE_PATIENT_DATA["occupation"],
                                    "past_medical_history": SAMPLE_PATIENT_DATA["past_medical_history"],
                                    "family_history": SAMPLE_PATIENT_DATA["family_history"],
                                    "medications": SAMPLE_PATIENT_DATA["medications"],
                                    "vital_signs": SAMPLE_PATIENT_DATA["vital_signs"],
                                    "physical_findings": SAMPLE_PATIENT_DATA["physical_findings"],
                                    "laboratory_results": SAMPLE_PATIENT_DATA["laboratory_results"],
                                    "diagnostic_tests": SAMPLE_PATIENT_DATA["diagnostic_tests"],
                                    "lifestyle": SAMPLE_PATIENT_DATA["lifestyle"],
                                    "social_history": SAMPLE_PATIENT_DATA["social_history"]
                                }, indent=2),
                                lines=15,
                                show_copy_button=True
                            )
                        
                        analyze_btn = gr.Button("Analyze Patient Case", variant="primary")

                        async def process_inputs(required: str, additional: str) -> tuple[str, str, str]:
                            """Process required and additional patient information"""
                            try:
                                required_data = json.loads(required)
                                additional_data = json.loads(additional) if additional.strip() else {}
                                
                                # Combine the data
                                data = {
                                    **required_data,
                                    **additional_data,
                                    "bmi": round(float(required_data["weight"]) / ((float(required_data["height"])/100) ** 2), 1)
                                }
                                
                                return await self.analyze_patient_case(data)
                            except json.JSONDecodeError as e:
                                error_msg = f"Invalid JSON format: {str(e)}"
                                return error_msg, "", ""
                            except Exception as e:
                                error_msg = f"Error processing input: {str(e)}"
                                return error_msg, "", ""
                    
                    with gr.Column():
                        specialist_output = gr.Textbox(label="Specialist Assessments", lines=20)
                        summary_output = gr.Textbox(label="Patient Summary", lines=20)
            
            with gr.Tab("Agent Graph"):
                graph_output = gr.HTML(
                    label="Agent Interaction Graph",
                    value=generate_graph()  # Generate graph on interface load
                )
            
            analyze_btn.click(
                fn=process_inputs,
                inputs=[required_info, additional_info],
                outputs=[specialist_output, summary_output, graph_output],
                api_name="analyze"
            )
        
        return interface

def main():
    """Application entry point"""
    logger.info("Initializing MedAgent AI application")
    app = MedAgentUI()
    interface = app.create_interface()
    
    interface.queue()
    logger.info("Starting Gradio server")
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        max_threads=4
    )

if __name__ == "__main__":
    main()
