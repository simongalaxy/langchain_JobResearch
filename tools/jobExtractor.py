from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting
from tools.markdownProcesser import markdown_to_text


class jobExtractor:
    def __init__(self, logger):
        self.logger = logger
        self.llm = OllamaLLM(model=os.getenv("OLLAMA_EXTRACTION_MODEL"))

    # Extract structured job data from unstructured job description using LLM.
    def extract_info_from_jobAd(self, job_content: str) -> str:
        
        schema = JobPosting.model_json_schema()
        extraction_prompt = f"""
        Extract structured information from the job advertisement below.

        You MUST return JSON that strictly follows this JSON Schema:

        {schema}

        Job advertisement:
        ------------------
        {job_content}

        Return ONLY valid JSON. No explanation.
        """

        response = self.llm.invoke(extraction_prompt)
        
        self.logger.info("Job content:")
        self.logger.info(job_content)
        self.logger.info("\n")

        if response.startswith("```json"):
            data = response.replace("```json", "").replace("```", "")
        else:
            data = response
            
        return json.loads(data)
    
    def process_jobAds(self, jobAds, keyword: str) -> list[JobPosting]:
        
        jobs = []
        for i, jobAd in enumerate(jobAds):
            
            extracted_data = self.extract_info_from_jobAd(job_content=markdown_to_text(jobAd))
            job = JobPosting.model_validate(extracted_data)
            updated_job = job.model_copy(update={"url": jobAd.url, "keyword": keyword})
            self.logger.info(f"No. {i}: ")
            self.logger.info(updated_job)
            self.logger.info("-"*100)
            jobs.append(updated_job)
        
        return jobs