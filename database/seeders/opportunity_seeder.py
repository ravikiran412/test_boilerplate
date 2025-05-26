from datetime import datetime, timedelta
from database import db
from database.models import Opportunity
import random

async def seed_opportunities(lead_ids):
    """Seed the opportunities collection with initial data"""
    try:
        opportunities_collection = db.get_db().opportunities
        
        if not lead_ids:
            print("No lead_ids provided. Please seed leads first.")
            return []
        
        # Sample opportunity data
        opportunities = []
        for lead_id in lead_ids:
            # Only create opportunities for some leads (30% chance)
            if random.random() < 0.3:
                # Generate a random close date within the next 90 days
                expected_close_date = datetime.utcnow() + timedelta(days=random.randint(1, 90))
                
                opportunity = Opportunity(
                    lead_id=str(lead_id),
                    value=random.uniform(1000, 100000),
                    stage=random.choice(["discovery", "proposal", "negotiation", "closed_won", "closed_lost"]),
                    probability=random.uniform(0, 1),
                    expected_close_date=expected_close_date,
                    created_at=datetime.utcnow()
                )
                opportunities.append(opportunity)
        
        if not opportunities:
            print("No opportunities created. Check lead_ids.")
            return []
            
        # Clear existing data
        await opportunities_collection.delete_many({})
        
        # Insert new data
        result = await opportunities_collection.insert_many([opp.model_dump() for opp in opportunities])
        print(f"Successfully seeded {len(result.inserted_ids)} opportunities")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding opportunities: {str(e)}")
        return [] 