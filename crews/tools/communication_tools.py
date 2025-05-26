from crewai.tools import tool
from database import db
from bson import ObjectId
from typing import Dict, Any

@tool("get communication")
async def get_communication(communication_id: str) -> Dict[str, Any]:
    """
    Get communication details by ID from the database
    
    Args:
        communication_id (str): The ID of the communication to retrieve
        
    Returns:
        Dict[str, Any]: The communication details
    """
    try:
        print(communication_id, "communication_id")
        communications_collection = db.get_db().communications
        communication = await communications_collection.find_one({"_id": ObjectId(communication_id)})
        if not communication:
            raise ValueError(f"Communication with ID {communication_id} not found")
        return communication
    except Exception as e:
        raise Exception(f"Error fetching communication: {str(e)}")

@tool("save communication summary")
async def save_communication_summary(communication_id: str, summary_data: Dict[str, Any]) -> bool:
    """
    Save communication summary to the database
    
    Args:
        communication_id (str): The ID of the communication
        summary_data (Dict[str, Any]): The summary data to save
        
    Returns:
        bool: True if save was successful
    """
    try:
        summaries_collection = db.get_db().communication_summaries
        summary_data["communication_id"] = communication_id
        result = await summaries_collection.insert_one(summary_data)
        return bool(result.inserted_id)
    except Exception as e:
        raise Exception(f"Error saving communication summary: {str(e)}")

# Export the tools
__all__ = ["get_communication", "save_communication_summary"] 