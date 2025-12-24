import duckdb
import os
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

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

    def __init__(self, logger):
        # Connect to DuckDB via LangChain's SQLDatabase (uses SQLAlchemy under the hood)
        self.logger = logger
        self.folder_path = os.getenv("DB_FOLDER")
        self.db_name = os.getenv("DB_NAME")
        self.db_path = os.path.join(self.folder_path, self.db_name) # type: ignore
        self.db_uri = f"duckdb:///{self.db_path}"
        # self.db = SQLDatabase.from_uri(self.db_uri)
        self.con = duckdb.connect(database=self.db_path, read_only=True)
        
        # Ollama LLM (chat model for better structured responses)
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_LLM_MODEL"),
            temperature=0.3,  # Low temperature for analytical/factual output
        )

        self.table_name = os.getenv("DB_TABLE")

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

    # def run_query(self, query: str) -> str:
    #     """Execute a SQL query and return formatted results."""
    #     try:
    #         result = self.db.run(query)
    #         return result or "No results returned."
    #     except Exception as e:
    #         return f"Query error: {str(e)}"
    
    def run_query(self, query: str) -> str:
        try:
            result = self.con.execute(query).fetchdf()  # Returns pandas DataFrame
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

    def generate_report(self) -> str:
        """Generate and return the full job research report."""
        query_results = self.gather_insights()

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