import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.jobExtractor import jobExtractor
from tools.DataProcesser import remove_duplicates_by_id


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
        # jobAds = asyncio.run(crawler.crawl(keyword=keyword))
        results = asyncio.run(crawler.concurrent_crawling(keyword=keyword))
        
        for i, result in enumerate(results):
            print(f"No. {i} - Data Type: {type(result)}")
            for item in result:
                print(f"data type of items under result: {type(item)}")
                print(item.url)
        
        # # remove duplicate job advertisement.
        # unique_jobAds = remove_duplicates_by_id(jobAds=jobAds)
        # logger.info(f"Total no. of jobAd (unique): {len(unique_jobAds)}")
    
        
        # # extract information from jobAds.
        # jobInfos = extractor.process_jobAds(
        #     jobAds=jobAds, 
        #     keyword=keyword
        # )


# main program entry point.
if __name__ == "__main__":
    main()
