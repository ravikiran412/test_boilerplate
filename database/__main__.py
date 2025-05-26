import asyncio
from database import db
from database.seeders import seed_all

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

if __name__ == "__main__":
    asyncio.run(main()) 