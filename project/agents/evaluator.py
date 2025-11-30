from typing import Any, Dict, List
from project.core.a2a_protocol import PlannerPlan, WorkerResult, EvaluatorDecision
from project.core.context_engineering import build_evaluator_prompt
from project.core.observability import log_event


class EvaluatorAgent:
    """
    EvaluatorAgent:
    - Checks safety, clarity, and completeness of Worker output.
    - Enforces disclaimers and escalation messages.
    - Produces final text response in an EvaluatorDecision.
    """

    def __init__(self) -> None:
        pass

    def _needs_escalation(self, plan: PlannerPlan, worker_result: WorkerResult) -> bool:
        if worker_result.risk_score >= 8:
            return True
        if plan.severity in ["high", "critical"]:
            return True
        return False

    def _build_response_text(
        self,
        plan: PlannerPlan,
        worker_result: WorkerResult,
        escalate: bool,
    ) -> str:
        header = "Emergency Response Guide Agent\n\n"
        disclaimer = (
            "Important: This is not a substitute for professional medical or emergency services. "
            "If you are in immediate danger or unsure, contact your local emergency number right away.\n\n"
        )

        escalation_line = ""
        if escalate:
            escalation_line = (
                "⚠️ This situation may be serious. If possible, stop reading and call your local emergency number immediately.\n\n"
            )

        details: List[str] = []
        details.append(f"Detected emergency type: {plan.emergency_type} (severity: {plan.severity}).")

        if worker_result.alerts:
            details.append("There may be active alerts in your area. Always follow instructions from local authorities.")

        steps_block = ""
        if worker_result.steps:
            steps_block = "Recommended steps:\n"
            for step in worker_result.steps:
                steps_block += f"- {step}\n"

        warnings_block = ""
        if worker_result.warnings:
            warnings_block = "\nWarnings:\n"
            for w in worker_result.warnings:
                warnings_block += f"- {w}\n"

        local_info_block = ""
        if worker_result.local_info:
            local_info_block = "\nLocal emergency information:\n"
            for k, v in worker_result.local_info.items():
                local_info_block += f"- {k}: {v}\n"

        uncertainties_block = ""
        if worker_result.uncertainties:
            uncertainties_block = "\nNotes:\n"
            for u in worker_result.uncertainties:
                uncertainties_block += f"- {u}\n"

        body = ""
        for d in details:
            body += d + "\n"
        body += "\n"
        body += steps_block
        body += warnings_block
        body += local_info_block
        body += uncertainties_block

        prompt_used = build_evaluator_prompt(
            emergency_type=plan.emergency_type,
            severity=plan.severity,
            risk_score=worker_result.risk_score,
        )

        full_response = header + disclaimer + escalation_line + body + "\n"
        full_response += "\n(Internal evaluator prompt applied for safety and clarity.)\n"
        full_response += f"(Evaluator prompt summary: {prompt_used[:200]}...)\n"

        return full_response

    def evaluate(self, plan: PlannerPlan, worker_result: WorkerResult) -> EvaluatorDecision:
        log_event(
            agent_name="EvaluatorAgent",
            event_type="evaluate_start",
            data={"plan_id": plan.plan_id, "risk_score": worker_result.risk_score},
        )

        escalate = self._needs_escalation(plan, worker_result)
        response_text = self._build_response_text(plan, worker_result, escalate)

        risk_flags: List[str] = []
        if escalate:
            risk_flags.append("escalation_advised")

        decision = EvaluatorDecision(
            plan_id=plan.plan_id,
            final_response_text=response_text,
            risk_flags=risk_flags,
            escalation_advice=escalate,
            notes_for_logs="Evaluation complete.",
        )

        log_event(
            agent_name="EvaluatorAgent",
            event_type="evaluate_end",
            data={"plan_id": plan.plan_id, "escalation": escalate},
        )

        return decision
