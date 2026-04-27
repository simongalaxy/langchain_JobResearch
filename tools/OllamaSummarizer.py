from ollama import AsyncClient
from crawl4ai import CrawlResult

from tools.DataClass import JobInfo, ExtractedJobInfo

import asyncio
from pprint import pformat
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class OllamaSummarizer:
    def __init__(self, logger):
        self.logger = logger
        self.model_name = os.getenv("OLLAMA_EXTRACTION_MODEL")
        if not self.model_name:
            raise ValueError("OLLAMA_EXTRACTION_MODEL not set in .env file")
        
        self.client = AsyncClient()
        self.logger.info(f"Ollama Summarizer initialized with model: {self.model_name}")

    async def _summarize_job_info(self, result: CrawlResult, keyword: str) -> JobInfo:
        url = result.url
        job_id = url.split("/")[-1].split("?")[0]
        content = result.markdown

        # Strong, clear prompt for extraction
        prompt = f"""You are an expert job information extractor.
        Extract the following fields from the job description. 
        Only use information that actually appears in the text. 
        If a field is not mentioned, use null or empty list.

        Return ONLY valid JSON matching this schema. Do not add explanations.

        Job Content:
        {content}
        """

        try:
            response = await self.client.chat(
                model=self.model_name,                    # ← This was becoming None before
                messages=[{'role': 'user', 'content': prompt}],
                format=ExtractedJobInfo.model_json_schema(),   # Native structured output
                options={
                    'temperature': 0.0,
                    'num_ctx': 16384,      # Good for long job descriptions
                    'num_predict': 1500,
                }
            )

            # Parse the JSON response directly into your Pydantic model
            extracted = ExtractedJobInfo.model_validate_json(
                response['message']['content']
            )

            job_info = JobInfo(
                id=job_id,
                url=url,
                content=content,
                keyword=keyword,
                job_info=extracted,
                embedding=None,   # To be filled later
            )

            self.logger.info("Successfully extracted job: \n%s", pformat(job_info.model_dump(), indent=4))
            self.logger.info("#"*50)
            
            return job_info

        except Exception as e:
            self.logger.error(f"Failed to extract job {job_id}: {e}")
            # Fallback: return basic info so the pipeline doesn't crash
            return JobInfo(
                id=job_id,
                url=url,
                content=content,
                keyword=keyword,
                job_info=ExtractedJobInfo(
                    job_title=None,
                    company=None,
                    responsibilities=None,
                    qualifications=None,
                    experiences=None,
                    skills=None,
                    salary=None,
                    working_location=None,
                ),
                embedding=None,
            )

    async def summarize_all_jobs(self, results: List[CrawlResult], keyword: str) -> List[JobInfo]:
        self.logger.info(f"Starting extraction for {len(results)} jobs...")

        semaphore = asyncio.Semaphore(4)   # Tune this (3~6) based on your GPU/RAM

        async def bounded_extract(result: CrawlResult):
            async with semaphore:
                return await self._summarize_job_info(result, keyword)

        tasks = [bounded_extract(result) for result in results]
        job_infos = await asyncio.gather(*tasks, return_exceptions=True)

        # Remove any exceptions
        successful = [j for j in job_infos if not isinstance(j, Exception)]
        self.logger.info(f"Extraction completed. {len(successful)}/{len(results)} jobs succeeded.")

        return successful