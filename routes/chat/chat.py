from fastapi import APIRouter
from pydantic import BaseModel
from crews import leadProcessImagecrew
from config import setup_logger
from datetime import datetime

crew_logger = setup_logger('crewai', 'logs/crewai.log')

class InputData(BaseModel):
    text: str
    
router = APIRouter()

@router.post("/")
async def chat_handler(data: InputData):
    # Placeholder for LangChain processing
    crew_logger.info("Starting CrewAI execution with input: %s", datetime.now())
    result = leadProcessImagecrew.kickoff()  # if kickoff expects input text
    crew_logger.info("CrewAI result: %s", result)
    
    # Return the result as JSON response
    return {"result": result}
