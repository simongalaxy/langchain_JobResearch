import psycopg2
from pprint import pformat
import os
from dotenv import load_dotenv
load_dotenv()

from tools.DataClass import JobInfo

class DBHandler:
    def __init__(self, logger):
        self.logger = logger
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.db_name = os.getenv("db_name")
        self.postgres_url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.conn = psycopg2.connect(self.postgres_url)
        self.conn.autocommit = True
        
        self.logger.info(f"Class - {DBHandler.__name__} initiated.")
    
    def connect(self):
        return psycopg2.connect(dsn=self.postgres_url)
    
    def create_table(self) -> None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS JobAd(
            id SERIAL PRIMARY KEY,
            url TEXT,
            content TEXT,
            keyword TEXT,
            job_title TEXT NULL,
            company TEXT NULL,
            responsibilities TEXT[] NULL,
            qualifications TEXT[] NULL,
            experiences TEXT[] NULL,
            skills TEXT[] NULL,
            salary TEXT NULL,
            working_location TEXT NULL
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query=create_table_query)
            
        return
        
    def insert_job(self, job_item: JobInfo) -> None:
        insert_query = """
        INSERT INTO JobAd (
            id, url, content, keyword, job_title,
            company, responsibilities, qualifications,
            experiences, skills, salary, working_location
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            url = EXCLUDED.url,
            content = EXCLUDED.content,
            keyword = EXCLUDED.keyword,
            job_title = EXCLUDED.job_title,
            company = EXCLUDED.company,
            responsibilities = EXCLUDED.responsibilities,
            qualifications = EXCLUDED.qualifications,
            experiences = EXCLUDED.experiences,
            skills = EXCLUDED.skills,
            salary = EXCLUDED.salary,
            working_location = EXCLUDED.working_location
        RETURNING id;
        """
        values = (
            job_item.id,
            job_item.url,
            job_item.content,
            job_item.keyword,
            job_item.job_title,
            job_item.company,
            job_item.responsibilities,
            job_item.qualifications,
            job_item.experiences,
            job_item.skills,
            job_item.salary,
            job_item.working_location,
        )

        with self.conn.cursor() as cur:
            cur.execute(insert_query, values)
            return cur.fetchone()["id"]
    
    
    def query_job(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query=query)
            return cur.fetchall()
    
      
    def close(self):
        if self.conn:
            self.conn.close()