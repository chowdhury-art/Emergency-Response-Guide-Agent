from typing import Any, Dict, List
from project.core.a2a_protocol import PlannerPlan, WorkerResult
from project.core.observability import log_event
from project.tools.tools import (
    get_emergency_protocol,
    get_local_emergency_contacts,
    get_disaster_alerts,
    summarize_protocol,
    compute_risk_score,
)


class WorkerAgent:
    """
    WorkerAgent:
    - Executes the Planner's plan.
    - Calls tools to fetch protocols, local info, and alerts.
    - Produces a structured WorkerResult.
    """

    def __init__(self) -> None:
        pass

    def work(self, plan: PlannerPlan) -> WorkerResult:
        log_event(
            agent_name="WorkerAgent",
            event_type="work_start",
            data={"plan_id": plan.plan_id, "emergency_type": plan.emergency_type},
        )

        session_region = plan.session_summary_snapshot.get("region", "global")
        session_language = plan.session_summary_snapshot.get("language", "en")

        protocol_text = ""
        local_info: Dict[str, Any] = {}
        alerts: List[Dict[str, Any]] = []
        warnings: List[str] = []
        uncertainties: List[str] = []

        if "get_emergency_protocol" in plan.tools_to_call:
            protocol_text = get_emergency_protocol(
                emergency_type=plan.emergency_type,
                severity=plan.severity,
                region=session_region,
                language=session_language,
            )

        if "get_local_emergency_contacts" in plan.tools_to_call:
            local_info = get_local_emergency_contacts(region=session_region)

        if "get_disaster_alerts" in plan.tools_to_call:
            alerts = get_disaster_alerts(region=session_region, emergency_type=plan.emergency_type)

        risk_score = compute_risk_score(
            emergency_type=plan.emergency_type,
            severity=plan.severity,
        )

        summarized_steps = summarize_protocol(protocol_text, max_steps=7)

        if risk_score >= 8:
            warnings.append(
                "This situation appears potentially life-threatening. Call your local emergency number immediately if you can."
            )

        if not protocol_text:
            uncertainties.append(
                "Could not find a specific protocol for this situation. Providing general safety guidance only."
            )

        steps: List[str] = []
        for i, step in enumerate(summarized_steps, start=1):
            steps.append(f"Step {i}: {step}")

        if not steps:
            steps.append(
                "Stay as safe as possible, move away from immediate danger if you can do so safely, and contact local emergency services."
            )

        result = WorkerResult(
            plan_id=plan.plan_id,
            steps=steps,
            warnings=warnings,
            local_info=local_info,
            alerts=alerts,
            source_protocols=["default_knowledge_base"],
            uncertainties=uncertainties,
            risk_score=risk_score,
        )

        log_event(
            agent_name="WorkerAgent",
            event_type="work_end",
            data={
                "plan_id": plan.plan_id,
                "num_steps": len(steps),
                "risk_score": risk_score,
                "has_alerts": bool(alerts),
            },
        )

        return result
