from sqlmodel import SQLModel, Field
from typing import Optional, List
from sqlalchemy import Column, JSON

class JobPosting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_title: Optional[str] = None
    responsibilities: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )
    requirements: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )
    skills: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    keyword: Optional[str] = None
    url: Optional[str] = Field(default=None, unique=True, index=True)
    # job_content: Optional[str] = None
    