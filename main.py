import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.JobPosting import Post
from tools.JobSummarizer import JobSummarizer
from tools.SQLiteDatabase import sqliteHandler, JobAd
# from tools.DuchDBHandler import DuchDBHandler
# from tools.ReportGenerator import JobResearchReportGenerator
from tools.writeReport import write_report


from pprint import pformat


def generate_urls(keyword: str) -> list[str]:
    total_page=int(os.getenv("MAX_SEARCH_PAGES"))
    urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page)]
    
    return urls


# main program.
def main():
    # initiate classes: logger, webcrawler, DuckDBHandler.
    logger = Logger(__name__).get_logger()
    Crawler = WebCrawler(logger=logger)
    sqlHandler = sqliteHandler(logger=logger)
    Summarizer = JobSummarizer(logger=logger)
    sqlHandler.check_and_create_table()
    # DBHandler = DuchDBHandler(logger=logger)
    # Generator = JobResearchReportGenerator(logger=logger, DBHandler=DBHandler)
    
    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # generate the search page urls for specific keyword.
        urls = generate_urls(keyword=keyword)
        logger.info(f"Total {len(urls)} generated: {urls}")
        
        unique_jobAds = asyncio.run(Crawler.crawl_multiple_pages(urls=urls, keyword=keyword))
        
        # save all crawled data:
        # logger.info("Save crawled data into sqlite3 DB.")
        # for job in unique_jobAds:
        #     job_item = JobAd(
        #         id=job.url.split("?")[0].split("/")[-1],
        #         url=job.url,
        #         ad_content=job.markdown,
        #         keyword=keyword
        #     )
        #     logger.info(f"job_item: \n%s", pformat(job_item.model_dump(), indent=2))
        #     sqlHandler.create_JobAd(job_item=job_item)
        

        # jobs = sqlHandler.fetch_all_JobAds_by_keyword(keyword=keyword)
        # logger.info(f"total No. of JobAds fetched from sqlite3 DB: {len(jobs)}")
        # summarize the job ads.
        summaries = asyncio.run(Summarizer.summarize_all_jobs(jobs=unique_jobAds, keyword=keyword))
        
        # # save data to database.
        # logger.info("Start insert all the summaries to DuckDB.")
        # for i, summary in enumerate(summaries):
        #     DBHandler.insert_jobAd(job=summary)
            
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
