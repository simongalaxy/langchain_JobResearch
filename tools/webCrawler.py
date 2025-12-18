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
                
        return result # to remove the first search result page.
    


