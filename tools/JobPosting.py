from pydantic import BaseModel, Field
from typing import List, Optional


class JobPosting(BaseModel):
    job_title: str = Field(description="job title")
    company: Optional[str] = Field(description="company of this job")
    responsibilities: List[str] = Field(default_factory=list, description="roles and responsibilities of the job or the work you will do")
    requirements: List[str] = Field(default_factory=list, description="all the job requirements on qualifications and skills")
    salary: Optional[str]
    working_location: Optional[str]
    experiences: Optional[str] = Field(description="working expereiences of the job") 