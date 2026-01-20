from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select, inspect
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY


from pprint import pformat
import os
from dotenv import load_dotenv
load_dotenv()


# for saving the job ad raw data for further processing.
class JobAd(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True) # 👈 Enforce uniqueness
    url: str
    content: Optional[str] = Field(default=None, description="Raw data of job advertisement.")
    keyword: str = Field(description="keyword in searching the job.")
    job_title: Optional[str] = Field(default=None, description="job title")
    company: Optional[str] = Field(default=None, description="company name")
    responsibilities: List[str] = Field(default=None, sa_column=Column(ARRAY(String)), description="all the task responsibilities of the job")
    qualifications: List[str] = Field(default=None, sa_column=Column(ARRAY(String)), description="all the job qualifications required")
    experiences: List[str] = Field(default=None, sa_column=Column(ARRAY(String)), description="working expereiences required")
    skills: List[str] = Field(default=None, sa_column=Column(ARRAY(String)), description="all the technical and soft skills required for this job")
    salary: Optional[str] = Field(default=None, description="salary of job")
    working_location: Optional[str] = Field(default=None, description="working location.")


class PostgresDBHandler:
    def __init__(self, logger):
        self.logger=logger
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.db_name = os.getenv("db_name")
        self.postgres_url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine=create_engine(self.postgres_url, echo=True)
        
        self.logger.info(f"Class - {PostgresDBHandler.__name__} initiated.")
        
        
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
            
            return

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
        self.logger.info(f"Saved total {len(job_results)} jobDBs into Postgresql for keyword - {keyword}.")
        return None
            
