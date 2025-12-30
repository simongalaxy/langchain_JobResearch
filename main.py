import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.JobSummarizer import JobSummarizer
from tools.DuchDBHandler import DuchDBHandler
from tools.ReportGenerator import JobResearchReportGenerator

from pprint import pformat


# main program.
def main():
    # initiate classes: logger, webcrawler, DuckDBHandler.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    summarizer = JobSummarizer(logger=logger)
    DBHandler = DuchDBHandler(logger=logger)
    
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
        
        results = asyncio.run(crawler.crawl_multiple_pages(urls=urls, keyword=keyword))
        unique_jobAds = crawler.get_unique_jobAds(results=results, keyword=keyword)
        
        # summarize the job ads.
        summaries = asyncio.run(summarizer.summarize_all_jobs(jobs=unique_jobAds, keyword=keyword))
        
        # save data to database.
        logger.info("Start insert all the summaries to DuckDB.")
        for i, summary in enumerate(summaries):
            DBHandler.insert_jobAd(job=summary)
            
        # # generate report.
        # report = Generator.generate_report(keyword=keyword)
        # logger.info(f"Generated Report:\n{report}")
        
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
