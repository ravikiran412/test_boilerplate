from crewai.tools import tool
from database import db
from bson import ObjectId
from typing import Union, List

async def fetch_lead_data(lead_id: Union[str, List[str]]) -> dict:
    """
    Fetches lead data from MongoDB based on lead ID(s).
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Lead data including company details
    """
    try:
        leads_collection = db.get_db().leads
        companies_collection = db.get_db().companies
        
        # Convert single ID to list for uniform processing
        if isinstance(lead_id, str):
            lead_id = [lead_id]
            
        # Convert string IDs to ObjectId
        lead_ids = [ObjectId(id) for id in lead_id]
        
        # Fetch leads
        leads = await leads_collection.find({"_id": {"$in": lead_ids}}).to_list(length=None)
        
        if not leads:
            return {"error": "No leads found"}
            
        # Fetch company details for each lead
        for lead in leads:
            if "company_id" in lead:
                company = await companies_collection.find_one({"_id": ObjectId(lead["company_id"])})
                if company:
                    lead["company"] = company
                    
        return {"leads": leads}
    except Exception as e:
        return {"error": f"Error fetching lead data: {str(e)}"}

@tool("get lead data")
async def get_lead_data(lead_id: Union[str, List[str]]) -> dict:
    """
    CrewAI tool to fetch lead data from MongoDB based on lead ID(s).
    
    Args:
        lead_id (Union[str, List[str]]): Single lead ID or list of lead IDs
        
    Returns:
        dict: Lead data including company details
    """
    return await fetch_lead_data(lead_id) 