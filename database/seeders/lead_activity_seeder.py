from datetime import datetime, timedelta
from database import db
from database.models import LeadActivity
from bson import ObjectId
import random

def calculate_lead_score(activities, real_time_metrics):
    """Calculate lead score based on activities and real-time metrics"""
    score = 0
    
    # Email engagement (max 20 points)
    score += min(real_time_metrics["Email Opens (count)"] * 2, 10)
    score += min(real_time_metrics["Email Clicks (count)"] * 2, 10)
    
    # Website engagement (max 20 points)
    score += min(real_time_metrics["Website Visits (count)"] * 1.5, 10)
    score += min(len(real_time_metrics["Pages Visited (last session)"]) * 2, 10)
    
    # Form submissions and CTAs (max 20 points)
    score += len(real_time_metrics["Form Submissions"]) * 5
    if real_time_metrics["CTA Clicked"] == "Book a demo":
        score += 10
    
    # Demo and trial (max 20 points)
    if real_time_metrics["Demo Requested"]:
        score += 10
    if real_time_metrics["Trial Started"]:
        score += 10
    
    # Communication quality (max 20 points)
    comm_data = real_time_metrics["Communication Data"]
    score += min(comm_data["Email Count"] * 0.5, 5)
    score += (comm_data["Email Sentiment Score"] + 1) * 5  # Convert -1 to 1 range to 0 to 10
    score += min(comm_data["Voice Call Count"] * 2, 5)
    score += min(comm_data["Call Duration Total"] / 10, 5)
    
    # Status and progression (max 20 points)
    status_history = comm_data["Status History"].split(" → ")
    if "Demo" in status_history:
        score += 5
    if "Negotiation" in status_history:
        score += 5
    if "Converted" in status_history:
        score += 10
    
    # Normalize score to 0-100
    return min(score, 100)

