from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting


class JobSummarizer:
    def __init__(self, logger):
        self.logger = logger
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_EXTRACTION_MODEL"), 
            temperature=0
            )
        self.structured_llm = self.llm.with_structured_output(JobPosting)
        
        self.logger.info("JobSummarizer has been initiatied.")

    # Extract structured job data from unstructured job description using LLM.
    def summarize_info(self, job_content: str):
        
        self.logger.info(f"Original job content:")
        self.logger.info(job_content)
        self.logger.info("--------start LLM extraction-----------")
        
        summary = self.structured_llm.invoke(f"Summarize the content:\n{job_content}. Use empty strings or empty list if information is missing.") 
        
        self.logger.info(f"Extracted Job Info - Data type: {type(summary)}:")
        self.logger.info(f"Data: \n%s", json.dumps(summary.model_dump(), indent=2))
        self.logger.info("-"*100)
          
        return summary
    
        
