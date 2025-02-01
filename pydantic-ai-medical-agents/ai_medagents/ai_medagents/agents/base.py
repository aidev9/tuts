from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from dataclasses import dataclass

from ai_medagents.patient import PatientCase
from ai_medagents.models import get_medical_model

class Diagnosis(BaseModel):
    """Diagnosis model containing medical analysis and recommendations"""
    patient_id: int
    name: str
    diagnosis: str
    confidence_score: float
    recommendations: List[str]
    timestamp: datetime = datetime.now()

@dataclass
class AgentDeps:
    """Dependencies for medical agents"""
    case: PatientCase

class MedicalAgent:
    """Base class for specialized medical agents"""
    
    def __init__(self, system_prompt: str):
        self.agent = Agent(
            model=get_medical_model(),
            result_type=Diagnosis,
            system_prompt=system_prompt,
            deps_type=AgentDeps
        )
        
        @self.agent.system_prompt
        def get_system_prompt(ctx: RunContext[AgentDeps]) -> str:
            return f"The patient case is {ctx.deps.case}."
    
    def analyze(self, case: PatientCase, message_history: List[ModelMessage] = None) -> Diagnosis:
        """Analyze patient case and provide diagnosis"""
        deps = AgentDeps(case=case)
        result = self.agent.run_sync(
            "What is the diagnosis based on the provided patient case?",
            deps=deps,
            message_history=message_history
        )
        
        if message_history is not None:
            message = ModelResponse(
                parts=[TextPart(content=result.data.diagnosis, part_kind='text')],
                timestamp=datetime.now().isoformat(),
                kind='response'
            )
            message_history.append(message)
            
        return result.data
