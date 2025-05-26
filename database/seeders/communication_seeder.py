from datetime import datetime, timedelta
from database import db
from database.models import Communication
from bson import ObjectId
import random

# More realistic email contents with industry-specific pain points
EMAIL_CONTENTS = {
    "initial_contact": [
        "Hi {first_name},\n\nI noticed your team at {company} visited our pricing page. Given your focus on {industry}, I thought you might be interested in how we've helped similar companies reduce their sales cycle by 30% and increase conversion rates by 25%.\n\nWould you be open to a 15-minute chat to discuss your specific challenges?\n\nBest regards,\n{rep_name}",
        "Hello {first_name},\n\nI saw that {company} downloaded our enterprise guide. As a {industry} company, you might be facing challenges with {pain_point}. We've helped companies like yours streamline their processes and improve ROI.\n\nWould you be interested in seeing a quick demo of how we can help?\n\nRegards,\n{rep_name}",
        "Hi {first_name},\n\nI noticed your team at {company} has been exploring automation solutions. Given your {industry} focus, I thought you might be interested in how we've helped similar companies reduce manual tasks by 40% and improve team productivity.\n\nWould you have 15 minutes for a quick chat about your specific needs?\n\nBest,\n{rep_name}"
    ],
    "follow_up": [
        "Hi {first_name},\n\nI wanted to follow up on our previous conversation about {topic}. I've attached a case study of how we helped a similar {industry} company achieve {result}.\n\nWould you have time this week to discuss how we might help {company}?\n\nBest regards,\n{rep_name}",
        "Hello {first_name},\n\nI noticed you haven't opened our last few emails about {topic}. I understand you're busy, but I wanted to make sure you had all the information you need about how we can help with {pain_point}.\n\nIs there a better time to connect?\n\nRegards,\n{rep_name}",
        "Hi {first_name},\n\nI wanted to share some recent updates about {topic} that might be relevant to {company}'s goals. We've recently helped several {industry} companies achieve {result}.\n\nWould you be interested in a quick update call?\n\nBest,\n{rep_name}"
    ],
    "demo_request": [
        "Hi {first_name},\n\nI'd be happy to schedule a demo focused on {topic}. Based on {company}'s needs, I think you'll be particularly interested in our {feature} capabilities.\n\nWould next {day} at {time} work for you? I'll make sure to include {other_decision_maker} in the invite.\n\nBest regards,\n{rep_name}",
        "Hello {first_name},\n\nI've prepared a custom demo that addresses {company}'s specific challenges with {pain_point}. I'll show you how we've helped similar {industry} companies achieve {result}.\n\nWhen would be a good time for a 30-minute walkthrough?\n\nRegards,\n{rep_name}",
        "Hi {first_name},\n\nI've attached some case studies from {industry} companies similar to {company}. I'd love to show you how we can help with {pain_point} and achieve {result}.\n\nWould you be available for a demo this week?\n\nBest,\n{rep_name}"
    ]
}

# More realistic call transcripts with industry-specific context
CALL_TRANSCRIPTS = [
    """Lead: Hi, thanks for calling. I've been looking at your platform and have some questions about the integration capabilities.
Rep: Of course! I noticed you're using Salesforce and HubSpot. We have native integrations with both, and I'd be happy to show you how they work. What specific integration challenges are you facing?
Lead: Well, we're currently spending a lot of time manually syncing data between systems.
Rep: That's a common pain point. Our integration can automate that process and reduce manual work by up to 40%. Would you like to see how it works?
Lead: Yes, that would be helpful. We're also concerned about data accuracy.
Rep: I understand. Our integration includes data validation and error handling to ensure accuracy. I can show you some examples during the demo.""",

    """Lead: Hello, I'm interested in your automation features.
Rep: Great! I see you're in the {industry} space. What specific processes are you looking to automate?
Lead: Mainly our lead nurturing and follow-up process. We're currently using spreadsheets.
Rep: I understand. Many of our {industry} clients were in the same situation. Our automation can help you create personalized nurture sequences and ensure no leads fall through the cracks.
Lead: How does it handle different types of leads?
Rep: We have smart segmentation capabilities that can automatically categorize leads based on their behavior and engagement. Would you like to see how that works?""",

    """Lead: Hi, I saw your pricing page and wanted to discuss the enterprise plan.
Rep: I'd be happy to go through the enterprise features. I notice you have about 200 sales reps. Our enterprise plan is designed for teams of that size and includes advanced features like AI-powered forecasting and custom reporting.
Lead: Yes, we're particularly interested in the forecasting capabilities.
Rep: Perfect! Our AI forecasting has helped similar companies improve their forecast accuracy by 35%. I can show you some real examples during the demo.
Lead: That sounds promising. What about implementation time?
Rep: For a team your size, we typically complete implementation within 4-6 weeks. I can share our implementation plan and timeline if you're interested."""
]

