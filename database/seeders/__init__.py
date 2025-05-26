from .company_seeder import seed_companies
from .employee_seeder import seed_employees
from .lead_seeder import seed_leads
from .communication_seeder import seed_communications
from .summary_seeder import seed_summaries
from .opportunity_seeder import seed_opportunities
from .schedule_seeder import seed_schedules

async def seed_all():
    """Seed all collections in the correct order"""
    try:
        print("Starting database seeding...")
        
        # Step 1: Seed companies
        print("\nSeeding companies...")
        company_ids = await seed_companies()
        if not company_ids:
            print("Failed to seed companies. Aborting.")
            return False
            
        # Step 2: Seed employees
        print("\nSeeding employees...")
        employee_ids = await seed_employees()
        if not employee_ids:
            print("Failed to seed employees. Aborting.")
            return False
            
        # Step 3: Seed leads
        print("\nSeeding leads...")
        lead_ids = await seed_leads(company_ids)
        if not lead_ids:
            print("Failed to seed leads. Aborting.")
            return False
            
        # Step 4: Seed communications
        print("\nSeeding communications...")
        communication_ids = await seed_communications(lead_ids, employee_ids)
        if not communication_ids:
            print("Failed to seed communications. Aborting.")
            return False
            
        # Step 5: Seed summaries
        print("\nSeeding communication summaries...")
        summary_ids = await seed_summaries(lead_ids)
        if not summary_ids:
            print("Failed to seed summaries. Aborting.")
            return False
            
        # Step 6: Seed opportunities
        print("\nSeeding opportunities...")
        opportunity_ids = await seed_opportunities(lead_ids)
        if not opportunity_ids:
            print("Failed to seed opportunities. Aborting.")
            return False
            
        # Step 7: Seed schedules
        print("\nSeeding schedules...")
        schedule_ids = await seed_schedules(employee_ids, lead_ids)
        if not schedule_ids:
            print("Failed to seed schedules. Aborting.")
            return False
            
        print("\nDatabase seeding completed successfully!")
        return True
        
    except Exception as e:
        print(f"\nError during seeding: {str(e)}")
        return False 