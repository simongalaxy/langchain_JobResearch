from tools.logger import Logger
from tools.JobCrawler import JobCrawler
from tools.PostgresDatabase import PostgresDBHandler
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
    PsqlHandler = PostgresDBHandler(logger=logger)
    PsqlHandler.check_and_create_table()
    crawler = JobCrawler(logger=logger, db_handler=PsqlHandler)
    # Generator = JobResearchReportGenerator(logger=logger, DBHandler=DBHandler)
    
    # chat loop.
    while True:
        keyword = input("Enter your keyword to search jobs (or type 'q' for quit): ")
        
        if keyword.lower() == 'q':
            logger.info("User exited the application.")
            break
        logger.info(f"keyword input: {keyword}")
        
        # crawl all job pages based on the keyword and save the extracted results to the postgresql database.
        crawler.crawl_all_job_pages(keyword=keyword, total_pages=10)
        
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
