import duckdb

import os
from dotenv import load_dotenv
load_dotenv()


class DuchDBHandler:
    def __init__(self, logger):
        self.logger = logger
        self.db_name = os.getenv("DB_NAME")
        self.db_folder = os.getenv("DB_FOLDER")
        self.conn = duckdb.connect(database=os.path.join(self.db_folder, self.db_name))
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS job_ads (
                job_id VARCHAR PRIMARY KEY,
                job_title VARCHAR,
                company VARCHAR,
                responsibilities VARCHAR[],
                qualifications VARCHAR[],
                experiences VARCHAR,
                skills VARCHAR[],
                salary VARCHAR,
                working_location VARCHAR,
                source_url VARCHAR,
                keyword VARCHAR
            )
        """)

    def insert_jobAd(self, job:dict):
        self.conn.execute("""
            INSERT OR REPLACE INTO job_ads (job_id, job_title, company, responsibilities, qualifications, experiences, skills, salary, working_location, source_url, keyword)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (job['job_id'], job['job_title'], job['company'], job['responsibilities'], job['qualifications'], job['experiences'], job['skills'], job['salary'], job['working_location'], job['source_url'], job['keyword']))
        self.logger.info(f"Inserted/Updated job ad with ID: {job['job_id']}, Title: {job['job_title']}")


    def run_query(self, query: str):
        return self.conn.execute(query).fetchall()


    def fetch_all_job_ads(self):
        return self.conn.execute("SELECT * FROM job_ads").fetchall()


    def close(self):
        self.conn.close()


