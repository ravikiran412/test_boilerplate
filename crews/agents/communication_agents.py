from crewai import Agent
from config.llm import LLMSelector
from crews.tools.communication_tools import get_communication, save_communication_summary

openai_llm = LLMSelector(provider="openai").get_llm()

sentimentAnalysisAgent = Agent(
    role="Sentiment Analyzer",
    goal="Analyze the emotional tone and sentiment of communication content",
    backstory=(
        "Expert in natural language processing and emotion detection in text. "
        "I analyze communications to detect emotional tone, urgency, and potential risks."
    ),
    llm=openai_llm,
    verbose=True,
    allow_delegation=False,
    tools=[get_communication]
)

featureExtractionAgent = Agent(
    role="Feature Extractor",
    goal="Extract key features, requirements, and action items from communication",
    backstory=(
        "Expert in identifying important points and actionable insights from conversations. "
        "I identify product features, requirements, and action items mentioned in communications."
    ),
    llm=openai_llm,
    verbose=True,
    allow_delegation=False,
    tools=[get_communication]
)

communicationSummaryAgent = Agent(
    role="Communication Summarizer",
    goal=(
        "Create comprehensive summaries of communications by combining sentiment analysis "
        "and feature extraction results into a structured format"
    ),
    backstory=(
        "Expert in distilling complex conversations into actionable summaries. "
        "I take the sentiment analysis and feature extraction results to create "
        "comprehensive summaries that highlight key points, risks, and action items."
    ),
    llm=openai_llm,
    verbose=True,
    allow_delegation=False,
    tools=[get_communication, save_communication_summary]
) 