from crewai import Crew
from crews.agents import imageOcrAgent, leadAgent
from crews.tasks import FormatLeadTask, ReadImgeOcr

leadProcessImagecrew = Crew(
    agents=[imageOcrAgent, leadAgent],
    tasks=[
         ReadImgeOcr, FormatLeadTask
        ]
)

__all__ = ["leadProcessImagecrew"]