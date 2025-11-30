import time
from typing import Any, Dict

from project.agents.planner import PlannerAgent
from project.agents.worker import WorkerAgent
from project.agents.evaluator import EvaluatorAgent
from project.core.a2a_protocol import UserMessage
from project.core.observability import log_event
from project.memory.session_memory import GLOBAL_SESSION_MEMORY


class MainAgent:
    """
    Orchestrates Planner -> Worker -> Evaluator.
    """

    def __init__(self, user_id: str = "demo_user") -> None:
        self.user_id = user_id
        self.planner = PlannerAgent()
        self.worker = WorkerAgent()
        self.evaluator = EvaluatorAgent()

    def handle_message(self, user_input: str, session_id: str = "default_session") -> Dict[str, Any]:
        timestamp = time.time()
        session_summary = GLOBAL_SESSION_MEMORY.get_session_summary(session_id)
        GLOBAL_SESSION_MEMORY.set_default_region_if_missing(session_id)
        GLOBAL_SESSION_MEMORY.set_default_language_if_missing(session_id)

        user_message = UserMessage(
            user_id=self.user_id,
            session_id=session_id,
            text=user_input,
            timestamp=timestamp,
            metadata={},
        )

        log_event(
            agent_name="MainAgent",
            event_type="handle_message_start",
            data={"session_id": session_id, "text": user_input},
        )

        plan = self.planner.plan(user_message=user_message, session_summary=session_summary)
        worker_result = self.worker.work(plan=plan)
        decision = self.evaluator.evaluate(plan=plan, worker_result=worker_result)

        GLOBAL_SESSION_MEMORY.update_session_summary(
            session_id,
            {
                "last_emergency_type": plan.emergency_type,
                "last_severity": plan.severity,
                "last_risk_score": worker_result.risk_score,
            },
        )

        log_event(
            agent_name="MainAgent",
            event_type="handle_message_end",
            data={
                "session_id": session_id,
                "plan_id": plan.plan_id,
                "risk_flags": decision.risk_flags,
            },
        )

        return {
            "response": decision.final_response_text,
            "risk_flags": decision.risk_flags,
            "escalation_advice": decision.escalation_advice,
        }


def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
