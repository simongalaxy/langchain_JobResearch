import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.jobExtractor import jobExtractor



# main program.
def main():
    # initiate logger.
    logger = Logger(__name__).get_logger()
    logger.info("Logger has been initiated.")
    
    # initiate webcrawler.
    crawler = WebCrawler(logger=logger)
    logger.info("Webcrawler has been initiated.")
    
    # initiate jobExtractor.
    extractor = jobExtractor(logger=logger)
    logger.info("JobExtractor has been initiatied.")
    
    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # search and crawl jobs by keyword.
        jobAds = asyncio.run(crawler.crawl(keyword=keyword))
        
        # extract information from jobAds.
        jobPosts = extractor.process_jobAds(
            jobAds=jobAds, 
            keyword=keyword
        )


# main program entry point.
if __name__ == "__main__":
    main()
