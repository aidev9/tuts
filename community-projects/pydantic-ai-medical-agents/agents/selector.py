from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

from models import get_medical_model
from patient import PatientCase
from agents.base import AgentDeps

class SelectedSpecialties(BaseModel):
    """List of selected medical specialties"""
    specialties: List[str]

@dataclass
class SelectorAgentDeps:
    """Dependencies for the agent selector"""
    case: PatientCase

AGENT_SELECTOR_PROMPT = """
You are a highly skilled medical intake specialist. Your task is to analyze a patient's case details and identify the most relevant medical specialties needed for a comprehensive evaluation.

Consider the following information:
- Chief complaint: The primary reason for the patient's visit.
- Present illness: Details about the current medical issue.
- Medical history: Past medical conditions, surgeries, and allergies.
- Other relevant information: Any additional details provided in the patient's case.

Based on your analysis, provide a list of the medical specialties that should be consulted. Only include specialties that are directly relevant to the patient's case.

Available Specialties:
- cardiology
- neurology
- gastroenterology
- psychotherapy
- pulmonology
- endocrinology
- orthopedics
- immunology
- dermatology
- emergency

Output a list of specialties, ensuring each specialty is relevant to the provided patient information.
"""

class AgentSelector:
    """Agent for selecting relevant medical specialties"""
    
    def __init__(self):
        self.agent = Agent(
            model=get_medical_model(),
            result_type=SelectedSpecialties,
            system_prompt=AGENT_SELECTOR_PROMPT,
            deps_type=SelectorAgentDeps
        )
        
        @self.agent.system_prompt
        def get_system_prompt(ctx: RunContext[SelectorAgentDeps]) -> str:
            return f"The patient case is: {ctx.deps.case}"
    
    async def select_specialties(self, case: PatientCase) -> List[str]:
        """Select relevant medical specialties based on patient case"""
        try:
            deps = SelectorAgentDeps(case=case)
            result = await self.agent.run(
                "Which medical specialties are relevant for this patient case?",
                deps=deps
            )
            
            if result is None or result.data is None:
                raise ValueError("Agent selector returned no data")
            
            if not isinstance(result.data, SelectedSpecialties):
                raise TypeError(f"Expected SelectedSpecialties type, got {type(result.data)}")
            
            return result.data.specialties
        except Exception as e:
            logging.error(f"Error in agent selector: {str(e)}")
            raise
