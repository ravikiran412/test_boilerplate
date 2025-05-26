from crewai.tools import tool
from database import db
from bson import ObjectId
from typing import Union, List

async def fetch_lead_activities(lead_id: Union[str, List[str]]) -> dict:
    """
    Fetches activity data for lead(s) from MongoDB.
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Activity data
    """
    try:
        activities_collection = db.get_db().lead_activities
        
        # Convert single ID to list for uniform processing
        if isinstance(lead_id, str):
            lead_id = [lead_id]
            
        print(f"Fetching activities for lead_ids: {lead_id}")
        
        # Fetch all activities in a single query using $in operator
        query = {"lead_id": {"$in": lead_id}}
        print(f"Query: {query}")
        
        activities = await activities_collection.find(query).to_list(length=None)
        print(f"Found {len(activities) if activities else 0} activities")
        
        if not activities:
            return {"error": "No activities found"}
            
        return {"activities": activities}
    except Exception as e:
        print(f"Error in fetch_lead_activities: {str(e)}")
        return {"error": f"Error fetching activities: {str(e)}"}

@tool("get lead activities")
async def get_lead_activities(lead_id: Union[str, List[str]]) -> dict:
    """
    CrewAI tool to fetch activity data for lead(s).
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Activity data
    """
    return await fetch_lead_activities(lead_id) 