async def seed_lead_activities(lead_ids):
    """Seed the lead activities collection with initial data"""
    try:
        activities_collection = db.get_db().lead_activities
        activities = []
        
        print(f"Starting to seed activities for {len(lead_ids)} leads")
        
        for lead_id in lead_ids:
            print(f"Processing lead_id: {lead_id}")
            # Create real-time metrics activity
            last_interaction = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            
            real_time_metrics = {
                "Email Opens (count)": random.randint(1, 10),
                "Email Clicks (count)": random.randint(1, 5),
                "Last Email Open Date": last_interaction.strftime("%Y-%m-%d"),
                "Website Visits (count)": random.randint(5, 15),
                "Pages Visited (last session)": random.sample([
                    "Pricing", "Demo", "Features", "Case Studies", 
                    "About", "Contact", "Blog", "Documentation"
                ], k=random.randint(1, 4)),
                "CTA Clicked": random.choice([
                    "Book a demo", "Start free trial", "Download guide", "Contact sales"
                ]),
                "Form Submissions": random.sample([
                    "Contact Form", "Demo Request", "Ebook Download", "Newsletter Signup"
                ], k=random.randint(1, 3)),
                "Demo Requested": random.choice([True, False]),
                "Trial Started": random.choice([True, False]),
                "Event Attended": random.choice([
                    "Webinar - May 2025", "Product Launch - April 2025",
                    "Industry Best Practices - March 2025", "Customer Success Stories - February 2025"
                ]),
                "Chat Interaction": random.choice([True, False]),
                
                "Communication Data": {
                    "Email Count": random.randint(5, 20),
                    "Email Sentiment Score": round(random.uniform(-1, 1), 1),
                    "Voice Call Count": random.randint(1, 5),
                    "Call Duration Avg": round(random.uniform(2, 10), 1),
                    "Call Duration Total": random.randint(10, 60),
                    "Call Outcomes": {
                        "Interested": random.randint(1, 3),
                        "Voicemail": random.randint(0, 2),
                        "Not Interested": random.randint(0, 1),
                        "Callback Requested": random.randint(0, 2)
                    },
                    "Days Since Last Interaction": random.randint(0, 30),
                    "Status History": " → ".join(random.sample([
                        "New", "Contacted", "Qualified", "Demo", "Negotiation", "Converted", "Lost"
                    ], k=random.randint(2, 5))),
                    "Sequence Stage Completed": random.randint(1, 5),
                    "Meeting Scheduled": random.choice([True, False]),
                    "Days in Current Stage": random.randint(1, 30)
                }
            }
            
            # Create activity with real-time metrics
            activity = LeadActivity(
                lead_id=str(lead_id),
                activity_type="real_time_metrics",
                details=real_time_metrics,
                created_at=last_interaction
            )
            activities.append(activity)
            print(f"Added real-time metrics activity for lead {lead_id}")
            
            # Create individual activities for tracking
            num_activities = random.randint(5, 15)
            print(f"Creating {num_activities} individual activities for lead {lead_id}")
            
            for i in range(num_activities):
                activity_type = random.choice([
                    "email_open", "email_click", "website_visit", "form_submission",
                    "demo_request", "trial_started", "event_attended", "chat_interaction"
                ])
                
                # Generate realistic details based on activity type
                if activity_type == "email_open":
                    details = {
                        "email_id": f"email_{i}",
                        "subject": random.choice([
                            "Quick question about your needs",
                            "Following up on our conversation",
                            "New features that might interest you",
                            "Case study: Similar company success"
                        ]),
                        "open_count": random.randint(1, 5),
                        "last_open_date": last_interaction.isoformat()
                    }
                elif activity_type == "email_click":
                    details = {
                        "email_id": f"email_{i}",
                        "link_clicked": random.choice([
                            "pricing_page",
                            "demo_request",
                            "case_study",
                            "feature_overview"
                        ]),
                        "click_count": random.randint(1, 3)
                    }
                elif activity_type == "website_visit":
                    details = {
                        "pages_visited": random.sample([
                            "pricing",
                            "features",
                            "case-studies",
                            "about",
                            "contact",
                            "blog"
                        ], k=random.randint(1, 4)),
                        "session_duration": random.randint(60, 1800),
                        "cta_clicked": random.choice([
                            "Book a demo",
                            "Start free trial",
                            "Download guide",
                            "Contact sales"
                        ])
                    }
                elif activity_type == "form_submission":
                    details = {
                        "form_type": random.choice([
                            "Contact Form",
                            "Demo Request",
                            "Ebook Download",
                            "Newsletter Signup"
                        ]),
                        "submitted_data": {
                            "name": f"Lead {i}",
                            "email": f"lead{i}@example.com",
                            "company": f"Company {i}"
                        }
                    }
                elif activity_type == "demo_request":
                    details = {
                        "requested_date": (last_interaction + timedelta(days=random.randint(1, 14))).isoformat(),
                        "preferred_time": random.choice(["morning", "afternoon", "evening"]),
                        "attendees": random.randint(1, 5)
                    }
                elif activity_type == "trial_started":
                    details = {
                        "start_date": last_interaction.isoformat(),
                        "plan_type": random.choice(["basic", "professional", "enterprise"]),
                        "users_added": random.randint(1, 10)
                    }
                elif activity_type == "event_attended":
                    details = {
                        "event_name": random.choice([
                            "Product Launch Webinar",
                            "Industry Best Practices",
                            "Customer Success Stories",
                            "Platform Deep Dive"
                        ]),
                        "event_date": last_interaction.isoformat(),
                        "duration": random.randint(30, 120)
                    }
                else:  # chat_interaction
                    details = {
                        "chat_duration": random.randint(5, 45),
                        "topics_discussed": random.sample([
                            "pricing",
                            "features",
                            "integration",
                            "support",
                            "security"
                        ], k=random.randint(1, 3)),
                        "agent_name": random.choice([
                            "Sarah Johnson",
                            "Michael Chen",
                            "Emily Rodriguez"
                        ])
                    }
                
                activity = LeadActivity(
                    lead_id=str(lead_id),
                    activity_type=activity_type,
                    details=details,
                    created_at=last_interaction
                )
                activities.append(activity)
                print(f"Added {activity_type} activity for lead {lead_id}")
                
                # Update last interaction time
                last_interaction -= timedelta(days=random.randint(1, 5))
        
        if not activities:
            print("No activities created. Check lead_ids.")
            return []
            
        # Clear existing data
        print("Clearing existing activities...")
        await activities_collection.delete_many({})
        
        # Insert new data
        print(f"Inserting {len(activities)} activities...")
        result = await activities_collection.insert_many([a.model_dump() for a in activities])
        print(f"Successfully seeded {len(result.inserted_ids)} lead activities")
        
        return result.inserted_ids
    except Exception as e:
        print(f"Error seeding lead activities: {str(e)}")
        return [] 