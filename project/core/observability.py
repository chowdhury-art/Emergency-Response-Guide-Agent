from typing import Any, Dict
import json
import time
import sys


def log_event(agent_name: str, event_type: str, data: Dict[str, Any], severity: str = "info") -> None:
    """
    Simple JSON logging to stdout.
    This is lightweight but demonstrates observability.
    """
    log_record = {
        "timestamp": time.time(),
        "agent": agent_name,
        "event_type": event_type,
        "severity": severity,
        "data": data,
    }
    try:
        sys.stdout.write(json.dumps(log_record) + "\n")
    except Exception:
        # Fallback to plain print if JSON serialization fails
        print(f"[LOG][{agent_name}][{event_type}] {data}")
