from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tools.PostgresDatabase import PostgresDBHandler

import asyncio
from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field
from typing import List, Optional

class Post(BaseModel):
    job_title: str = Field(description="job title")
    company: Optional[str] = Field(default=None, description="company name")
    responsibilities: List[str] = Field(description="all the task responsibilities of the job")
    qualifications: List[str] = Field(description="all the job qualifications")
    experiences: List[str] = Field(description="years of working expereiences")
    skills: List[str] = Field(description="all the technical and soft skills")
    salary: Optional[str] = Field(default=None, description="salary")
    working_location: Optional[str] = Field(default=None, description="working location")


class JobSummarizer:
    def __init__(self, logger, PsqlHandler: PostgresDBHandler):
        self.logger = logger
        self.DBhandler = PsqlHandler
        self.modelName = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.llm = ChatOllama(
            model= self.modelName,
            temperature=0.1
            )
        self.structured_llm = self.llm.with_structured_output(Post)
        self.prompt = PromptTemplate.from_template(
            "Summarize the following content:\n{job_content}. Do not add interpretations, Do not invent details. Only use information from the content."
        )
        self.logger.info("JobSummarizer has been initiatied.")


    # Extract structured job data from unstructured job description using LLM/    
    async def summarize_job_info(self, job, keyword):
        
        # get the job summary.
        summary = await self.structured_llm.ainvoke(
            self.prompt.format(job_content=job.content)
        )
        
        # convert pydantic class to dict.
        summary_dict = summary.model_dump()
        # summary_dict = job.id
        # update relevant data in postgresql database.
        self.DBhandler.update_JobAd(id=job.id, update_data=summary_dict)
        
        self.logger.info(f"Original job content:\n {job.content}")
        self.logger.info(f"Extracted job info (data type: {type(summary_dict)}): \n%s", pformat(summary_dict, indent=2))
        self.logger.info("-"*100)
          
        return summary_dict
    
    
    async def summarize_all_jobs(self, jobs, keyword):
        self.logger.info("Job Summarization starts.")
        tasks = [self.summarize_job_info(job=job, keyword=keyword) for job in jobs]
        summaries = await asyncio.gather(*tasks)
        self.logger.info("Job summarization completed.")
        
        return summaries
        
