from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PatientCase(BaseModel):
    """Patient case model containing all relevant medical information"""
    
    patient_id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    bmi: Optional[float]
    occupation: Optional[str]
    chief_complaint: str
    
    # Medical history
    present_illness: str
    past_medical_history: List[str]
    family_history: List[str]
    medications: List[str]
    
    # Physical examination
    vital_signs: dict
    physical_findings: dict
    
    # Test results
    laboratory_results: dict
    diagnostic_tests: dict
    
    # Additional information
    lifestyle: dict
    social_history: dict
    
    case_id: str
    timestamp: datetime = datetime.now()
