from crewai.tools import tool
from database import db
from bson import ObjectId
from typing import Union, List

async def fetch_lead_communications(lead_id: Union[str, List[str]]) -> dict:
    """
    Fetches communication data for lead(s) from MongoDB.
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Communication data including summaries
    """
    try:
        communications_collection = db.get_db().communications
        summaries_collection = db.get_db().communication_summaries
        
        # Convert single ID to list for uniform processing
        if isinstance(lead_id, str):
            lead_id = [lead_id]
            
        # Fetch all communications in a single query using $in operator
        communications = await communications_collection.find({"lead_id": {"$in": lead_id}}).to_list(length=None)
        
        if not communications:
            return {"error": "No communications found"}
            
        # Fetch summaries for each communication
        for comm in communications:
            if "summary_id" in comm:
                summary = await summaries_collection.find_one({"_id": ObjectId(comm["summary_id"])})
                if summary:
                    comm["summary"] = summary
                    
        return {"communications": communications}
    except Exception as e:
        return {"error": f"Error fetching communications: {str(e)}"}

@tool("get lead communications")
async def get_lead_communications(lead_id: Union[str, List[str]]) -> dict:
    """
    CrewAI tool to fetch communication data for lead(s).
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Communication data
    """
    return await fetch_lead_communications(lead_id) 