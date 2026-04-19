import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from pprint import pformat

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

        if not all([self.username, self.password, self.host, self.port, self.db_name]):
            raise ValueError("Missing database credentials in .env file")

        self.postgres_url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        
        # Create persistent connection with autocommit
        self.conn = psycopg2.connect(self.postgres_url)
        self.conn.autocommit = True
        
        self.logger.info(f"DBHandler initialized and connected to {self.db_name}")

    def create_table(self) -> None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS JobAd (
            id TEXT PRIMARY KEY,                    -- Changed from SERIAL
            url TEXT NOT NULL,
            content TEXT,
            keyword TEXT,
            job_title TEXT,
            company TEXT,
            responsibilities TEXT[],
            qualifications TEXT[],
            experiences TEXT[],
            skills TEXT[],
            salary TEXT,
            working_location TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(create_table_query)
            self.logger.info("Table JobAd created (or already exists)")
        except Exception as e:
            self.logger.error(f"Failed to create table: {e}")
            raise

    def insert_job(self, job_item: JobInfo) -> str | None:
        """Insert or update a job. Returns the job id on success."""
        insert_query = """
        INSERT INTO JobAd (
            id, url, content, keyword, job_title, company,
            responsibilities, qualifications, experiences,
            skills, salary, working_location
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
            working_location = EXCLUDED.working_location,
            updated_at = NOW()
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

        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(insert_query, values)
                row = cur.fetchone()

                if row:
                    inserted_id = row["id"]
                    self.logger.debug(f"Inserted/Updated job {inserted_id}")
                    return inserted_id
                else:
                    self.logger.warning(f"No row returned for job {job_item.id}")
                    return None

        except Exception as e:
            self.logger.error(f"Error inserting job {job_item.id}: {e}")
            # Do NOT raise here if you want the pipeline to continue
            # raise  
            return None

    def query_job(self, query: str):
        """Execute a SELECT query and return all rows."""
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            return []

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.logger.info("Database connection closed.")