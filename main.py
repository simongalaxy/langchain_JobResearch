from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.JobSummarizer import JobSummarizer
from tools.SQLiteDatabase import sqliteHandler
from tools.DuchDBHandler import DuchDBHandler
# from tools.ReportGenerator import JobResearchReportGenerator
# from tools.writeReport import write_report


from pprint import pformat
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


# main program.
def main():
    # initiate classes: logger, webcrawler, DuckDBHandler.
    logger = Logger(__name__).get_logger()
    Crawler = WebCrawler(logger=logger)
    sqlHandler = sqliteHandler(logger=logger)
    sqlHandler.check_and_create_table()
    DBHandler = DuchDBHandler(logger=logger)
    Summarizer = JobSummarizer(logger=logger)
    # Generator = JobResearchReportGenerator(logger=logger, DBHandler=DBHandler)
    
    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # job_results = Crawler.crawl_all_job_pages(
        #     keyword=keyword, 
        #     total_pages=20
        # )
        
        # # # save all crawled data:
        # sqlHandler.save_jobAd_to_db(
        #     job_results=job_results, 
        #     keyword=keyword
        # )

        # load data from sqlite3DB for generating summaries.
        jobs = sqlHandler.fetch_all_JobAds_by_keyword(keyword=keyword)
        logger.info(f"total No. of JobAds fetched from sqlite3 DB: {len(jobs)}")
        
        # summarize the job ads.
        summaries = asyncio.run(Summarizer.summarize_all_jobs(jobs=jobs, keyword=keyword))
        
        # save data to database.
        logger.info("Start insert all the summaries to DuckDB.")
        for i, summary in enumerate(summaries):
            DBHandler.insert_jobAd(job=summary)
            
        # # generate report.
        # report = Generator.generate_report(keyword=keyword)
        # logger.info(f"Generated Report:\n{report}")
        
        # # save the report in text file.
        # write_report(
        #     keyword=keyword,
        #     markdown=report
        # )
       
    return

# main program entry point.
if __name__ == "__main__":
    main()
