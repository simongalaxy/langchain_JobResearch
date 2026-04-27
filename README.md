# 🧠 AI‑Powered Job Research Pipeline  
High‑performance async pipeline for crawling, extracting, analyzing, and summarizing job postings using lightweight Ollama models and PostgreSQL JSONB storage.

---

## 🚀 Overview

This project is a fully asynchronous, modular job‑research system designed for **speed**, **clarity**, and **maintainability**.  
It crawls job postings, extracts structured information, generates insights, and stores everything in PostgreSQL using a clean Pydantic‑based architecture.

Key design principles:
- **No ORM overhead** → direct PostgreSQL JSONB  
- **No LangChain** → direct Ollama calls for maximum speed  
- **No class overlap** → strict separation of concerns  
- **Async end‑to‑end** → fast, scalable pipeline  
- **Pydantic state models** → clean, typed, validated data flow  

---

## 🧩 Architecture

The system follows a lightweight, LangGraph‑inspired state‑based design:



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

### 🦙 Ollama
- Runs LLMs locally for **privacy** and **zero cost**  
- Extracts structured data from unstructured text with asyncio to speed up the extraction process.
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

## 🧠 Model Selection

This project uses two lightweight Ollama models with clear functional separation:

### **1. MiniMistral‑3:3B — Inference‑Driven Summarization**
- Designed for interpretive understanding of job descriptions
- Strong at identifying implicit skills and experience not explicitly stated
- Produces natural, narrative summaries instead of rigid JSON

- Ideal for:
  - summarizing required skills (explicit + inferred)
  - summarizing experience level and role expectations
  - extracting soft skills from context
  - generating human‑readable job overviews


### **2. phi4:mini — Reasoning & Report Generation**
- Small model with strong reasoning  
- Fast summarization  
- Ideal for generating:  
  - job summaries  
  - insights  
  - skill analysis  
  - market‑fit reports  

***Why this combination?***  
**Both MiniMistral‑3:3B and Phi‑4 Mini — Optimized for MLX Acceleration**
- Both models run significantly faster when executed through Ollama with the MLX backend
- MLX provides lower latency, better memory efficiency, and higher throughput on Apple Silicon
- Ideal for high‑concurrency pipelines where you need fast inference without sacrificing quality

---


## 📁 Project Structure

Langchain_JobResearch/
│
├── logs/                      # save the log files
├── reports/                   # save report generated. 
├── tools/
│   ├── logger.py              # Logging utilities
│   ├── DataClass.py           # Define pydantic classes to store data in different stages with validation
│   ├── webCrawler.py          # Crawl job ads using Crawl4AI
│   ├── OllamaSummarizer.py    # LLM-based job ad information extractor using Ollama LLM Model - nuextract
│   ├── DBHandler.py           # Postgresql Database connection + CRUD
│   └── OllamaResearcher.py      # LLM-based insights report generation using Ollama LLM Model - phi4:mini
│
├── main.py                    # Main entry point
├── .env                       # Environment variables
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md

---

## 🏗️ Main Components

### WebCrawler
- Async Playwright‑based Crawl4AI
- Timeout + retry watchdog
- Outputs CrawlResult (Pydantic)

### OllamaSummarizer
- Uses nuextract for structured extraction
- Outputs ExtractedData (Pydantic)

### OllamaResearcher
- Uses phi4:mini for summarization & insights
- Outputs Text file in markdown format

### DBHandler
- Direct PostgreSQL
- No ORM
- Fast, flexible, schema‑light

---

## 🚀 How It Works

1. **Crawl job advertisement webpages** using Crawl4AI  
2. **Extract structured data** using LLMs with Ollama
3. **Validate data** with Pydantic models  
4. **Store results** in PostgreSQL  
5. **Generate insights and reports** using LLMs with Ollama

---

## 🛠️ Installation and Usage

Clone the repository:

git clone https://github.com/yourusername/Langchain_JobResearch.git
cd Langchain_JobResearch

# install dependences
uv sync

# pull ollama LLM models
ollama pull ministral-3:3b 
ollama pull phi4-mini

## Set up your .env file:
POSTGRES_URL=your_postgres_connection_string
OLLAMA_EXTRACTION_MODEL = ministral-3:3b
OLLAMA_SUMMARIZATION_MODEL = phi4-mini:latest

## Usage
uv run main.py
type the keyword(e.g. AI) for searching relevant jobs.

---

## 📌 Performance Notes
- Crawl4AI / Playwright may occasionally freeze under heavy load
- A retry + timeout wrapper is included to ensure stability
- Async Ollama calls significantly reduce LLM latency
- Removing ORM + LangChain reduces overhead and improves throughput

---