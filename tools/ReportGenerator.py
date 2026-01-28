from pprint import pformat
import os
from dotenv import load_dotenv
load_dotenv()
import ast

from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_classic.prompts import PromptTemplate


class ReportGenerator:
    def __init__(self, logger):
        
        # declaring logger.
        self.logger = logger
        
        # declare database connection parameters.
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port") 
        self.db_name = os.getenv("db_name")
        self.db_uri = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.db = SQLDatabase.from_uri(self.db_uri)
        
        # set up llm.
        self.model_name = os.getenv("OLLAMA_LLM_MODEL")
        self.llm = ChatOllama(model=self.model_name, temperature=0.7)
        
        # set up prompt template for report generation.
        self.report_prompt = PromptTemplate(
                input_variables=["insights"],
                template="""
                You are generating a job market research report.

                Use ONLY the data provided in the JSON input. 
                Do NOT invent job titles, responsibilities, skills, qualifications, or experiences that are not explicitly present in the input.

                Your task:
                1. Summarize the top job titles exactly as provided, preserving counts.
                2. Identify the most common responsibilities, skills, qualifications, and experiences based strictly on frequency in the input.
                3. Write a detailed and comprehensive analytical report that reflects the dataset, not general industry knowledge.
                4. Avoid generic statements unless they are supported by the data.
                5. Do not add job titles that are not in the input.

                Input data:
                {insights}

                Output format (Markdown):
                # Job Market Research Report

                ## Top Job Titles
                (List exactly as provided, with counts in descending order)

                ## Key Responsibilities
                (Categorize and summarize based on top 10 frequency with at least 4 to 5 examples by categories; no invented items; Only from the dataset)

                ## Common Skills
                (Categorize and summarize based on top 10 frequency with at least 4 to 5 examples by categories; no invented items; Only from the dataset)

                ## Common Qualifications
                (Categorize and summarize based on top 10 frequency with at least 4 to 5 examples by categories; no invented items; Only from the dataset)

                ## Common Experiences
                (Categorize and summarize based on top 10 frequency with at least 4 to 5 examples by categories; no invented items; Only from the dataset)

                ## Insights & Trends
                (Highlight patterns visible in the data only)
                
                ## Summary
                (A short, factual conclusion)
                """
            )
        
        self.logger.info("Report Generator for keyword - {self.keyword} started.")

    # Function to generate the report
    def generate_job_market_report(self, keyword: str):
        # Use agent to query DB for key insights (add more queries as needed)
        
        items = ["Job Title", "Responsiblities", "Skills", "Qualifications", "Experiences"]
        queries = [
                f"""
                SELECT job_title, COUNT(id) AS count
                FROM public.jobad
                WHERE job_title IS NOT NULL
                AND keyword = '{keyword}'
                GROUP BY job_title
                ORDER BY count DESC
                LIMIT 5;
                """,
    
                f"""
                SELECT unnest(skills) AS element
                FROM public.jobad
                WHERE array_length(skills, 1) > 0
                AND keyword = '{keyword}';
                """,

                f"""
                SELECT unnest(qualifications) AS element
                FROM public.jobad
                WHERE array_length(qualifications, 1) > 0
                AND keyword = '{keyword}';
                """,

                f"""
                SELECT unnest(responsibilities) AS element
                FROM public.jobad
                WHERE array_length(responsibilities, 1) > 0
                AND keyword = '{keyword}';
                """,

                f"""
                SELECT unnest(experiences) AS element
                FROM public.jobad
                WHERE array_length(experiences, 1) > 0
                AND keyword = '{keyword}';
                """
            ]

        insights = {}
        
        for item, query in zip(items, queries):
            result = self.db.run(query)
            text = "\n".join(t[0] for t in ast.literal_eval(result) if t[0] is not None)
            insights[item] = text

        # self.logger.info(f"insights: \n%s", pformat(insights))
        
        # Chain to generate the full report using the prompt
        report_chain = self.report_prompt | self.llm  # Simple chain: prompt -> LLM
        report = report_chain.invoke({"insights": insights})
        
        return report.content  # Or report if using other LLM output format

