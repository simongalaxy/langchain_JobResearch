from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase


from tools.PostgresDatabase import PostgresDBHandler

import os
from dotenv import load_dotenv
load_dotenv()

class JobResearchReportGenerator:
    """
    A class to generate an analytical job research report from job data stored in DuckDB.
    It uses Ollama (local LLM) via LangChain to query the database, extract insights,
    and write a concise report based strictly on the data.

    Assumptions about your DuckDB schema:
    - You have a table named 'jobs' (adjust if different).
    - Relevant columns: job_title, company, responsibilities (text), qualifications (text),
      experience (text or years), skills (text, possibly comma-separated or array),
      salary (numeric or text range), location (text).

    If your table/column names differ, update the PROMPT_TEMPLATE accordingly.
    """
    
    def __init__(self, logger, Handler: PostgresDBHandler):
        # Connect to DuckDB via LangChain's SQLDatabase (uses SQLAlchemy under the hood)
        self.logger = logger
        self.PsqlHandler = Handler
        self.table_name = os.getenv("db_name")
        
        # Ollama LLM (chat model for better structured responses)
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_LLM_MODEL"),
            temperature=0,  # Low temperature for analytical/factual output
        )

        # Comprehensive prompt that guides the LLM to extract all required insights in one go
        self.PROMPT_TEMPLATE = f"""
        You are an expert job market analyst. Using only the data from the provided SQL query results,
        produce a concise, analytical job research report in clear paragraphs.

        Key requirements:
        - Summarize overall hiring trends (e.g., most common job titles, dominant companies, locations).
        - Highlight the most requested skills (top 5–10, with counts if possible).
        - Identify experience level patterns (e.g., junior/mid/senior distribution, average years required).
        - Mention salary ranges if salary data is available; otherwise state that salary information is unavailable.
        - Keep the tone professional, analytical, and concise.
        - Do NOT invent, assume, or hallucinate any data. Base everything strictly on the provided results.
        - If certain information is missing or insufficient, explicitly state it (e.g., "Salary data is unavailable in the dataset").
        - Structure the report with paragraphs, no bullet points or headings unless natural.

        The dataset contains job advertisements in the table `{self.table_name}`.

        Here are key analytical SQL query results (each section is labeled):

        {{query_results}}

        Write the final report now.
        """

        self.prompt = PromptTemplate.from_template(self.PROMPT_TEMPLATE)


    def generate_report(self, keyword: str) -> str:
        """Generate and return the full job research report."""
        query_results = self.DBHandler.gather_insights(keyword=keyword)
        chain = self.prompt | self.llm | StrOutputParser()
        report = chain.invoke({"query_results": query_results})

        return report


# # Example usage:
# if __name__ == "__main__":
#     generator = JobResearchReportGenerator(
#         db_path="path/to/your/jobs.duckdb",  # Update with your actual file path
#         table_name="jobs",                   # Update if your table has a different name
#         ollama_model="llama3.2",             # Your pulled Ollama model
#     )

#     report = generator.generate_report()
#     print(report)