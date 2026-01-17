from pydantic import BaseModel, Field
from typing import List, Optional


class Post(BaseModel):
    job_title: str = Field(description="job title")
    company: Optional[str] = Field(description="company name")
    responsibilities: List[str] = Field(description="task responsibilities of the job")
    qualifications: List[str] = Field(description="job qualifications required")
    experiences: List[str] = Field(description="working expereiences required")
    skills: List[str] = Field(description="the technical and soft skills required for this job")
    salary: Optional[str] =Field(description="salary of job")
    working_location: Optional[str] = None
    job_id: Optional[str] = None
    source_url: Optional[str] = None
    keyword: Optional[str] = None

    

