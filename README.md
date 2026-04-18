# 🧠 Job Research AI — Automated Job Ad Extraction & Insights

A fully automated pipeline that crawls job advertisement webpages, extracts structured information using LLMs, and generates insights and reports.  
Built for fast, accurate, and scalable analysis of job market trends.

---

## 🌟 Motivation

Researching roles such as *AI Engineer* or *Data Analyst* requires manually reading large numbers of job advertisements. This is slow and inefficient because:

- Job ads have **no consistent format**
- Key information (skills, responsibilities, salary, experience) is often missing or scattered
- Traditional scraping and parsing techniques **struggle with unstructured text**

To solve this, the project uses **LLMs**, **Crawl4AI**, **Pydantic**, and **PostgreSQL** to extract structured data from messy webpages — automatically and reliably.

---

## 🎯 What Problem Does This Project Solve?

This system converts **unstructured job advertisement webpages** into **clean, structured data**, including:

- Job title  
- Company name  
- Responsibilities  
- Required skills  
- Qualifications  
- Experience  
- Salary  
- Location  

It then uses LLMs to generate **insights and reports** based on the extracted data.

Traditional scraping cannot handle unstructured text effectively.  
LLMs *can* — and this project uses them in a controlled, typed, and production‑safe way.

---

## 🧰 Technologies Used

### 🕷️ Crawl4AI
- Crawls job advertisement webpages efficiently  
- Supports asynchronous crawling  
- Integrates with LLMs for extraction  
- Fast and reliable for large‑scale scraping  

### 🔗 LangChain
- Provides a clean interface to communicate with LLMs  
- Handles prompts, models, and structured output  

### 🦙 Ollama
- Runs LLMs locally for **privacy** and **zero cost**  
- Extracts structured data from unstructured text  
- Generates insights and reports  

### 🐘 PostgreSQL
- Stores extracted job data  
- Supports complex data types (e.g., lists)  
- Reliable, scalable, and production‑ready  

### 🧩 Pydantic
- Ensures extracted data matches strict schemas  
- Validates types before inserting into the database  

### ⚡ Asyncio
- Enables concurrent crawling and extraction  
- Significantly speeds up processing time  

---

## 📁 Project Structure

Langchain_JobResearch/
│
├── logs/                      # save the log files
├── reports/                   # save report generated. 
├── tools/
│   ├── init.py
│   ├── logger.py              # Logging utilities
│   ├── DataClass.py           # Define pydantic classes to store data in different stages with validation
│   ├── WebCrawler.py          # Crawl job ads using Crawl4AI
│   ├── JobSummarizer.py       # LLM-based job ad information extractor
│   ├── DBHandler.py           # Postgresql Database connection + CRUD
│   ├── writeReport.py         # Write insights to file
│   └── ReportGenerator.py     # LLM-based insights generation
│
├── main.py                    # Main entry point
├── .env                       # Environment variables
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md



---

## 🚀 How It Works

1. **Crawl job advertisement webpages** using Crawl4AI  
2. **Extract structured data** using LLMs (via Ollama)  
3. **Validate data** with Pydantic models  
4. **Store results** in PostgreSQL  
5. **Generate insights and reports** using LLMs with LangChain and Ollama

---

## 🛠️ Installation and Usage

Clone the repository:

git clone https://github.com/yourusername/Langchain_JobResearch.git
cd Langchain_JobResearch

# install dependences
uv sync

## Set up your .env file:
POSTGRES_URL=your_postgres_connection_string
OLLAMA_MODEL=your_local_llm_model

## Usage
uv run main.py
type the keyword(e.g. AI) for searching relevant jobs.

---

