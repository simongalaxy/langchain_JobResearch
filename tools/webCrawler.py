import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain


class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"type=standard$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.crawl_config = CrawlerRunConfig(
                deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=3,  # Reduced depth for faster crawling
                include_external=False,
                filter_chain=self.filter_chain
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=True,
            exclude_all_images=True,
            exclude_social_media_domains=True,
            # Use valid CSS attribute selectors for better compatibility
            target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'],
            )

    async def crawl(self, keyword: str):
        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun(
                url=f"https://hk.jobsdb.com/{keyword}-jobs", 
                config=self.crawl_config
            )
            self.logger.info(f"WebCrawler: Total {len(results[1:])} were crawled for keyword - {keyword}.")
            
        return results[1:] # to remove the first search result page.
    
    