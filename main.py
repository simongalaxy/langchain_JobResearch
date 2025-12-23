import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.DataProcesser import get_unique_jobAds_by_id
from tools.JobSummarizer import JobSummarizer

from pprint import pformat


# main program.
def main():
    # initiate classes: logger, webcrawler, jobExtractor.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    # summarizer = JobSummarizer(logger=logger)

    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # generate the search page urls for specific keyword.
        total_page=int(os.getenv("MAX_SEARCH_PAGES"))
        urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page)]
        logger.info(f"total {len(urls)} urls: {urls}")
        
        
        # crawl job ads from the search page urls and then extract information from job ads.
        unique_jobAds = crawler.get_unique_jobAds(urls=urls, keyword=keyword)
        
        for job in unique_jobAds:
            logger.info(f"Job Ad Extracted:\n{pformat(job)}")
        # extract information from jobad and then chunk and embed to chromaDB.
        
        
            
      
            
    return

# main program entry point.
if __name__ == "__main__":
    main()
