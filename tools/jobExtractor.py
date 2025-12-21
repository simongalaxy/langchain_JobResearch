from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting
from tools.DataProcesser import markdown_to_text
from pprint import pformat

class jobExtractor:
    def __init__(self, logger):
        self.logger = logger
        self.llm = OllamaLLM(model=os.getenv("OLLAMA_EXTRACTION_MODEL"))
        self.logger.info("JobExtractor has been initiatied.")

    # Extract structured job data from unstructured job description using LLM.
    def extract_info_from_jobAd(self, job_content: str) -> str:
        
        self.logger.info(f"Original job content:")
        self.logger.info(job_content)
        self.logger.info("--------start LLM extraction-----------")
        
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
        
        self.logger.info(f"Extracted Job Info - Data type: {type(response)}:")
        self.logger.info(f"Data: \n%s", pformat(response))
        self.logger.info("-"*100)
          
        return response
    
        
