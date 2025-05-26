from datetime import datetime
from database import db
from database.models import Lead
import random

async def seed_leads(company_ids):
    """Seed the leads collection with initial data"""
    try:
        leads_collection = db.get_db().leads
        employees_collection = db.get_db().employees
        
        # Get all employees for lead ownership
        employees = await employees_collection.find().to_list(length=None)
        if not employees:
            print("No employees found. Please seed employees first.")
            return []
        
        # Sample lead data
        leads = []
        for company_id in company_ids:
            # Create 3-5 leads per company
            num_leads = random.randint(3, 5)
            for _ in range(num_leads):
                # Convert ObjectId to string for company_id
                company_id_str = str(company_id)
                # Select random employee for lead ownership
                employee = random.choice(employees)
                employee_id_str = str(employee["_id"])
                
                lead = Lead(
                    first_name=random.choice(["John", "Jane", "Michael", "Sarah", "David", "Emily"]),
                    last_name=random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]),
                    email=f"{random.choice(['john', 'jane', 'mike', 'sarah', 'david', 'emily'])}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])}",
                    phone=f"+1{random.randint(2000000000, 9999999999)}",
                    job_title=random.choice(["CEO", "CTO", "CFO", "COO", "VP Sales", "Director", "Manager"]),
                    company_id=company_id_str,
                    lead_source=random.choice(["website", "referral", "social_media", "email_campaign"]),
                    lead_owner_id=employee_id_str,
                    status=random.choice(["new", "contacted", "qualified", "unqualified"]),
                    score=random.uniform(0, 1),  # 0-1 scale as per model
                    priority=random.uniform(0, 1),  # 0-1 scale as per model
                    predicted_value=random.uniform(1000, 100000),
                    enrichment_data={}  # Empty dict as per model
                )
                leads.append(lead)
        
        if not leads:
            print("No leads created. Check company_ids and employee data.")
            return []
            
        # Clear existing data
        await leads_collection.delete_many({})
        
        # Insert new data
        result = await leads_collection.insert_many([lead.model_dump() for lead in leads])
        print(f"Successfully seeded {len(result.inserted_ids)} leads")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding leads: {str(e)}")
        return [] 