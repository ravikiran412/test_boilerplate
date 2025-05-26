from crewai import Task
from crews.agents import leadAgent

FormatLeadTask = Task(
    description=(
        "Parse the raw OCR text and output structured lead data fields "
        "(first name, last name, email, mobile, phone, organization, job, description, lead status=New)."
        "Make sure to check with a human till the output json is properly structured and info has proper value"
        "Update manual value updated by the user"
    ),
    tools=[],
    agent=leadAgent,
    expected_output="Structured lead details only with valid values",
    # human_input=True 
)