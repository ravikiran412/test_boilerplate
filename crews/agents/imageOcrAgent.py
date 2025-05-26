from crewai import Agent
from config.llm import LLMSelector
from crews.tools import extract_lead_from_business_card

openai_llm = LLMSelector(provider="openai").get_llm()

imageOcrAgent = Agent(
    role='Scanner',
    goal = f"You are an image OCR agent. Read images and extract content from the image at path `assets/lead.jpg`.",
    backstory='You are a data expert',
    llm=openai_llm,
    verbose=True,
    allow_delegation=False,
    tools=[extract_lead_from_business_card],
)