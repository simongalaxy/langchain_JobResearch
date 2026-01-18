from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select, inspect

from pprint import pformat
import os
from dotenv import load_dotenv
load_dotenv()


class JobAd(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True) # 👈 Enforce uniqueness
    url: str
    content: Optional[str]
    keyword: str


class sqliteHandler:
    def __init__(self, logger):
        self.logger=logger
        self.DBname=os.getenv("SQLITE_FILENAME")
        self.sqlite_url = f"sqlite:///{self.DBname}"
        self.engine=create_engine(self.sqlite_url)
        self.logger.info(f"Class - {sqliteHandler.__name__} initiated.")
        
        
    def check_and_create_table(self) -> None:
        inspector = inspect(self.engine)
        if inspector.has_table("JobAd"):
            self.logger.info("Table JobAd already exists.")
        else:
            self.logger.info("Table JobAd does not exist, creating it now.")
            SQLModel.metadata.create_all(self.engine)
            self.logger.info("Table JobAd created.")
        
        return None


    def create_JobAd(self, job_item: JobAd) -> None:
        with Session(self.engine) as session:
            statement = select(JobAd).where(JobAd.id == job_item.id)
            existing = session.exec(statement=statement).first()
            if not existing:
                session.add(job_item)
                session.commit()
                session.refresh(job_item)
                self.logger.info(f"JobAd - id: {job_item.id}) saved to sqlite3.")
            else:
                self.logger.info(f"JobAd - id: {job_item.id} item already existed in database. No saving action taken.")   
        
        return None


    def fetch_all_JobAds_by_keyword(self, keyword: str):
        with Session(self.engine) as session:
            stmt = select(JobAd).where(JobAd.keyword == keyword)
            return session.exec(stmt).all()
        
    
    def read_JobAd(self, id: str):
        with Session(self.engine) as session:
            return session.get(JobAd, id)


    def update_JobAd(self, id: str, update_data: dict):
        with Session(self.engine) as session:
            db_JobAd = session.get(JobAd, id)
            if not db_JobAd:
                return None
            for key, value in update_data.items():
                setattr(db_JobAd, key, value)
            session.add(db_JobAd)
            session.commit()
            session.refresh(db_JobAd)
            
            return db_JobAd

    def delete_JobAd(self, id: str):
        with Session(self.engine) as session:
            db_JobAd = session.get(JobAd, id)
            if db_JobAd:
                session.delete(db_JobAd)
                session.commit()
                return True
            return False


    def list_all_JobAds_id(self):
        with Session(self.engine) as session:
            return session.exec(select(JobAd.id)).all()
    
    
    def save_jobAd_to_db(self, job_results, keyword) -> None:
        # save all crawled data:
        self.logger.info("Save crawled data into sqlite3 DB.")
        for job in job_results:
            job_item = JobAd(
                id=job.url.split("?")[0].split("/")[-1],
                url=job.url,
                content=job.markdown,
                keyword=keyword
            )
            # self.logger.info(f"job_item: \n%s", pformat(job_item.model_dump(), indent=2))
            self.create_JobAd(job_item=job_item)
        self.logger.info(f"Saved total {len(job_results)} jobAds into sqlite3DB for keyword - {keyword}.")
        return None
            
## usage example

# handler = sqliteHandler("news_data.db")

# # Create
# new_entry = News(
#     title="2026 Tech Trends", 
#     publish_date=date(2026, 1, 9), 
#     publish_time=time(14, 30),
#     source_url="https://example.com",
#     content="Full article content...",
#     keywords="AI, Tech, Future"
# )
# handler.create_news(new_entry)

# # Read
# news = handler.read_news(1)
# print(news.title if news else "Not Found")