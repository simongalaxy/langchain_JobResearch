from unittest import result
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig, MemoryAdaptiveDispatcher, LLMConfig, LLMExtractionStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

from pprint import pformat
import asyncio, json, re, os
from pydantic import BaseModel, Field
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()

from tools.PostgresDatabase import JobAd, PostgresDBHandler


class Post(BaseModel):
    job_title: Optional[str] = Field(default=None, description="job title")
    company: Optional[str] = Field(default=None, description="company name")
    responsibilities: List[str] = Field(description="all the task responsibilities of the job")
    qualifications: List[str] = Field(description="all the job qualifications required")
    experiences: List[str] = Field(description="working expereiences required")
    skills: List[str] = Field( description="all the technical and soft skills required for this job")
    salary: Optional[str] | None = Field(description="salary of job")
    working_location: Optional[str] | None = Field(description="working location.")


class JobCrawler:
    def __init__(self, logger, db_handler: PostgresDBHandler):
        self.logger = logger
        self.db_handler = db_handler
        self.browser_config = BrowserConfig(
            headless=True,
            text_mode=True,
            light_mode=True
        )
        self.crawl_config_search_page = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_external_links=True,
            exclude_social_media_domains=True,
            cache_mode=CacheMode.BYPASS
        )
        self.llm_config = LLMConfig(
            provider=os.getenv("provider"),    # provider="ollama/mistral:latest"
            temperature=0.1
        )
        self.llm_extraction = LLMExtractionStrategy(
            llm_config=self.llm_config,
            schema=Post.model_json_schema(),
            extraction_type="schema",
            instruction="Summarize the item from the content. Do not add any additional information not present in the content.",
            chunk_token_threshold=1000,
            overlap_rate=0.1,
            apply_chunking=True,
            input_format="markdown",
            extra_args={"temperature": 0.1, "max_tokens": 1000},
            verbose=True
        )
        self.crawl_config_post_page = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_external_links=True,
            exclude_social_media_domains=True,
            target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'],
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=self.llm_extraction,
            stream=True # Enable streaming 
        )
        self.dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=70,
            check_interval=1,
            max_session_permit=4
        )
    
    
    async def crawl_search_pages(self, urls: list[str]):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun_many(
                urls=urls,
                config=self.crawl_config_search_page,
                dispatcher=self.dispatcher
            )
        jobs_links = []
        for result in results:
            links = result.links.get("internal", [])
            for link in links:
                if re.search(pattern=r"\d+\?type=standard", string=link["href"]):
                        jobs_links.append(link["href"])
        
        self.logger.info(f"Total {len(jobs_links)} job page links crawled from {len(urls)} search pages.")
        
        return jobs_links
   
 
    async def crawl_post_pages(self, urls: list[str], keyword:str) -> None:
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            async for result in await crawler.arun_many(
                urls=urls,
                config=self.crawl_config_post_page,
                dispatcher=self.dispatcher
            ):
            
                if result.success:
                    job_item = JobAd(
                        id=result.url.split("?")[-1].split("/")[-1],
                        url=result.url,
                        content=result.markdown,
                        keyword=keyword,
                        job_title=result.extracted_data.job_title,
                        company=result.extracted_data.company,
                        responsibilities=result.extracted_data.responsibilities,
                        qualifications=result.extracted_data.qualifications,
                        experiences=result.extracted_data.experiences,
                        skills=result.extracted_data.skills,
                        salary=result.extracted_data.salary,
                        working_location=result.extracted_data.working_location
                    )
                    self.db_handler.create_JobAd(job_item=job_item)
                    self.logger.info(f"JobAd: \n%s", pformat(job_item.model_dump(), indent=2))
                else:
                    self.logger.error(f"Failed to crawl URL: {result.url}")
            
        return None
    
    
    def generate_urls(self, keyword: str, total_page: int) -> list[str]:
            urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page)]
            self.logger.info(f"Generated total {len(urls)} search pages - urls: {urls}")
            
            return urls


    def crawl_all_job_pages(self, keyword: str, total_pages: int): 
            # Generate search pages.
            urls = self.generate_urls(
                keyword=keyword, 
                total_page=total_pages)
            for i, url in enumerate(urls):
                print(f"{i}: {url}")

            # crawl all links for job pages from search pages.
            job_links = asyncio.run(self.crawl_search_pages(urls=urls))
            
            # crawl all contents from each job pages.
            asyncio.run(self.crawl_post_pages(urls=job_links, keyword=keyword))

            return None