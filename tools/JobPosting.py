from pydantic import BaseModel, Field
from typing import List, Optional


class JobPosting(BaseModel):
    job_title: str = Field(description="job title")
    company: Optional[str] = Field(description="company of this job")
    responsibilities: List[str] = Field(description="all the task responsibilities of the job")
    qualifications: List[str] = Field(description="all the job qualifications required")
    skills: List[str] = Field(description="all the technical and soft skills required for this job")
    salary: Optional[str]
    working_location: Optional[str]
    experiences: Optional[str] = Field(description="working expereiences required for this job")
