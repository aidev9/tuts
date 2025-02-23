import logging
import base64
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Annotated, Optional, Any, Union
from pydantic import BaseModel
from pydantic_graph import Graph, BaseNode, End, Edge, GraphRunContext

from patient import PatientCase
from agents.base import Diagnosis
from agents.summary import PatientSummary, SummaryAgent
from agents.medical.cardiology import CardiologyAgent
from agents.medical.neurology import NeurologyAgent
from agents.medical.gastroenterology import GastroenterologyAgent
from agents.medical.psychotherapy import PsychotherapyAgent
from agents.medical.pulmonology import PulmonologyAgent
from agents.medical.endocrinology import EndocrinologyAgent
from agents.medical.orthopedics import OrthopedicsAgent
from agents.medical.immunology import ImmunologyAgent
from agents.medical.dermatology import DermatologyAgent
from agents.medical.emergency import EmergencyAgent
from agents.selector import AgentSelector

logger = logging.getLogger(__name__)


specialists = {
    "cardiology": CardiologyAgent,
    "neurology": NeurologyAgent,
    "gastroenterology": GastroenterologyAgent,
    "psychotherapy": PsychotherapyAgent,
    "pulmonology": PulmonologyAgent,
    "endocrinology": EndocrinologyAgent,
    "orthopedics": OrthopedicsAgent,
    "immunology": ImmunologyAgent,
    "dermatology": DermatologyAgent,
    "emergency": EmergencyAgent,
}


class AnalysisStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class SpecialistResult:
    specialty: str
    diagnosis: Optional[Diagnosis] = None
    error: Optional[str] = None
    status: AnalysisStatus = AnalysisStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class GraphState:
    """Enhanced state tracking for medical analysis workflow"""

    patient: PatientCase
    specialist_results: Dict[str, SpecialistResult] = field(default_factory=dict)
    selected_specialties: List[str] = field(default_factory=list)
    summary: Optional[PatientSummary] = None
    workflow_start: datetime = field(default_factory=datetime.now)
    workflow_end: Optional[datetime] = None
    error: Optional[str] = None


class SummaryAnalysis(BaseModel):
    """Final analysis result including timing information"""

    patient: PatientCase
    specialist_results: Dict[str, SpecialistResult]
    summary: PatientSummary
    total_duration: float  # seconds


@dataclass
class PatientIntakeNode(BaseNode[GraphState]):
    """Initialize analysis workflow and validate patient data"""

    docstring_notes = True

    async def run(
        self, ctx: GraphRunContext[GraphState]
    ) -> "SpecialistsCoordinatorNode":
        logger.info(
            f"Starting analysis for patient {ctx.state.patient.name} (ID: {ctx.state.patient.patient_id})"
        )

        # Initialize specialist results (will be populated dynamically)
        ctx.state.specialist_results = {}

        return SpecialistsCoordinatorNode()


@dataclass
class ValidationNode(BaseNode[GraphState]):
    """Validate all specialist analyses completed successfully"""

    docstring_notes = True

    async def run(
        self, ctx: GraphRunContext[GraphState]
    ) -> Union["SummaryNode", "ErrorNode"]:
        # Check for any failed analyses in the dynamically selected specialists
        errors = []
        for specialty, result in ctx.state.specialist_results.items():
            if result.status == AnalysisStatus.ERROR:
                errors.append(f"{specialty}: {result.error}")

        if errors:
            ctx.state.error = "Specialist analysis errors:\n" + "\n".join(errors)
            return ErrorNode()

        return SummaryNode()


@dataclass
class ErrorNode(BaseNode[GraphState]):
    """Handle workflow errors gracefully"""

    docstring_notes = True

    async def run(self, ctx: GraphRunContext[GraphState]) -> End[SummaryAnalysis]:
        logger.error(f"Workflow error: {ctx.state.error}")
        ctx.state.workflow_end = datetime.now()
        duration = (ctx.state.workflow_end - ctx.state.workflow_start).total_seconds()

        return End(
            SummaryAnalysis(
                patient=ctx.state.patient,
                specialist_results=ctx.state.specialist_results,
                summary=None,  # No summary on error
                total_duration=duration,
            )
        )


