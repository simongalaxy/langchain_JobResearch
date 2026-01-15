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


class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"type=standard$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.browser_config = BrowserConfig(
            headless=True,
            text_mode=True
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
        )
        self.logger.info("Webcrawler has been initiated.")

    
    def get_job_id(self, result) -> str:
        return result.url.split("?")[0].split("/")[-1]
    
    
    def get_unique_jobAds(self, results, keyword):
        seen = set()
        unique_jobAds = []
        
        self.logger.info(f"Start getting unique jobAds....")
        for result in results:
            job_id = self.get_job_id(result=result)
            if job_id not in seen and f"{keyword}-jobs" not in job_id:
                seen.add(job_id)
                unique_jobAds.append(result)
        
        self.logger.info(f"Total {len(unique_jobAds)} unique jobAds get.")
        
        return unique_jobAds


    async def crawl_page(self, url: str):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun(
                url=url, 
                config=self.crawl_config
            )
                
        return results
    
    
    async def crawl_multiple_pages(self, urls: list[str], keyword):
        tasks = [self.crawl_page(url=url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # consolidate a list of jobAd from results.
        jobAds = []
        for result in results:
            for item in result:
                jobAds.append(item)
            
        self.logger.info(f"Total Pages crawled:        {len(jobAds)}")
        self.logger.info(f"Total search Pages crawled: {len(urls)}")
        
        # return unique_jobAds.
        unique_jobAds = self.get_unique_jobAds(results=jobAds, keyword=keyword)
        
        return unique_jobAds 
    
    
    
    
        
        