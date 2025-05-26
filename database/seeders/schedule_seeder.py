from datetime import datetime, timedelta
from database import db
from database.models import Schedule
import random

async def seed_schedules(lead_ids, employee_ids):
    """Seed the schedules collection with initial data"""
    try:
        schedules_collection = db.get_db().schedules
        schedules = []
        
        for lead_id in lead_ids:
            # Get employee with lowest workload
            employees = await db.get_db().employees.find().to_list(length=None)
            if not employees:
                continue
                
            # Sort by workload and select employee
            employees.sort(key=lambda x: x.get("workload", 0))
            employee = employees[0]
            
            # Create schedule for next 7 days
            start_time = datetime.utcnow() + timedelta(days=random.randint(1, 7))
            duration = random.randint(30, 120)  # 30 mins to 2 hours
            
            schedule = Schedule(
                employee_id=str(employee["_id"]),
                lead_id=str(lead_id),
                start_time=start_time,
                end_time=start_time + timedelta(minutes=duration),
                activity_type=random.choice([
                    "initial_contact",
                    "follow_up",
                    "demo",
                    "negotiation",
                    "closing"
                ]),
                status="scheduled"
            )
            schedules.append(schedule)
            
            # Update employee workload
            await db.get_db().employees.update_one(
                {"_id": employee["_id"]},
                {"$inc": {"workload": 0.1}}  # Increase workload by 10%
            )
        
        if schedules:
            # Clear existing data
            await schedules_collection.delete_many({})
            # Insert new data
            result = await schedules_collection.insert_many([s.model_dump() for s in schedules])
            print(f"Successfully seeded {len(result.inserted_ids)} schedules")
            return result.inserted_ids
            
        return []
    except Exception as e:
        print(f"Error seeding schedules: {str(e)}")
        return [] 