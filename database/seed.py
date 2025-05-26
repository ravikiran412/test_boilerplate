import asyncio
from database import db
from database.seeders import seed_all
from database.seeders.company_seeder import seed_companies
from database.seeders.employee_seeder import seed_employees
from database.seeders.lead_seeder import seed_leads
from database.seeders.communication_seeder import seed_communications
from database.seeders.summary_seeder import seed_summaries
from database.seeders.opportunity_seeder import seed_opportunities
from database.seeders.lead_activity_seeder import seed_lead_activities

async def main():
    """Main function to run all seeders"""
    try:
        # Connect to database
        await db.connect_db()
        
        # Run all seeders
        await seed_all()
        
        print("All seeders completed successfully!")
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
    finally:
        # Close database connection
        await db.close_db()

async def seed_all():
    """Seed all collections with initial data"""
    try:
        # Seed companies first
        print("\nSeeding companies...")
        company_ids = await seed_companies()
        if not company_ids:
            print("Failed to seed companies. Aborting.")
            return False

        # Seed employees
        print("\nSeeding employees...")
        employee_ids = await seed_employees()
        if not employee_ids:
            print("Failed to seed employees. Aborting.")
            return False

        # Seed leads
        print("\nSeeding leads...")
        lead_ids = await seed_leads(company_ids)
        if not lead_ids:
            print("Failed to seed leads. Aborting.")
            return False

        # Seed communications
        print("\nSeeding communications...")
        communication_ids = await seed_communications(lead_ids, employee_ids)
        if not communication_ids:
            print("Failed to seed communications. Aborting.")
            return False

        # Seed summaries
        print("\nSeeding summaries...")
        summary_ids = await seed_summaries(lead_ids)
        if not summary_ids:
            print("Failed to seed summaries. Aborting.")
            return False

        # Seed opportunities
        print("\nSeeding opportunities...")
        opportunity_ids = await seed_opportunities(lead_ids)
        if not opportunity_ids:
            print("Failed to seed opportunities. Aborting.")
            return False

        # Seed lead activities
        print("\nSeeding lead activities...")
        activity_ids = await seed_lead_activities(lead_ids)
        if not activity_ids:
            print("Failed to seed lead activities. Aborting.")
            return False

        print("\nAll seeders completed successfully!")
        return True
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 