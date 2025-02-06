import asyncio
import json
import os
import gradio as gr
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, List

from patient import PatientCase, DocumentAnalysis
from agents.vision import (
    DocumentVisionAgent,
    VisionAnalysis,
)
from graph import (
    Graph,
    InitialNode,
    ParallelSpecialistNode,
    ValidationNode,
    SummaryNode,
    ErrorNode,
    GraphState,
    generate_graph,
    AnalysisStatus,
    SpecialistResult,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Sample patient data for the demo
SAMPLE_PATIENT_DATA = {
    "patient_id": 123456,
    "name": "John Doe",
    "age": 54,
    "sex": "Male",
    "weight": 81.6,
    "height": 180.0,
    "chief_complaint": "Chest pain",
    "present_illness": "Presented with intermittent chest pain over three days...",
    "case_id": "CARD-2024-001",
}

# Sample additional medical data as free text
SAMPLE_ADDITIONAL_INFO = """
Past Medical History:
- Hypertension
- Hyperlipidemia
- GERD

Family History:
- Father: MI at 67
- Mother: Hypertension

Medications:
- Amlodipine 10mg daily
- Atorvastatin 20mg daily

Vital Signs:
- Blood Pressure: 148/92
- Heart Rate: 88 bpm

Physical Examination:
- Cardiovascular: Regular rhythm, no murmurs
- Respiratory: Clear to auscultation bilaterally

Laboratory Results:
- Lipid Panel: Total Cholesterol 220, LDL 140
- Blood Glucose: 98 mg/dL (normal)

Diagnostic Tests:
- ECG: Normal sinus rhythm
- Chest X-ray: Clear lung fields

Social & Lifestyle:
- Occupation: Office Manager
- Smoking: Current smoker, 1 pack/day
- Exercise: Sedentary lifestyle
- Stress Level: Reports high work-related stress
"""

class MedicalAnalyzer:
    """Handles medical analysis pipeline using Pydantic graph workflow"""

    def __init__(self):
        self.graph = Graph(
            nodes=[
                InitialNode,
                ParallelSpecialistNode,
                ValidationNode,
                SummaryNode,
                ErrorNode,
            ]
        )

    def _format_specialist_result(self, result: SpecialistResult) -> str:
        """Format individual specialist results"""
        if result.status == AnalysisStatus.ERROR:
            return f"\n{result.specialty} Assessment Error: {result.error}\n"

        if result.status != AnalysisStatus.COMPLETED or not result.diagnosis:
            return f"\n{result.specialty} Assessment: Incomplete\n"

        duration = (result.end_time - result.start_time).total_seconds()
        return (
            f"\n{result.specialty} Assessment:\n"
            f"Diagnosis: {result.diagnosis.diagnosis}\n"
            f"Confidence: {result.diagnosis.confidence_score}\n"
            f"Analysis Duration: {duration:.2f}s\n"
            f"Recommendations:\n"
            f"{chr(10).join(f'• {rec}' for rec in result.diagnosis.recommendations)}\n"
        )

    def format_summary(self, summary: "PatientSummary") -> str:
        """Format patient summary report"""
        if not summary:
            return "Error: Summary generation failed"

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

async def read_file_content(file: gr.File) -> Tuple[bytes, str]:
    """Helper method to read file content"""
    if not file:
        raise ValueError("Empty file object")

    file_name = file.name if hasattr(file, "name") else str(file)
    logger.info(f"Reading file: {file_name}")

    if isinstance(file, str):
        with open(file, "rb") as f:
            content = f.read()
    elif hasattr(file, "name") and os.path.exists(file.name):
        with open(file.name, "rb") as f:
            content = f.read()
    elif hasattr(file, "read"):
        content = file.read()
    else:
        raise ValueError(f"Unable to read file content from {file_name}")

    if not content:
        raise ValueError(f"Empty file content for {file_name}")

    return content, file_name

class MedAgentUI:
    """Handles Gradio interface setup and management"""

    def __init__(self):
        self.analyzer = MedicalAnalyzer()
        self.vision_agent = DocumentVisionAgent()
        self.current_case = None

    def format_patient_case(self, case: PatientCase) -> str:
        """Format complete patient case including document analysis"""
        basic_info = f"""PATIENT CASE
{'-' * 20}
ID: {case.patient_id}
Name: {case.name}
Age: {case.age}
Sex: {case.sex}
Weight: {case.weight} kg
Height: {case.height} cm
Chief Complaint: {case.chief_complaint}
Case ID: {case.case_id}

Present Illness:
{case.present_illness}

Additional Medical Information:
{case.additional_info if case.additional_info else 'None provided'}

Document Analysis:
"""
        
        doc_analysis = []
        for doc in case.document_analysis:
            doc_analysis.extend([
                f"\nFile: {doc.file_name}",
                f"Type: {doc.file_type}",
                f"Timestamp: {doc.timestamp.strftime('%Y-%m-%d %H:%M')}",
                "Findings:",
                *[f"• {finding}" for finding in doc.findings],
                "Extracted Information:",
                json.dumps(doc.metadata, indent=2) if doc.metadata else "No additional information",
                "-" * 40
            ])
        
        if not doc_analysis:
            doc_analysis = ["No documents analyzed"]
        
        return basic_info + "\n".join(doc_analysis)

    async def generate_preview(
        self, required: str, additional: str, files: List[gr.File]
    ) -> str:
        """Generate patient case preview with document analysis"""
        try:
            required_data = json.loads(required)
            required_data["additional_info"] = additional

            # Create document analysis objects from vision results
            document_analyses = []
            if files:
                for file in files:
                    try:
                        content, file_name = await read_file_content(file)
                        vision_result = await self.vision_agent.analyze_document_with_prompt(
                            content, file_name
                        )
                        
                        # Convert vision result to DocumentAnalysis
                        doc_analysis = DocumentAnalysis(
                            file_name=file_name,
                            file_type=vision_result.document_type,
                            findings=[
                                f"{finding.category}: {finding.description} {finding.value} {finding.units}".strip()
                                for finding in vision_result.findings
                            ],
                            metadata={
                                "extracted_text": vision_result.extracted_text
                            }
                        )
                        document_analyses.append(doc_analysis)
                    except Exception as e:
                        logger.error(
                            f"Error processing file {getattr(file, 'name', str(file))}: {str(e)}"
                        )
                        continue

            # Add document analyses to patient data
            required_data["document_analysis"] = [doc.dict() for doc in document_analyses]
            
            # Create patient case
            self.current_case = PatientCase(**required_data)
            logger.info(f"Generated preview for {self.current_case.name} (ID: {self.current_case.patient_id})")

            # Format case preview
            case_preview = self.format_patient_case(self.current_case)
            return case_preview

        except Exception as e:
            logger.error(f"Error generating preview: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

    async def analyze_case(self) -> Tuple[str, str, str]:
        """Analyze the current patient case"""
        try:
            if not self.current_case:
                raise ValueError("No patient case available for analysis")

            # Initialize graph state
            state = GraphState(patient=self.current_case)

            # Run analysis workflow
            result, history = await self.analyzer.graph.run(InitialNode(), state=state)

            # Format specialist results
            specialist_results = []
            for specialty_result in result.specialist_results.values():
                specialist_results.append(
                    self.analyzer._format_specialist_result(specialty_result)
                )

            summary_text = (
                self.analyzer.format_summary(result.summary)
                if result.summary
                else "Error: Summary generation failed"
            )

            graph = generate_graph()
            return "\n".join(specialist_results), summary_text, graph

        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}", exc_info=True)
            return f"Error: {str(e)}", "", ""

    def create_interface(self) -> gr.Blocks:
        """Create and configure Gradio interface"""
        gr.close_all()

        with gr.Blocks(title="MedAgent AI") as demo:
            gr.Markdown("# MedAgent AI - Medical Analysis System")

            with gr.Tab("Patient Analysis"):
                with gr.Row():
                    # Left Column - Input Forms
                    with gr.Column(scale=1):
                        with gr.Group("Required Information"):
                            required_info = gr.Textbox(
                                label="Patient Data",
                                value=json.dumps(SAMPLE_PATIENT_DATA, indent=2),
                                lines=10,
                                show_copy_button=True,
                            )

                        with gr.Group("Additional Information (Optional)"):
                            additional_info = gr.Textbox(
                                label="Additional Medical Data",
                                value=SAMPLE_ADDITIONAL_INFO,
                                lines=15,
                                show_copy_button=True,
                            )

                        with gr.Group("Medical Documents"):
                            file_input = gr.File(
                                label="Upload Medical Documents",
                                file_count="multiple",
                                file_types=["image", ".pdf"],
                                height=100,
                            )

                        preview_btn = gr.Button(
                            "Generate Preview", variant="secondary"
                        )
                        
                        

                    # Right Column - Case Preview
                    with gr.Column(scale=1):
                        case_preview = gr.Textbox(
                            label="Patient Case Preview",
                            lines=30,
                            show_copy_button=True
                        )
                        
                        analyze_btn = gr.Button(
                            "Analyze Case", variant="primary"
                        )

            with gr.Tab("Analysis Results"):
                with gr.Row():
                    with gr.Column(scale=1):
                        specialist_results = gr.Textbox(
                            label="Specialist Assessment Results", 
                            lines=25, 
                            show_copy_button=True
                        )
                    with gr.Column(scale=1):
                        summary_output = gr.Textbox(
                            label="Summary Report", 
                            lines=25, 
                            show_copy_button=True
                        )

            with gr.Tab("Agent Graph"):
                graph_output = gr.HTML(
                    label="Agent Interaction Graph", 
                    value=generate_graph()
                )

            # Handle preview generation
            preview_btn.click(
                fn=self.generate_preview,
                inputs=[required_info, additional_info, file_input],
                outputs=[case_preview],
            )

            # Handle case analysis
            analyze_btn.click(
                fn=self.analyze_case,
                inputs=[],
                outputs=[specialist_results, summary_output, graph_output],
            )

        return demo

def main():
    """Application entry point"""
    logger.info("Initializing MedAgent AI application")
    app = MedAgentUI()
    demo = app.create_interface()

    demo.queue()
    logger.info("Starting Gradio server")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        max_threads=4,
    )

if __name__ == "__main__":
    main()
