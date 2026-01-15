from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

import asyncio
from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting

class JobSummarizer:
    def __init__(self, logger):
        self.logger = logger
        self.modelName = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.llm = ChatOllama(
            model= self.modelName,
            temperature=0.1
            )
        self.structured_llm = self.llm.with_structured_output(JobPosting)
        self.logger.info("JobSummarizer has been initiatied.")


    # Extract structured job data from unstructured job description using LLM/    
    async def summarize_job_info(self, job, keyword):
        
        job_content = job.markdown
        self.logger.info(f"Original job content:\n {job_content}")
        self.logger.info("--------start LLM extraction-----------")
        
        prompt = PromptTemplate.from_template(
            "Summarize the following content:\n{job_content}. Do not add interpretations, Do not invent details. Only use information from the content."
        )
        # get the job summary.
        summary = self.structured_llm.invoke(
            prompt.format(job_content=job_content)
        )
        summary.job_id = job.url.split("?")[0].split("/")[-1]
        summary.source_url = job.url
        summary.keyword = keyword
        
        summary_dict = summary.model_dump(mode="json")
        
        self.logger.info(f"Extracted Job Info - Data type: {type(summary_dict)}:")
        self.logger.info(f"Data: \n%s", pformat(summary_dict, indent=2))
        self.logger.info("-"*100)
          
        return summary_dict    
    
    
    async def summarize_all_jobs(self, jobs, keyword):
        self.logger.info("Job Summarization starts.")
        tasks = [self.summarize_job_info(job=job, keyword=keyword) for job in jobs]
        summaries = await asyncio.gather(*tasks)
        self.logger.info("Job summarization completed.")
        
        return summaries
        
