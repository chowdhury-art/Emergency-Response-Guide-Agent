from typing import Any, Dict
from project.core.a2a_protocol import UserMessage, PlannerPlan
from project.core.context_engineering import build_planner_prompt
from project.core.observability import log_event


class PlannerAgent:
    """
    PlannerAgent:
    - Classifies emergency type and severity.
    - Decides high-level goals.
    - Chooses which tools the Worker should call.
    - Produces a structured PlannerPlan.
    """

    def __init__(self) -> None:
        pass

    def _simple_classify(self, user_text: str) -> Dict[str, Any]:
        text = user_text.lower()
        emergency_type = "general"
        severity = "low"

        if any(k in text for k in ["bleeding", "unconscious", "heart", "chest pain", "can't breathe", "cannot breathe", "not breathing"]):
            emergency_type = "medical"
            severity = "critical"
        elif any(k in text for k in ["fire", "smoke", "burning"]):
            emergency_type = "fire"
            severity = "high"
        elif any(k in text for k in ["earthquake", "tremor", "shaking"]):
            emergency_type = "earthquake"
            severity = "high"
        elif any(k in text for k in ["flood", "water rising", "flash flood"]):
            emergency_type = "flood"
            severity = "high"
        elif any(k in text for k in ["storm", "hurricane", "tornado", "cyclone"]):
            emergency_type = "storm"
            severity = "high"

        if any(k in text for k in ["urgent", "emergency", "help now"]):
            if severity == "low":
                severity = "high"

        return {
            "emergency_type": emergency_type,
            "severity": severity,
        }

    def plan(self, user_message: UserMessage, session_summary: Dict[str, Any]) -> PlannerPlan:
        """
        Produce a PlannerPlan from a UserMessage and existing session summary.
        """
        log_event(
            agent_name="PlannerAgent",
            event_type="plan_start",
            data={"session_id": user_message.session_id, "text": user_message.text},
        )

        classification = self._simple_classify(user_message.text)
        emergency_type = classification["emergency_type"]
        severity = classification["severity"]

        # Simple rule-based goals and tools
        goals = []
        tools_to_call = []

        if emergency_type == "medical":
            goals.append("provide_first_aid_steps")
            tools_to_call.append("get_emergency_protocol")
            tools_to_call.append("get_local_emergency_contacts")
        elif emergency_type in ["fire", "earthquake", "flood", "storm"]:
            goals.append("provide_safety_and_evacuation_steps")
            tools_to_call.append("get_emergency_protocol")
            tools_to_call.append("get_local_emergency_contacts")
            tools_to_call.append("get_disaster_alerts")
        else:
            goals.append("provide_general_safety_guidance")
            tools_to_call.append("get_emergency_protocol")
            tools_to_call.append("get_local_emergency_contacts")

        desired_output_format = "numbered_steps"

        info_gaps = []
        if not session_summary.get("region"):
            info_gaps.append("region")
        if not session_summary.get("language"):
            info_gaps.append("language")

        prompt = build_planner_prompt(
            user_text=user_message.text,
            emergency_type=emergency_type,
            severity=severity,
            goals=goals,
            info_gaps=info_gaps,
        )

        plan = PlannerPlan(
            plan_id=f"plan-{user_message.session_id}",
            emergency_type=emergency_type,
            severity=severity,
            goals=goals,
            info_gaps=info_gaps,
            tools_to_call=tools_to_call,
            desired_output_format=desired_output_format,
            session_summary_snapshot=session_summary,
            raw_prompt=prompt,
        )

        log_event(
            agent_name="PlannerAgent",
            event_type="plan_end",
            data={
                "session_id": user_message.session_id,
                "plan_id": plan.plan_id,
                "emergency_type": emergency_type,
                "severity": severity,
                "goals": goals,
                "tools_to_call": tools_to_call,
            },
        )

        return plan
