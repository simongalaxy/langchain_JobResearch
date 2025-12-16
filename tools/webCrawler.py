import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, CacheMode, BrowserConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

from tools.JobPosting import JobPosting

class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"type=standard$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.llm_config = LLMConfig(
            provider="ollama/mistral:7b-instruct"
        )
        self.browser_config = BrowserConfig(headless=True)
        self.llm_strategy = LLMExtractionStrategy(
            llm_config=self.llm_config,
            schema=JobPosting.model_json_schema(), # for jobsdb.
            extraction_type="schema",
            instruction="Extract job title, company, responsibilities, requirements, salary, working location and experiences from the content. Use empty strings or empty list if information is missing.", # for jobsdb.
            chunking_strategy=None,
            verbose=True,
            extra_args={"temperature": 0.0, "max_tokens": 800},
            input_format="markdown"
        )
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
            extraction_strategy=self.llm_strategy
        )
       

    async def crawl(self, keyword: str):
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
            
                results = await crawler.arun(
                    url=f"https://hk.jobsdb.com/{keyword}-jobs", 
                    config=self.crawl_config
                )
            
                self.logger.info(f"WebCrawler: Total {len(results)} were crawled for keyword - {keyword}.")
                
            return results # to remove the first search result page.
    
    
    async def concurrent_crawling(self, keyword: str):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, 10)]
            tasks = [crawler.arun(url=url, config=self.crawl_config) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            self.logger.info(f"WebCrawler: Total {len(results)} were crawled for keyword - {keyword}.")
            
        return results


