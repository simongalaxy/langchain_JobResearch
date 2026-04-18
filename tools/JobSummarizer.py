from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from crawl4ai import CrawlResult

from typing import List
import asyncio
from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.DataClass import JobInfo, ExtractedJobInfo

class JobSummarizer:
    def __init__(self, logger):
        self.logger = logger
        self.modelName = os.getenv("OLLAMA_MODEL")
        self.llm = ChatOllama(
            model= self.modelName,
            temperature=0.1
            )
        self.structured_llm = self.llm.with_structured_output(ExtractedJobInfo)
        self.prompt = PromptTemplate.from_template(
            "Summarize the following content:\n{job_content}. Do not add interpretations, Do not invent details. Only use information from the content."
        )
        self.logger.info("JobSummarizer has been initiatied.")


    # Extract structured job data from unstructured job description using LLM/    
    async def _summarize_job_info(self, result: CrawlResult, keyword: str) -> JobInfo:
        
        # get basic information from result.
        url = result.url
        id = url.split("/")[-1].split("?")[0]
        content = result.markdown
        
        # get the job summary.
        extracted_info = await self.structured_llm.ainvoke(
            self.prompt.format(job_content=content)
        )
        
        job_info = JobInfo(
            id=id,
            url=url,
            content=content,
            keyword=keyword,
            job_title=extracted_info.job_title,
            company=extracted_info.company,
            responsibilities=extracted_info.responsibilities,
            qualifications=extracted_info.qualifications,
            experiences=extracted_info.experiences,
            skills=extracted_info.skills,
            salary=extracted_info.salary,
            working_location=extracted_info.working_location
        )
        
        self.logger.info(f"Extracted job info: \n%s", pformat(job_info.model_dump(), indent=2))
        self.logger.info("-"*100)
          
        return job_info
    
    
    async def summarize_all_jobs(self, results: List[CrawlResult], keyword: str) -> List[JobInfo]:
        self.logger.info("Job Summarization starts.")
        tasks = [self._summarize_job_info(result=result, keyword=keyword) for result in results]
        job_infos = await asyncio.gather(*tasks)
        self.logger.info("Job summarization completed.")
        
        return job_infos
        