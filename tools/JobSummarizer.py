from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

import asyncio
from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import Post

class JobSummarizer:
    def __init__(self, logger):
        self.logger = logger
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
            self.prompt.format(job_content=job.markdown)
        )
        # add relevant attribute to summary class.
        summary.job_id = job.url.split("?")[0].split("/")[-1]
        summary.source_url = job.url
        summary.keyword = keyword
        
        # convert pydantic class to dict.
        summary_dict = summary.model_dump()
        
        self.logger.info(f"Original job content:\n {job.markdown}")
        self.logger.info(f"Extracted job info (data type: {type(summary_dict)}): \n%s", pformat(summary_dict, indent=2))
        self.logger.info("-"*100)
          
        return summary
    
    
    async def summarize_all_jobs(self, jobs, keyword):
        self.logger.info("Job Summarization starts.")
        tasks = [self.summarize_job_info(job=job, keyword=keyword) for job in jobs]
        summaries = await asyncio.gather(*tasks)
        self.logger.info("Job summarization completed.")
        
        return summaries
        
