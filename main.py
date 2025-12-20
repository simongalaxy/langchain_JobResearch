import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.jobExtractor import jobExtractor
from tools.DataProcesser import get_unique_jobAds_by_id

from pprint import pformat


# main program.
def main():
    # initiate classes: logger, webcrawler, jobExtractor.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    extractor = jobExtractor(logger=logger)
    
    
    
    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # generate the search page urls for specific keyword.
        total_page=2
        urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page)]
        logger.info(f"total {len(urls)} urls: {urls}")
        unique_jobAds = crawler.get_unique_jobAds(urls=urls)
        
        # extract information from jobad and then chunk and embed to chromaDB.
        for i, job in enumerate(unique_jobAds):
            logger.info(f"{i}:")
            extracted_json = extractor.extract_info_from_jobAd(job_content=job["markdown"])

            
    return

# main program entry point.
if __name__ == "__main__":
    main()
