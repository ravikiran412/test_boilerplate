from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, Field

class Company(BaseModel):
    name: str
    industry: str
    company_type: str
    size: str
    location: Dict[str, str]
    website: str
    linkedin_url: Optional[str]
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    department: str
    workload: float = 0.0  # 0-1 scale
    max_leads: int = 10
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Lead(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    job_title: str
    company_id: str
    lead_source: str
    lead_owner_id: str
    status: str
    score: float = 0.0  # 0-1 scale
    priority: float = 0.0  # 0-1 scale
    predicted_value: float = 0.0
    enrichment_data: Dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Communication(BaseModel):
    lead_id: str
    employee_id: str
    type: str
    content: str
    sentiment_score: float
    status: str
    embedding: List[float] = []  # Vector for semantic search
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CommunicationSummary(BaseModel):
    lead_id: str
    summary: str
    key_points: List[str]
    sentiment: str
    embedding: List[float] = []  # Vector for semantic search
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Opportunity(BaseModel):
    lead_id: str
    value: float
    stage: str
    probability: float
    expected_close_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LeadActivity(BaseModel):
    lead_id: str
    activity_type: str
    details: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Schedule(BaseModel):
    employee_id: str
    lead_id: str
    start_time: datetime
    end_time: datetime
    activity_type: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow) 