from typing import Any, Dict, List


def build_planner_prompt(
    user_text: str,
    emergency_type: str,
    severity: str,
    goals: List[str],
    info_gaps: List[str],
) -> str:
    """
    Return a textual representation of how the Planner is interpreting the situation.
    This is mostly for transparency and logging in the demo.
    """
    prompt = []
    prompt.append("SYSTEM: You are the Planner agent for an Emergency Response Guide Agent.")
    prompt.append("You must classify the emergency and decide appropriate goals and tools.")
    prompt.append("")
    prompt.append(f"User text: {user_text}")
    prompt.append(f"Detected emergency_type: {emergency_type}")
    prompt.append(f"Detected severity: {severity}")
    prompt.append(f"Goals: {', '.join(goals) if goals else 'none'}")
    prompt.append(f"Missing info (info_gaps): {', '.join(info_gaps) if info_gaps else 'none'}")
    return "\n".join(prompt)


def build_evaluator_prompt(
    emergency_type: str,
    severity: str,
    risk_score: int,
) -> str:
    """
    Return a textual representation of safety guidelines used by the Evaluator.

    In a real system this would be a detailed, carefully engineered prompt.
    """
    guideline_lines: List[str] = []
    guideline_lines.append("SYSTEM: You are the Evaluator agent.")
    guideline_lines.append("Your top priority is safety and clarity.")
    guideline_lines.append("Always encourage contacting local emergency services when risk is high.")
    guideline_lines.append("Never provide detailed medical diagnoses or prescribe medications.")
    guideline_lines.append("")
    guideline_lines.append(f"Emergency type: {emergency_type}")
    guideline_lines.append(f"Severity: {severity}")
    guideline_lines.append(f"Risk score: {risk_score}")
    guideline_lines.append("")
    guideline_lines.append("Checklist:")
    guideline_lines.append("- Is the advice practical and easy to follow?")
    guideline_lines.append("- Is the user encouraged to contact local emergency services when in doubt?")
    guideline_lines.append("- Are there any unsafe or speculative recommendations? If so, remove or soften them.")
    return "\n".join(guideline_lines)
