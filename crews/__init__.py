from crewai import Crew
from crews.agents import imageOcrAgent, leadAgent
from crews.tasks import FormatLeadTask, ReadImgeOcr
from crews.agents.communication_agents import (
    sentimentAnalysisAgent,
    featureExtractionAgent,
    communicationSummaryAgent
)
from crews.tasks.communication_tasks import (
    AnalyzeSentimentTask,
    ExtractFeaturesTask,
    SummarizeCommunicationTask
)

leadProcessImagecrew = Crew(
    agents=[imageOcrAgent, leadAgent],
    tasks=[
         ReadImgeOcr, FormatLeadTask
        ],
    verbose=True
)
communicationAnalysisCrew = Crew(
    agents=[
        # sentimentAnalysisAgent,
        # featureExtractionAgent,
        communicationSummaryAgent
    ],
    tasks=[
        # AnalyzeSentimentTask,
        # ExtractFeaturesTask,
        SummarizeCommunicationTask
    ],
    verbose=True
) 
__all__ = ["leadProcessImagecrew", "communicationAnalysisCrew"]