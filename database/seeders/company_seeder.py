from datetime import datetime
from database import db
from database.models import Company
import random

async def seed_companies():
    """Seed the companies collection with initial data"""
    try:
        companies_collection = db.get_db().companies
        
        # Sample company data
        companies = [
            Company(
                name="TechCorp Solutions",
                industry="Technology",
                company_type="Enterprise",
                size="500-1000",
                location={"city": "San Francisco", "country": "USA"},
                website="https://techcorp-solutions.com",
                linkedin_url="https://linkedin.com/company/techcorp-solutions",
                description="Leading provider of enterprise software solutions"
            ),
            Company(
                name="Global Retail Group",
                industry="Retail",
                company_type="Enterprise",
                size="1000+",
                location={"city": "New York", "country": "USA"},
                website="https://globalretail.com",
                linkedin_url="https://linkedin.com/company/global-retail",
                description="International retail chain with presence in 50+ countries"
            ),
            Company(
                name="HealthTech Innovations",
                industry="Healthcare",
                company_type="Mid-Market",
                size="100-500",
                location={"city": "Boston", "country": "USA"},
                website="https://healthtech-innovations.com",
                linkedin_url="https://linkedin.com/company/healthtech-innovations",
                description="Innovative healthcare technology solutions provider"
            ),
            Company(
                name="FinServ Solutions",
                industry="Financial Services",
                company_type="Enterprise",
                size="500-1000",
                location={"city": "London", "country": "UK"},
                website="https://finserv-solutions.com",
                linkedin_url="https://linkedin.com/company/finserv-solutions",
                description="Financial services technology and consulting firm"
            ),
            Company(
                name="EduTech Systems",
                industry="Education",
                company_type="Mid-Market",
                size="100-500",
                location={"city": "Toronto", "country": "Canada"},
                website="https://edutech-systems.com",
                linkedin_url="https://linkedin.com/company/edutech-systems",
                description="Educational technology and learning management solutions"
            )
        ]
        
        # Clear existing data
        await companies_collection.delete_many({})
        
        # Insert new data
        result = await companies_collection.insert_many([company.model_dump() for company in companies])
        print(f"Successfully seeded {len(result.inserted_ids)} companies")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding companies: {str(e)}")
        return [] 