# More detailed meeting notes with action items
MEETING_NOTES = [
    """Key Points:
- Lead is looking to replace their current CRM due to poor automation and reporting
- Main pain points:
  * Manual data entry taking 20% of sales team's time
  * Lack of real-time visibility into pipeline
  * Inaccurate forecasting
- Budget approved for Q3, approximately $X per user
- Decision makers:
  * CTO (technical evaluation)
  * Sales Director (user adoption)
  * CFO (ROI approval)
- Timeline: Looking to implement within 3 months
- Current system: Salesforce (basic plan)

Next Steps:
1. Send ROI calculator with their specific metrics
2. Schedule technical deep dive with IT team
3. Prepare custom demo focusing on automation features
4. Share implementation timeline and resource requirements
5. Connect with current customers in their industry

Follow-up:
- Send case studies by EOD
- Schedule next meeting in 1 week
- Prepare pricing proposal""",

    """Meeting Summary:
- Lead is expanding to new markets in Europe and Asia
- Key Requirements:
  * Multi-currency and multi-language support
  * Compliance with GDPR and local regulations
  * Integration with existing ERP system
- Current Challenges:
  * Data silos between regions
  * Inconsistent reporting across markets
  * Manual currency conversion
- Team Size: 50 sales reps across 3 regions
- Current System: Custom solution (outdated)

Action Items:
1. Prepare multi-currency demo
2. Share localization features and compliance documentation
3. Schedule security review with IT team
4. Provide integration specifications
5. Create regional rollout plan

Timeline:
- Technical evaluation: 2 weeks
- Security review: 1 week
- Pilot program: 1 month
- Full rollout: 3 months

Next Steps:
- Send compliance documentation
- Schedule technical deep dive
- Prepare regional pricing"""
]

async def seed_communications(lead_ids, employee_ids):
    """Seed the communications collection with initial data"""
    try:
        communications_collection = db.get_db().communications
        leads_collection = db.get_db().leads
        companies_collection = db.get_db().companies
        employees_collection = db.get_db().employees
        
        if not lead_ids or not employee_ids:
            print("No lead_ids or employee_ids provided. Please seed leads and employees first.")
            return []
        
        # Sample communication data
        communications = []
        for lead_id in lead_ids:
            # Get lead and company details for personalized content
            lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
            if not lead:
                continue
                
            company = await companies_collection.find_one({"_id": ObjectId(lead["company_id"])})
            if not company:
                continue
            
            # Create 3-5 communications per lead
            num_communications = random.randint(3, 5)
            for i in range(num_communications):
                # Generate a random date within the last 30 days
                date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                
                # Select random employee
                employee = await employees_collection.find_one({"_id": ObjectId(random.choice(employee_ids))})
                if not employee:
                    continue
                
                # Generate communication content based on type
                comm_type = random.choice(["email", "call", "meeting"])
                if comm_type == "email":
                    if i == 0:
                        content = random.choice(EMAIL_CONTENTS["initial_contact"]).format(
                            first_name=lead["first_name"],
                            company=company["name"],
                            industry=company["industry"],
                            pain_point="data integration",
                            rep_name=f"{employee['first_name']} {employee['last_name']}"
                        )
                    elif i == 1:
                        content = random.choice(EMAIL_CONTENTS["follow_up"]).format(
                            first_name=lead["first_name"],
                            company=company["name"],
                            industry=company["industry"],
                            topic="automation features",
                            pain_point="manual processes",
                            result="40% efficiency improvement",
                            rep_name=f"{employee['first_name']} {employee['last_name']}"
                        )
                    else:
                        content = random.choice(EMAIL_CONTENTS["demo_request"]).format(
                            first_name=lead["first_name"],
                            company=company["name"],
                            industry=company["industry"],
                            topic="enterprise features",
                            feature="AI-powered forecasting",
                            pain_point="forecast accuracy",
                            result="35% improvement in forecast accuracy",
                            day="Tuesday",
                            time="2 PM",
                            other_decision_maker="your technical team",
                            rep_name=f"{employee['first_name']} {employee['last_name']}"
                        )
                elif comm_type == "call":
                    content = random.choice(CALL_TRANSCRIPTS).format(
                        industry=company["industry"]
                    )
                else:  # meeting
                    content = random.choice(MEETING_NOTES)
                
                # Generate a simple embedding (in a real system, this would be generated by an ML model)
                embedding = [random.uniform(-1, 1) for _ in range(384)]  # Using 384 dimensions as an example
                
                # Create communication with all required fields
                communication = Communication(
                    lead_id=str(lead_id),
                    employee_id=str(employee["_id"]),
                    type=comm_type,
                    content=content,
                    sentiment_score=random.uniform(-1, 1),  # Required field: -1 to 1 scale
                    status="completed",
                    embedding=embedding,
                    created_at=date
                )
                communications.append(communication)
        
        if not communications:
            print("No communications created. Check lead_ids and employee_ids.")
            return []
            
        # Clear existing data
        await communications_collection.delete_many({})
        
        # Insert new data
        result = await communications_collection.insert_many([comm.model_dump() for comm in communications])
        print(f"Successfully seeded {len(result.inserted_ids)} communications")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding communications: {str(e)}")
        return [] 