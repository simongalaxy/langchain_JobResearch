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
        total_page=20
        urls = [f"https://hk.jobsdb.com/{keyword}-jobs?page={page}" for page in range(1, total_page)]
        logger.info(f"total {len(urls)} urls: {urls}")

        # crawl all jobAds from urls.
        unique_jobAds = []
        seen = set()
        count = 0
        for url in urls:
            logger.info(f"Start crawl search page - url: {url}")
            results = asyncio.run(crawler.crawl(url=url))
            
            unique_jobAds_per_url = get_unique_jobAds_by_id(jobAds=results)
            total_unique_jobAds_per_url = len(unique_jobAds_per_url)
            
            if total_unique_jobAds_per_url == 1: # break the loop when no search results.
                break
            else:
                # save jobAds to list.
                count +=1
                for job in unique_jobAds_per_url:
                    job_id = job.url.split("?")[0].split("/")[-1]
                    if job_id not in seen:
                        seen.add(job_id)
                        dict = {
                            "jobId": job_id,
                            "url": job.url,
                            "markdown": job.markdown
                        }
                        unique_jobAds.append(dict)
                        logger.info("jobAd: \n%s", pformat(dict))
        
        logger.info(f"Total no. of unique jobAds crawled from {count} search urls: {len(unique_jobAds)}.")
                
        for i, job in enumerate(unique_jobAds[1:], start=1):
            logger.info(f"{i}:")
            extracted_json = extractor.extract_info_from_jobAd(job_content=job["markdown"])
           
            
    return

# main program entry point.
if __name__ == "__main__":
    main()
