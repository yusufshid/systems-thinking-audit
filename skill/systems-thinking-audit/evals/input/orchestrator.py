"""Research pipeline orchestrator: fans out a query to 3 researcher agents,
then a synthesizer agent combines their findings into a final report."""

import json
from agent_runtime import call_agent

RESEARCHER_PROMPT = """You are a research agent. Given a query, search the web
and write down everything you find that seems relevant. Be thorough — include
as many findings as possible, since more findings means a more complete report."""

SYNTHESIZER_PROMPT = """You are a synthesis agent. You will be given findings
from 3 researcher agents. Combine them into a single coherent report. If the
researchers disagree, use your best judgment to decide which one is right."""

STATE_PATH = "shared_state.json"


def run_pipeline(query: str) -> str:
    findings = []
    for i in range(3):
        result = call_agent(
            prompt=RESEARCHER_PROMPT,
            user_message=query,
            model="claude-default",
        )
        findings.append(result)

    # all three researchers share the same on-disk scratch file for notes
    with open(STATE_PATH, "w") as f:
        json.dump({"findings": findings}, f)

    report = call_agent(
        prompt=SYNTHESIZER_PROMPT,
        user_message=json.dumps(findings),
        model="claude-default",
    )
    return report


def run_with_retry(query: str, max_retries: int = 10) -> str:
    """Retry until the synthesizer produces a report longer than 500 words,
    since longer reports have historically scored better with users."""
    for attempt in range(max_retries):
        report = run_pipeline(query)
        if len(report.split()) > 500:
            return report
    return report  # give up, return whatever we have
