import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

from tqdm.asyncio import tqdm_asyncio
    
class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"type=standard$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.crawl_config = CrawlerRunConfig(
                deep_crawl_strategy=BFSDeepCrawlStrategy(
                            max_depth=2,  # Reduced depth for faster crawling
                            include_external=False,
                            filter_chain=self.filter_chain,
                        ),
                scraping_strategy=LXMLWebScrapingStrategy(),
                exclude_all_images=True,
                exclude_social_media_domains=True,
                exclude_external_links=True,
                # stream=True,
                # Use valid CSS attribute selectors for better compatibility
                target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'],
                cache_mode=CacheMode.BYPASS
                )
        self.browser_cfg = BrowserConfig(
            headless=True
        )

    async def crawl(self, keyword: str):
        async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
        
            results = await crawler.arun(
                url=f"https://hk.jobsdb.com/{keyword}-jobs", 
                config=self.crawl_config
            )
           
            self.logger.info(f"WebCrawler: Total {len(results)} were crawled for keyword - {keyword}.")
            
        return results # to remove the first search result page.
    
    
    async def concurrent_crawling(self, keyword: str):
        async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
            urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, 10)]
            tasks = [crawler.arun(url=url, config=self.crawl_config) for url in urls]
            results = await asyncio.gather(*tasks)
            
            self.logger.info(f"WebCrawler: Total {len(results)} were crawled for keyword - {keyword}.")
            
        return results