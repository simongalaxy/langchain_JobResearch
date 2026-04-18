from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig, MemoryAdaptiveDispatcher, CrawlResult
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

from typing import List
import asyncio
from pprint import pformat
import re

# from tools.DataClass import JobAd

class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.browser_config = BrowserConfig(
            headless=True,
            text_mode=True,
	        light_mode=True
        )
        self.crawl_config_job = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            # Use valid CSS attribute selectors for better compatibility
            target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'], # for jobsdb
            cache_mode=CacheMode.BYPASS,
        )
        self.crawl_config_search = CrawlerRunConfig(
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            cache_mode=CacheMode.BYPASS,
        )
        self.dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=70,
            check_interval=1,
            max_session_permit=6
        )
        
        self.logger.info(f"{WebCrawler.__name__} initiated.")


    async def _crawl_pages(self, urls: List[str], config: CrawlerRunConfig) -> List[CrawlResult]:
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun_many(
                urls=urls, 
                config=config,
                dispatcher=self.dispatcher
            )
        self.logger.info(f"Total {len(results)} job pages crawled.")
                
        return results
    
    
    def _extract_job_links(self, results: List[CrawlResult]) -> List[str]:
        # extract the job page links.
        job_links = []
        for i, result in enumerate(results):
            links = result.links.get("internal", [])
            for link in links:
                if re.search(pattern=r"\d+\?type=standard", string=link["href"]):
                    job_links.append(link["href"])
            
        self.logger.info(f"Total {len(job_links)} job page links crawled from {len(results)} search pages.")    
         
        return job_links

    
    # def _get_JobAd_info_from_result(self, keyword: str, results: List[CrawlResult]) -> List[JobAd]:
    #     jobAds = []
    #     for i, result in enumerate(results, start=1):
    #         url = result.url
    #         content = result.markdown
    #         job_id = result.url.split("/")[-1].split("?")[0]
    #         jobad = JobAd(
    #             keyword=keyword,
    #             job_id=job_id,
    #             url=url,
    #             content=content,
    #             extracted_data=None
    #         )
    #         self.logger.info(f"Item -{i}: \n%s", pformat(jobad.model_dump(), indent=2))
    #         jobAds.append(jobad)

    #     return jobAds

    def _generate_urls(self, keyword: str, total_page: int) -> list[str]:
        urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page+1)]
        self.logger.info(f"Generated total {len(urls)} search pages - urls: {urls}")
        
        return urls


    def crawl_all_job_pages(self, keyword: str, total_pages: int) -> List[CrawlResult]: 
        # Generate search pages.
        urls = self._generate_urls(
            keyword=keyword, 
            total_page=total_pages)
        for i, url in enumerate(urls):
            print(f"{i}: {url}")

        # crawl all links for job pages from search pages.
        results = asyncio.run(self._crawl_pages(urls=urls, config=self.crawl_config_search))
        
        # extract job ad links.
        job_links = self._extract_job_links(results=results)
        
        # crawl all contents from each job pages.
        job_results = asyncio.run(self._crawl_pages(urls=job_links, config=self.crawl_config_job))
        
        # # extract inforamation from results and save them into JobAd dataclass.
        # JobAds = self._get_JobAd_info_from_result(keyword=keyword, results=job_results)
        
        return job_results
        
        
