from crewai import Task
from crews.agents.communication_agents import (
    sentimentAnalysisAgent,
    featureExtractionAgent,
    communicationSummaryAgent
)
from crews.tools.communication_tools import get_communication, save_communication_summary

AnalyzeSentimentTask = Task(
    description=(
        "Analyze the sentiment and emotional tone of the communication content. "
        "Identify overall mood, urgency, and concerning patterns."
    ),
    agent=sentimentAnalysisAgent,
    tools=[get_communication],
    expected_output="Sentiment analysis with tone, emotions, urgency, and risks"
)

ExtractFeaturesTask = Task(
    description=(
        "Extract key features, requirements, and action items from the communication. "
        "Identify product features, requirements, and future needs."
    ),
    agent=featureExtractionAgent,
    tools=[get_communication],
    expected_output="List of features, requirements, action items, and follow-up points"
)

SummarizeCommunicationTask = Task(
    description=(
        "Create a comprehensive summary of the communication with sentiment and features. "
        "Save the summary with the communication ID."
    ),
    agent=communicationSummaryAgent,
    tools=[get_communication, save_communication_summary],
    expected_output="Comprehensive summary with user intent, tone, quotes, actions, and risks"
) 