import duckdb

import os
from dotenv import load_dotenv
load_dotenv()


class DuchDBHandler:
    def __init__(self, logger):
        self.logger = logger
        self.db_name = os.getenv("DB_NAME")
        self.db_folder = os.getenv("DB_FOLDER")
        self.table_name = os.getenv("DB_TABLE")
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
        
    
    def run_query(self, query: str) -> str:
        try:
            result = self.conn.execute(query).fetchdf()  # Returns pandas DataFrame
            return result.to_string(index=False) or "No results."
        except Exception as e:
            return f"Query error: {str(e)}"

    def gather_insights(self, keyword: str) -> str:
        """Run a set of targeted SQL queries to extract all needed data for the report."""
        queries = {
            "Total jobs": f"SELECT COUNT(*) AS total_jobs FROM {self.table_name} where keyword = '{keyword}';",
            "Top job titles": f"""
                SELECT job_title, COUNT(*) AS count 
                FROM {self.table_name} 
                WHERE job_title IS NOT NULL and keyword = '{keyword}'
                GROUP BY job_title 
                ORDER BY count DESC 
                LIMIT 10;
            """,
            "Top companies": f"""
                SELECT company, COUNT(*) AS count 
                FROM {self.table_name} 
                WHERE company IS NOT NULL and keyword = '{keyword}'
                GROUP BY company 
                ORDER BY count DESC 
                LIMIT 10;
            """,
            "Top locations": f"""
                SELECT working_location, COUNT(*) AS count 
                FROM {self.table_name} 
                WHERE working_location IS NOT NULL and keyword = '{keyword}'
                GROUP BY location 
                ORDER BY count DESC 
                LIMIT 10;
            """,
            "Most requested skills": f"""
                SELECT UNNEST(string_split(skills, ',')) AS skill, COUNT(*) AS count
                FROM {self.table_name}
                WHERE skills IS NOT NULL AND skills != '' and keyword = '{keyword}'
                GROUP BY skill
                ORDER BY count DESC
                LIMIT 15;
            """,  # Adjust if skills are stored differently (e.g., JSON array)
            "Most responsibilities": f"""
                SELECT UNNEST(string_split(responsibilities, ',')) AS responsibility, COUNT(*) AS count
                FROM {self.table_name}
                WHERE responsibilities IS NOT NULL AND responsibilities != '' and keyword = '{keyword}'
                GROUP BY responsibility
                ORDER BY count DESC
                LIMIT 15;
            """, 
            "Most qualifications": f"""
                SELECT UNNEST(string_split(qualifications, ',')) AS qualification, COUNT(*) AS count
                FROM {self.table_name}
                WHERE qualifications IS NOT NULL AND qualifications != '' and keyword = '{keyword}'
                GROUP BY qualifications
                ORDER BY count DESC
                LIMIT 15;
            """, 
            "Most experiences": f"""
                SELECT UNNEST(string_split(experiences, ',')) AS experience, COUNT(*) AS count
                FROM {self.table_name}
                WHERE experiences IS NOT NULL AND experiences != '' and keyword = '{keyword}'
                GROUP BY experiences
                ORDER BY count DESC
                LIMIT 15;
            """, 
            "Salary ranges": f"""
                SELECT 
                    MIN(salary) AS min_salary,
                    MAX(salary) AS max_salary,
                    AVG(salary) AS avg_salary,
                    COUNT(*) AS jobs_with_salary
                FROM {self.table_name}
                WHERE salary IS NOT NULL and keyword = '{keyword}';
            """,
        }

        results = []
        for label, query in queries.items():
            data = self.run_query(query.strip())
            results.append(f"--- {label} ---\n{data}")

        return "\n\n".join(results)

    

    def fetch_all_job_ads(self):
        return self.conn.execute("SELECT * FROM job_ads").fetchall()


    def close(self):
        self.conn.close()