@dataclass
class SummaryNode(BaseNode[GraphState]):
    """Generate final patient summary"""

    docstring_notes = True
    agent = SummaryAgent()

    async def run(self, ctx: GraphRunContext[GraphState]) -> End[SummaryAnalysis]:
        logger.info("Generating final summary")
        try:
            # Get successful diagnoses
            diagnoses = [
                result.diagnosis
                for result in ctx.state.specialist_results.values()
                if result.diagnosis is not None
            ]

            summary = await self.agent.create_summary(ctx.state.patient, diagnoses)
            ctx.state.summary = summary

        except Exception as e:
            ctx.state.error = f"Summary generation error: {str(e)}"
            ctx.state.summary = None

        finally:
            ctx.state.workflow_end = datetime.now()
            duration = (
                ctx.state.workflow_end - ctx.state.workflow_start
            ).total_seconds()

            return End(
                SummaryAnalysis(
                    patient=ctx.state.patient,
                    specialist_results=ctx.state.specialist_results,
                    summary=ctx.state.summary,
                    total_duration=duration,
                )
            )


@dataclass
class SpecialistsCoordinatorNode(BaseNode[GraphState]):
    """Select relevant specialists and run analyses concurrently"""

    docstring_notes = True
    selector = AgentSelector()
    
    
    available_specialties = list(specialists.keys())

    async def run(
        self, ctx: GraphRunContext[GraphState]
    ) -> Union["ValidationNode", "ErrorNode"]:
        try:
            # Select relevant specialties
            selected_specialties = await self.selector.select_specialties(
                ctx.state.patient
            )
            logger.info(f"Selected specialties: {selected_specialties}")

            # Populate the selected specialties in the graph state
            ctx.state.selected_specialties = selected_specialties

            tasks = []
            for specialty in selected_specialties:
                if specialty in specialists:
                    agent_class = specialists[specialty]
                    agent = agent_class()
                    ctx.state.specialist_results[specialty] = SpecialistResult(
                        specialty=specialty
                    )
                    result = ctx.state.specialist_results[specialty]
                    result.status = AnalysisStatus.IN_PROGRESS
                    result.start_time = datetime.now()
                    tasks.append(self.analyze_specialty(specialty, agent, ctx))
                else:
                    logger.warning(f"Unknown specialty selected: {specialty}")

            # Run selected analyses sequentially
            for task in tasks:
                await task

            return ValidationNode()

        except Exception as e:
            ctx.state.error = f"Error in smart selection: {str(e)}"
            return ErrorNode()

    async def analyze_specialty(
        self, specialty: str, agent: Any, ctx: GraphRunContext[GraphState]
    ):
        """Run analysis for a single specialty"""
        result = ctx.state.specialist_results[specialty]
        try:
            diagnosis = await agent.analyze(ctx.state.patient)
            result.diagnosis = diagnosis
            result.status = AnalysisStatus.COMPLETED
        except Exception as e:
            result.error = str(e)
            result.status = AnalysisStatus.ERROR
        finally:
            result.end_time = datetime.now()


def generate_graph(
    state: GraphState, highlighted_nodes: Optional[List[str]] = None
) -> str:
    """Generate visualization of the medical analysis workflow"""
    try:
        logger.info("Generating workflow visualization")

        # Define nodes for the graph, including all specialty nodes
        nodes = {
            PatientIntakeNode,
            SpecialistsCoordinatorNode,
            ValidationNode,
            SummaryNode,
            ErrorNode,
        }

        # Create the graph with all nodes
        graph = Graph(nodes=nodes, name="Medical Analysis Workflow")

        image_bytes = graph.mermaid_image(
            title="Smart Medical Analysis Workflow",
            edge_labels=True,
            theme="default",
            format="png",
            direction="LR",
            highlighted_nodes=highlighted_nodes,
        )

        image_b64 = base64.b64encode(image_bytes).decode()
        logger.info("Workflow visualization generated successfully")
        return f'<div style="width: 90%; text-align: center;"><img src="data:image/png;base64,{image_b64}" alt="Analysis Workflow" style="max-width: 100%; height: auto;"></div>'

    except Exception as e:
        logger.error(f"Graph generation error: {str(e)}")
        return f'<div style="color: red; padding: 10px;">Failed to generate graph: {str(e)}</div>'
