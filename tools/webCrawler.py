from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, CacheMode, BrowserConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

import asyncio
from pprint import pformat
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting
from tools.DataProcesser import get_unique_jobAds_by_id, get_job_id

class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"type=standard$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        # self.llm_config = LLMConfig(
        #     provider="ollama/qwen2.5:3b"
        # )
        self.browser_config = BrowserConfig(
            headless=True,
            text_mode=True
        )
        # self.llm_strategy = LLMExtractionStrategy(
        #     llm_config=self.llm_config,
        #     schema=JobPosting.model_json_schema(), # for jobsdb.
        #     extraction_type="schema",
        #     instruction="Extract job title, company, responsibilities, requirements, salary, working location and experiences from the content. Use empty strings or empty list if information is missing.", # for jobsdb.
        #     chunking_strategy=None,
        #     verbose=True,
        #     extra_args={"temperature": 0, "max_tokens": 800},
        #     input_format="markdown"
        # )
        self.crawl_config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=1,  # Reduced depth for faster crawling
                include_external=False,
                filter_chain=self.filter_chain
                ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            # Use valid CSS attribute selectors for better compatibility
            target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'], # for jobsdb
            cache_mode=CacheMode.BYPASS,
            # extraction_strategy=self.llm_strategy
        )
        self.logger.info("Webcrawler has been initiated.")


    async def crawl(self, url: str):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(
                url=url, 
                config=self.crawl_config
            )
                
        return result 
    

    def get_unique_jobAds(self, urls: list[str]):
        # crawl all jobAds from urls.
        unique_jobAds = []
        seen = set()
       
        for url in urls:
            self.logger.info(f"Start crawl search page - url: {url}")
            results = asyncio.run(self.crawl(url=url))
            
            unique_jobAds_per_url = get_unique_jobAds_by_id(jobAds=results)
            total_unique_jobAds_per_url = len(unique_jobAds_per_url)
            
            if total_unique_jobAds_per_url == 1: # break the loop when no search results.
                break
            else:
                # save jobAds to list.
                count=0
                for job in unique_jobAds_per_url:
                    job_id = get_job_id(job=job)
                    if job_id not in seen:
                        seen.add(job_id)
                        unique_jobAds.append(job)
                        count+=1
                self.logger.info(f"{count} unique job ads crawled under url - {url}.")
        
        self.logger.info(f"Total no. of unique jobAds crawled: {len(unique_jobAds)}.")
        
        return unique_jobAds[1:] # for remove the first search page.   
        
        