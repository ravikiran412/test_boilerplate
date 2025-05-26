from datetime import datetime
from database import db
from database.models import Employee
import random

async def seed_employees():
    """Seed the employees collection with initial data"""
    try:
        employees_collection = db.get_db().employees
        
        # Sample employee data
        employees = [
            Employee(
                first_name="Sarah",
                last_name="Johnson",
                email="sarah.johnson@company.com",
                role="Sales Representative",
                department="Sales",
                workload=0.0,
                max_leads=10
            ),
            Employee(
                first_name="Michael",
                last_name="Chen",
                email="michael.chen@company.com",
                role="Senior Sales Representative",
                department="Sales",
                workload=0.0,
                max_leads=15
            ),
            Employee(
                first_name="Emily",
                last_name="Rodriguez",
                email="emily.rodriguez@company.com",
                role="Sales Manager",
                department="Sales",
                workload=0.0,
                max_leads=20
            ),
            Employee(
                first_name="David",
                last_name="Kim",
                email="david.kim@company.com",
                role="Sales Representative",
                department="Sales",
                workload=0.0,
                max_leads=10
            ),
            Employee(
                first_name="Lisa",
                last_name="Patel",
                email="lisa.patel@company.com",
                role="Senior Sales Representative",
                department="Sales",
                workload=0.0,
                max_leads=15
            )
        ]
        
        # Clear existing data
        await employees_collection.delete_many({})
        
        # Insert new data
        result = await employees_collection.insert_many([employee.model_dump() for employee in employees])
        print(f"Successfully seeded {len(result.inserted_ids)} employees")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding employees: {str(e)}")
        return [] 