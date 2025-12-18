from pydantic import BaseModel
from typing import List, Optional


class JobPosting(BaseModel):
    job_title: str
    company: Optional[str]
    responsibilities: List[str]
    requirements: List[str]
    salary: Optional[str]
    working_location: Optional[str]
    experiences: Optional[str]
    job_id: Optional[str]
    job_url: Optional[str]
    markdown: Optional[str]