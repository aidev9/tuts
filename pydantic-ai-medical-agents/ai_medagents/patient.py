from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class DocumentAnalysis(BaseModel):
    """Model for document analysis results"""
    file_name: str
    file_type: str
    timestamp: datetime = datetime.now()
    findings: List[str] = []
    metadata: Dict[str, Any] = {}

class PatientCase(BaseModel):
    """Patient case model containing all relevant medical information"""
    
    # Basic patient information
    patient_id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    chief_complaint: str
    present_illness: str
    case_id: str
    
    # Additional medical information as free text
    additional_info: str = ""
    
    # Metadata
    timestamp: datetime = datetime.now()
    
    # Document analysis
    document_analysis: List[DocumentAnalysis] = []
