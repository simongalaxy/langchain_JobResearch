from pydantic import BaseModel, Field
from typing import List, Optional

from crawl4ai import CrawlResult


class ExtractedJobInfo(BaseModel):
    job_title: str = Field(description="job title")
    company: Optional[str] = Field(default=None, description="company name")
    responsibilities: List[str] = Field(description="all the task responsibilities of the job")
    qualifications: List[str] = Field(description="all the job qualifications")
    experiences: List[str] = Field(description="years of working expereiences")
    skills: List[str] = Field(description="all the technical and soft skills")
    salary: Optional[str] = Field(default=None, description="salary")
    working_location: Optional[str] = Field(default=None, description="working location")


class JobInfo(BaseModel):
    id: str = Field(description="job id")
    url: str = Field(description="job ad link")
    content: str = Field(description="Original job ad content")
    keyword: str = Field(description="keyword for searching job ad")
    # extracted data from llm.
    job_title: str | None = Field(description="job title")
    company: Optional[str] | None = Field(description="company name")
    responsibilities: List[str] | None = Field(description="all the task responsibilities of the job")
    qualifications: List[str] | None = Field(description="all the job qualifications")
    experiences: List[str] | None = Field(description="years of working expereiences")
    skills: List[str] | None = Field(description="all the technical and soft skills")
    salary: Optional[str] | None = Field(description="salary")
    working_location: Optional[str] | None = Field(description="working location")
    