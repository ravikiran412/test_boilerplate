import asyncio
from crews.tools.lead_data import fetch_lead_data
from crews.tools.lead_communications import fetch_lead_communications
from crews.tools.lead_activities import fetch_lead_activities
from . import leadProcessImagecrew, communicationAnalysisCrew
from database import db
import os

async def test_tools():
    # Initialize database connection
    await db.connect_db()
    
    try:
        # Get actual lead IDs from the database
        leads_collection = db.get_db().leads
        leads = await leads_collection.find().limit(2).to_list(length=None)
        
        if not leads:
            print("No leads found in the database. Please run the seeders first.")
            return
            
        lead_ids = [str(lead["_id"]) for lead in leads]
        print(f"\nTesting with lead IDs: {lead_ids}")
        
        print("\nTesting fetch_lead_data:")
        lead_data = await fetch_lead_data(lead_ids)
        print(lead_data)
        
        print("\nTesting fetch_lead_communications:")
        communications = await fetch_lead_communications(lead_ids)
        print(communications)
        
        print("\nTesting fetch_lead_activities:")
        activities = await fetch_lead_activities(lead_ids)
        print(activities)
    finally:
        # Close database connection
        await db.close_db()

if __name__ == "__main__":
    # asyncio.run(test_tools())
    # print(leadProcessImagecrew.kickoff())
    inputs = {
        'commuication_id': '683406eff75abdca9e790d14'
    }
    result = communicationAnalysisCrew.kickoff(inputs)
    print(result)
