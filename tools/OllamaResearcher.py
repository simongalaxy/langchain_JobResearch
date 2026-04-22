from ollama import Client   # Native Ollama client
import psycopg2
import psycopg2.extras
from pprint import pformat
import json
import os
from dotenv import load_dotenv
load_dotenv()

from tools.writeReport import write_report

class OllamaResearcher:
    def __init__(self, logger):
        self.logger = logger

        # Database connection (using psycopg2 directly - faster & safer)
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.db_name = os.getenv("db_name")

        if not all([self.username, self.password, self.host, self.port, self.db_name]):
            raise ValueError("Missing database credentials in .env")

        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.conn.autocommit = True

        # Ollama setup
        self.model_name = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.client = Client()   # or AsyncClient() if you want async

        self.logger.info(f"Ollama Researcher initialized with model: {self.model_name}")


    def _get_top_job_titles(self, keyword: str, limit: int = 15):
        query = """
            SELECT job_title, COUNT(*) as count
            FROM public.jobad
            WHERE keyword = %s AND job_title IS NOT NULL
            GROUP BY job_title
            ORDER BY count DESC
            LIMIT %s;
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (keyword, limit))
            return cur.fetchall()


    def _get_top_items(self, keyword: str, column: str, limit: int = 20):
        query = f"""
            SELECT element, COUNT(*) as freq
            FROM (
                SELECT unnest({column}) AS element
                FROM public.jobad
                WHERE keyword = %s 
                  AND {column} IS NOT NULL 
                  AND array_length({column}, 1) > 0
            ) sub
            WHERE element IS NOT NULL AND TRIM(element) != ''
            GROUP BY element
            ORDER BY freq DESC
            LIMIT %s;
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (keyword, limit))
            return cur.fetchall()


    def generate_job_market_report(self, keyword: str) -> None:
        self.logger.info(f"Generating job market report for keyword: '{keyword}'")

        try:
            # 1. Fetch data efficiently
            job_titles = self._get_top_job_titles(keyword, 10)
            skills = self._get_top_items(keyword, "skills", 10)
            responsibilities = self._get_top_items(keyword, "responsibilities", 20)
            qualifications = self._get_top_items(keyword, "qualifications", 5)
            experiences = self._get_top_items(keyword, "experiences", 5)

            total_jobs = sum(row["count"] for row in job_titles)

            # 2. Prepare clean insights (much smaller than before)
            insights = {
                "keyword": keyword,
                "total_jobs": total_jobs,
                "top_job_titles": [{"title": r["job_title"], "count": r["count"]} for r in job_titles],
                "top_skills": [{"skill": r["element"], "count": r["freq"]} for r in skills],
                "top_responsibilities": [{"item": r["element"], "count": r["freq"]} for r in responsibilities],
                "top_qualifications": [{"item": r["element"], "count": r["freq"]} for r in qualifications],
                "top_experiences": [{"item": r["element"], "count": r["freq"]} for r in experiences]
            }

            # 3. Strong system + user prompt
            system_prompt = "You are a precise, data-driven job market analyst. Generate reports using ONLY the provided data. Never invent information."

            user_prompt = f"""Generate a professional Job Market Research Report based on the following data.

            Data:
            {json.dumps(insights, indent=2, ensure_ascii=False)}

            Rules:
            - Use only the exact items and counts from the data above.
            - Do not add any job titles, skills, or experiences that are not listed.
            - Be factual and specific.
            - Output in clean Markdown format.

            Return the full report in Markdown.
            """

            # 4. Call Ollama directly
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.0,      # Very important for factual report
                    "num_ctx": 16384,
                    "num_predict": 4096,     # Allow long report
                }
            )

            report_text = response['message']['content']
            write_report(keyword=keyword, markdown=report_text)
            self.logger.info("#"*50)
            self.logger.info("Report generated: \n%s", report_text)
            self.logger.info("#"*50)
            
            return

        except Exception as e:
            self.logger.error(f"Failed to generate report for '{keyword}': {e}")
            raise

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.logger.info("Database connection closed.")