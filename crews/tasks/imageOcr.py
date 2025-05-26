from crewai import Task
from crews.agents import imageOcrAgent
from crews.tools import extract_lead_from_business_card

ReadImgeOcr = Task(
    description=(
        "Analyse and give a report"
        "Make sure to check with a human if the draft is good before finalizing your answer."
        ),
    tools=[extract_lead_from_business_card],
    agent=imageOcrAgent,
    expected_output='Give a comprehensive full report on the given context',
    # human_input=True
)