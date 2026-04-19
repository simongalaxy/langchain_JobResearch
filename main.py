from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.OllamaSummarizer import OllamaSummarizer
from tools.DBHandler import DBHandler
from tools.OllamaResearcher import OllamaResearcher

from pprint import pformat
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


# main program.
def main():
    # initiate classes: logger, webcrawler, DuckDBHandler.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    summarizer = OllamaSummarizer(logger=logger)
    dbhandler = DBHandler(logger=logger)
    dbhandler.create_table()
    researcher = OllamaResearcher(logger=logger)
    
    # chat loop.
    while True:
        query = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if query.lower() == 'q':
            logger.info("User exited the application.")
            break
        
        # must convert query to a string in format "text-text-text" before searching.
        keyword = query.replace(" ", "-")
        logger.info(f"query input: {query}, keyword: {keyword}")
        
        # crawl all job pages based on the keyword and save the extracted results to the postgresql database.
        total_search_pages = 5
        job_results = crawler.crawl_all_job_pages(
            keyword=keyword, 
            total_pages=total_search_pages
        )
        
        # Extract information from job ads.
        job_infos = asyncio.run(summarizer.summarize_all_jobs(results=job_results, keyword=keyword))

        # save data to postgresql.
        for job in job_infos:
            dbhandler.insert_job(job_item=job)
        
        # generate report.
        researcher.generate_job_market_report(keyword=keyword)
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
