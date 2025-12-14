from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List

class JobPosting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[str] =None
    job_title: Optional[str] = None
    responsibilities: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )
    requirements: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )
    skills: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    keyword: Optional[str] = None
    url: Optional[str] = Field(default=None, unique=True, index=True)
    job_content: Optional[str] = None
    