from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class UserMessage:
    user_id: str
    session_id: str
    text: str
    timestamp: float
    metadata: Dict[str, Any]


@dataclass
class PlannerPlan:
    plan_id: str
    emergency_type: str
    severity: str
    goals: List[str]
    info_gaps: List[str]
    tools_to_call: List[str]
    desired_output_format: str
    session_summary_snapshot: Dict[str, Any]
    raw_prompt: str


@dataclass
class WorkerResult:
    plan_id: str
    steps: List[str]
    warnings: List[str]
    local_info: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    source_protocols: List[str]
    uncertainties: List[str]
    risk_score: int


@dataclass
class EvaluatorDecision:
    plan_id: str
    final_response_text: str
    risk_flags: List[str]
    escalation_advice: bool
    notes_for_logs: str
