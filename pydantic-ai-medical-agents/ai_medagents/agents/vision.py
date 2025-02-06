from typing import List, Dict, Any
from datetime import datetime
import logging
import base64
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from models import get_vision_model

logger = logging.getLogger(__name__)

class LineItem(BaseModel):
    description: str = Field("", description="Description of the medical finding")
    category: str = Field("Other", description="Category of the finding")
    value: str = Field("", description="Value or measurement if applicable")
    units: str = Field("", description="Units of measurement if applicable")
    class Config:
        extra = "allow"

class VisionAnalysis(BaseModel):
    extracted_text: str = Field("", description="Raw text extracted from the document")
    medical_entities: Dict[str, Any] = Field(default_factory=dict, description="Structured medical entities found")
    findings: List[LineItem] = Field(default_factory=list, description="List of structured medical findings")
    document_type: str = Field("Unknown", description="Type of medical document")
    timestamp: datetime = Field(default_factory=datetime.now)
    class Config:
        extra = "allow"

DOCUMENT_VISION_PROMPT = """
You are a medical document analyzer specialized in extracting clinical information from medical documents and images.
Analyze the document and return a structured response with the following fields:

1. extracted_text: The relevant text extracted from the document
2. document_type: The type of medical document (e.g., "Lab Report", "Radiology Report", "Clinical Notes")
3. medical_entities: A dictionary of structured medical information
4. findings: A list of medical findings, each with:
   - category: The type of finding (e.g., "Vital Signs", "Lab Results", "Observations")
   - description: A clear description of the finding
   - value: The measured or observed value
   - units: The units of measurement (if applicable)

Focus on extracting and structuring the medical information accurately.
"""

@dataclass
class VisionDeps:
    """Dependencies for vision agent"""
    file_data: bytes
    file_name: str
    mime_type: str
    encoded_data: str

class DocumentVisionAgent:
    def __init__(self):
        self.agent = Agent(
            model=get_vision_model(),
            result_type=VisionAnalysis,
            system_prompt=DOCUMENT_VISION_PROMPT,
            deps_type=VisionDeps
        )
        
        @self.agent.system_prompt
        def get_system_prompt(ctx: RunContext[VisionDeps]) -> str:
            return DOCUMENT_VISION_PROMPT

    def _prepare_file_data(self, file_data: bytes, file_name: str) -> VisionDeps:
        """Prepare file data for vision analysis"""
        file_ext = file_name.lower().split('.')[-1]
        if file_ext not in ['jpg', 'jpeg', 'png', 'pdf']:
            raise ValueError(f"Unsupported file type: {file_ext}")

        mime = "application/pdf" if file_ext == "pdf" else f"image/{file_ext}"
        encoded = base64.b64encode(file_data).decode('utf-8')
        
        return VisionDeps(
            file_data=file_data,
            file_name=file_name,
            mime_type=mime,
            encoded_data=encoded
        )

    async def analyze_document_with_prompt(self, file_data: bytes, file_name: str) -> VisionAnalysis:
        logger.info(f"Starting analysis for file: {file_name}")
        
        try:
            deps = self._prepare_file_data(file_data, file_name)
            
            messages = [
                {"type": "text", "text": (
                    "Analyze this medical document and extract all relevant clinical information. "
                    "Structure your response with the following fields:\n"
                    "1. extracted_text\n"
                    "2. document_type\n"
                    "3. medical_entities\n"
                    "4. findings (each with category, description, value, and units)"
                )},
                {"type": "image_url", "image_url": {
                    "url": f"data:{deps.mime_type};base64,{deps.encoded_data}"
                }}
            ]

            result = await self.agent.run(
                messages
            )
            
            logger.info("Analysis complete")
            logger.info(f"Analysis result: {result.data}")
            
            if result is None or result.data is None:
                raise ValueError("Model returned no data")
                
            if not isinstance(result.data, VisionAnalysis):
                raise TypeError(f"Expected VisionAnalysis type, got {type(result.data)}")
            
            logger.info("Analysis complete")
            return result.data
            
        except Exception as e:
            logger.error(f"Error during vision analysis: {str(e)}", exc_info=True)
            raise