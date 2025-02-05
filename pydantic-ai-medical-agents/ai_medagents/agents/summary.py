from typing import List
from datetime import datetime
import logging
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from dataclasses import dataclass

logger = logging.getLogger(__name__)

from patient import PatientCase
from agents.base import Diagnosis
from models import get_medical_model

class PatientSummary(BaseModel):
    """Patient-friendly summary of medical findings"""
    patient_id: int
    name: str
    main_findings: str
    key_points: List[str]
    lifestyle_recommendations: List[str]
    follow_up_steps: List[str]
    timestamp: datetime = datetime.now()

@dataclass
class SummaryDeps:
    """Dependencies for summary agent"""
    case: PatientCase
    diagnoses: List[Diagnosis]

SUMMARY_PROMPT = """
You are a skilled medical communicator, responsible for translating complex medical findings into clear, patient-friendly explanations. Your goal is to help patients understand their medical situation without causing unnecessary anxiety.

Guidelines:
- Translate medical terminology into plain language
- Maintain accuracy while being accessible
- Focus on actionable information
- Be clear about next steps
- Stay positive but realistic
- Emphasize the importance of following medical advice

Provide a clear summary of the medical findings that helps the patient understand their condition and next steps.
"""

class SummaryAgent:
    """Agent for creating patient-friendly summaries of medical findings"""
    
    def __init__(self):
        self.agent = Agent(
            model=get_medical_model(),
            result_type=PatientSummary,
            system_prompt=SUMMARY_PROMPT,
            deps_type=SummaryDeps
        )
        
        @self.agent.system_prompt
        def get_system_prompt(ctx: RunContext[SummaryDeps]) -> str:
            diagnoses_text = "\n\n".join(
                f"Specialist Report ({i+1}):\n{d.diagnosis}"
                for i, d in enumerate(ctx.deps.diagnoses)
            )
            return f"Patient Case:\n{ctx.deps.case}\n\nSpecialist Findings:\n{diagnoses_text}"
    
    async def create_summary(
        self,
        case: PatientCase,
        diagnoses: List[Diagnosis],
        message_history: List[ModelMessage] = None
    ) -> PatientSummary:
        """
        Create a patient-friendly summary from specialist diagnoses
        
        Args:
            case: The patient case
            diagnoses: List of specialist diagnoses
            message_history: Optional list of previous model messages
            
        Returns:
            Patient-friendly summary of findings
        """
        try:
            logger.info(f"Creating summary for patient {case.name} (ID: {case.patient_id})")
            deps = SummaryDeps(case=case, diagnoses=diagnoses)
            
            result = await self.agent.run(
                "Create a patient-friendly summary of the medical findings.",
                deps=deps,
                message_history=message_history
            )
            
            if result is None or result.data is None:
                raise ValueError("Model returned no data")
            
            if not isinstance(result.data, PatientSummary):
                raise TypeError(f"Expected PatientSummary type, got {type(result.data)}")
            
            logger.info(f"Successfully created summary for patient {case.name}")
            return result.data
            
        except Exception as e:
            logger.error(f"Error creating patient summary: {str(e)}")
            raise
