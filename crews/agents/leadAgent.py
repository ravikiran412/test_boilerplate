from crewai import Agent
from config.llm import LLMSelector
from crews.tools import extract_lead_from_business_card
openai_llm = LLMSelector(provider="openai").get_llm()

leadAgent = Agent(
    role="Lead Formatter",
    goal="Given raw OCR text from a business card, extract structured lead info: first name, last name, email, mobile, phone, organization, job, description, lead status (default New).",
    backstory="Expert in extracting structured lead data from unstructured text",
    llm=openai_llm,
    verbose=True,
    allow_delegation=False,
    tools=[extract_lead_from_business_card] 
)
