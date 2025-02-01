from pydantic import BaseModel
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from ai_medagents.patient import PatientCase
from ai_medagents.agents.base import Diagnosis, AgentDeps
from ai_medagents.agents.summary import PatientSummary, SummaryDeps

class SpecialistDiagnosis(BaseModel):
    """Links patient case to specialist diagnosis"""
    patient: PatientCase
    diagnosis: Diagnosis

class SummaryAnalysis(BaseModel):
    """Links patient case and diagnoses to summary"""
    patient: PatientCase
    diagnoses: List[Diagnosis]
    summary: PatientSummary

def generate_graph() -> str:
    """Generate graph using pydantic-graph"""
    logger.info("Starting graph generation")
    from pydantic_graph import Graph, BaseNode, End
    
    class PatientNode(BaseNode[PatientCase]):
        async def run(self, ctx) -> 'DiagnosisNode':
            logger.info("PatientNode: Creating DiagnosisNode")
            return DiagnosisNode()
            
    class DiagnosisNode(BaseNode[Diagnosis]):
        async def run(self, ctx) -> 'SummaryNode':
            logger.info("DiagnosisNode: Creating SummaryNode")
            return SummaryNode()
            
    class SummaryNode(BaseNode[PatientSummary]):
        async def run(self, ctx) -> 'End[None]':
            logger.info("SummaryNode: Creating End node")
            return End(None)
    
    # Create graph from the nodes
    logger.info("Creating graph with nodes")
    graph = Graph(nodes=[PatientNode, DiagnosisNode, SummaryNode], name="Medical Analysis Flow")
    
    # Generate mermaid code
    logger.info("Generating mermaid code")
    try:
        mermaid_code = graph.mermaid_code(
            title="Medical Analysis Flow",
            edge_labels=True,
            notes=True
        )
        logger.info("Mermaid code generated successfully")
    
        # Generate graph image using mermaid.ink
        logger.info("Generating graph image using mermaid.ink")
        image_bytes = graph.mermaid_image(
            title="Medical Analysis Flow",
            edge_labels=True,
            notes=True,
            theme="default",
            format="png"
        )
        
        # Convert image bytes to base64 for HTML embedding
        import base64
        image_b64 = base64.b64encode(image_bytes).decode()
        
        return f"""
        <div style="width: 100%; text-align: center;">
            <img src="data:image/png;base64,{image_b64}" alt="Agent Interaction Graph" style="max-width: 100%; height: auto;">
        </div>
        """
    except Exception as e:
        logger.error(f"Error generating graph: {str(e)}")
        return f'<div class="error" style="color: red; padding: 10px;">Error generating graph: {str(e)}</div>'
