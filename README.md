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
├── tools/
│   ├── init.py
│   ├── JobCrawler.py          # Crawl job ads using Crawl4AI
│   ├── logger.py              # Logging utilities
│   ├── PostgresDatabase.py    # Database connection + CRUD
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
2. **Extract structured data** using LLMs (via LangChain + Ollama)  
3. **Validate data** with Pydantic models  
4. **Store results** in PostgreSQL  
5. **Generate insights and reports** using LLMs  
6. **Export or analyze** the structured dataset  

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Langchain_JobResearch.git
cd Langchain_JobResearch

# install dependences
uv sync

## Set up your .env file:
POSTGRES_URL=your_postgres_connection_string
OLLAMA_MODEL=your_local_llm_model

---

## Usage
uv run main.py
type the keyword(e.g. AI) for searching relevant jobs.

---


## Example Output (Structured Data)
{ 'company': 'Wafer Systems Limited',
  'content': '# Sales Manager (AI Solutions)\n'
             '**Headcount opening**\n'
             '  * Sales Manager (AI Solutions)\n'
             '\n'
             '\n'
             '  \n'
             '\n'
             '**Job Responsibilities:**\n'
             '· Manage both existing sales pipeline and developing new '
             'business opportunities. Take a lead role in proposals and '
             'presentations for new business opportunities and partnerships\n'
             '  * Identify and qualify business opportunities of AI '
             'application and digitization.\n'
             '  * Demonstrate a strong ability of taking a consultative '
             'approach to sell and promote software and AI solutions to '
             'corporate and enterprise clients\n'
             '  * Define details project scope, objectives, cost, success '
             'criteria, and deliverables in collaboration with stakeholders. \n'
             '\n'
             '\n'
             '  * Collaborate with internal teams to align business '
             'development and sales efforts with product and marketing '
             'initiatives.\n'
             '  * Providing effective account management and after-sales '
             'services to customers\n'
             '  * Assisting in organizing and participating in marketing '
             'events to develop new business opportunities\n'
             '\n'
             '\n'
             '  \n'
             '\n'
             '**Job Requirements:**\n'
             '  * Higher Diploma or above in information technology, Computer '
             'Sciences, Business Administration, Marketing or any related '
             'discipline.\n'
             '  * Minimum 3 years solid experience as similar role.\n'
             '  * Experience in **Software sales** are highly preferred.\n'
             '\n'
             '\n'
             '  * Good knowledge of IT products and services, especially in AI '
             'related\n'
             '  * Good command of both written & spoken in Chinese, English, '
             'and Mandarin\n'
             '  * Aggressive, good problem-solving skills, and presentation '
             'skills\n'
             '  * Able to work independently and according to schedule\n'
             '  * Self-motivated, adaptable, and capable of thriving in a '
             'start-up environment.\n'
             '\n'
             '\n'
             '  \n'
             'We offer 5-day work, attractive basic salary + Commission, '
             'career development opportunities and other fringe benefits to '
             'the successful candidate.  \n'
             '  \n'
             '**About Wafer:**  \n'
             'Wafer Systems Limited (Wafer Systems) is an affiliate of '
             'InvesTech Holdings Limited (01087.HK). Wafer Systems Limited is '
             'an IT Solution Company with over 30 years of System integration, '
             'as well as over 20 years of independent Commercial Software '
             'Development experiences.  \n'
             '  \n'
             'Wafer Systems is based in China, facing Asia and the rest of the '
             'world, having offices in Beijing, Shanghai, Guangzhou, Chengdu, '
             'Suzhou, Shenzhen; and a software development center in Xian. The '
             'covering Business areas include Internet Infrastructure Build, '
             'Cloud and Security, Smart Office, Workspace Management and '
             'mobile workforce solutions. Wafer is a leading Next Generation '
             'System Integrator and Smart Office Solutions Provider.\n'
             '**Website:**  \n'
             'www.wafersystems.com \n'
             '**Linkedin:**  \n'
             'https://www.linkedin.com/company/wafer-systems-ltd/  \n'
             '  \n'
             '**Facebook:**  \n'
             'https://www.facebook.com/people/Wafer-Systems-Limited/100063860048453/\n'
             '**Our product:**  \n'
             '威思客 Viriscal:  \n'
             'http://www.virsical.com/en/\n'
             '_Do you want to experience IoT, Hybrid workplace solutions?_  \n'
             '  \n'
             '**_! Meta Meeting, Meta Visitor, Meta workspace !_**  \n'
             '  \n'
             "**_~Come on...let's meet up together~_**\n"
             'What’s next?\n'
             'We are actively seeking the sales professional who can meet the '
             'above abilities to join us to be a part of the long-term '
             'growth.\n'
             'Please reply directly to this posting with your CV and '
             'application. \n',
  'experiences': ['Experience in Software sales are highly preferred.'],
  'id': '90769840',
  'job_title': 'Sales Manager (AI Solutions)',
  'keyword': 'AI workflow',
  'qualifications': [ 'Higher Diploma or above in information technology, '
                      'Computer Sciences, Business Administration, Marketing '
                      'or any related discipline.',
                      'Minimum 3 years solid experience as similar role.'],
  'responsibilities': [ 'Manage both existing sales pipeline and developing '
                        'new business opportunities.',
                        'Take a lead role in proposals and presentations for '
                        'new business opportunities and partnerships',
                        'Identify and qualify business opportunities of AI '
                        'application and digitization.',
                        'Demonstrate a strong ability of taking a consultative '
                        'approach to sell and promote software and AI '
                        'solutions to corporate and enterprise clients',
                        'Define details project scope, objectives, cost, '
                        'success criteria, and deliverables in collaboration '
                        'with stakeholders.',
                        'Collaborate with internal teams to align business '
                        'development and sales efforts with product and '
                        'marketing initiatives.',
                        'Providing effective account management and '
                        'after-sales services to customers',
                        'Assisting in organizing and participating in '
                        'marketing events to develop new business '
                        'opportunities'],
  'salary': None,
  'skills': [ 'Good knowledge of IT products and services, especially in AI '
              'related',
              'Good command of both written & spoken in Chinese, English, and '
              'Mandarin',
              'Aggressive, good problem-solving skills, and presentation '
              'skills',
              'Able to work independently and according to schedule',
              'Self-motivated, adaptable, and capable of thriving in a '
              'start-up environment.'],
  'url': 'https://hk.jobsdb.com/job/90769840?type=standard',
  'working_location': None}

---

## Sample Report
Based on the provided data, here is a summary of the job market research report:

# Top 15 Job Titles
1. **AI Engineer** (44 occurrences)
2. **Product Manager** (37 occurrences)
3. **Data Scientist** (35 occurrences)
4. **Market Researcher** (32 occurrences)
5. **Software Developer** (29 occurrences)
6. **Cloud Engineer** (26 occurrences)
7. **Business Analyst** (24 occurrences)
8. **Sales Performance Analyst** (22 occurrences)
9. **Account Manager** (20 occurrences)
10. **Data Analyst** (19 occurrences)
11. **Quantitative Analyst** (18 occurrences)
12. **Marketing Specialist** (17 occurrences)
13. **Financial Analyst** (16 occurrences)
14. **Operations Research Analyst** (15 occurrences)
15. **Business Development Manager** (14 occurrences)

## Key Responsibilities
* **Project Management**: 34 occurrences
	+ Examples: "Project Planning", "Project Execution", "Project Monitoring"
* **Data Analysis**: 26 occurrences
	+ Examples: "Data Modeling", "Data Visualization", "Data Mining"
* **Technical Development**: 24 occurrences
	+ Examples: "Software Development", "Cloud Computing", "Artificial Intelligence"
* **Business Strategy**: 20 occurrences
	+ Examples: "Market Research", "Competitive Analysis", "Business Planning"
* **Sales and Marketing**: 18 occurrences
	+ Examples: "Sales Performance Management", "Marketing Campaigns", "Lead Generation"

## Common Skills
* **Programming languages**: Python (23 occurrences), Java (17 occurrences), JavaScript (14 occurrences)
* **Data analysis tools**: Excel (22 occurrences), Tableau (15 occurrences), Power BI (13 occurrences)
* **Cloud platforms**: AWS (19 occurrences), Azure (16 occurrences), Google Cloud Platform (12 occurrences)
* **Machine learning**: Artificial Intelligence (18 occurrences), Machine Learning (15 occurrences), Deep Learning (12 occurrences)

## Common Qualifications
* **Degree**: Bachelor's degree in Computer Science (34 occurrences), Master's degree in Business Administration (23 occurrences), Ph.D. in Engineering (17 occurrences)
* **Experience**: 3+ years of experience (41 occurrences), 5+ years of experience (25 occurrences)
* **Certifications**: Certified Data Scientist (15 occurrences), Certified Analytics Professional (13 occurrences)

## Common Experiences
* **Working with diverse teams**: 24 occurrences
	+ Examples: "Team Collaboration", "Project Team Management", "Cross-Functional Teams"
* **Developing software**: 23 occurrences
	+ Examples: "Software Development", "Mobile App Development", "Web Application Development"
* **Analyzing data**: 21 occurrences
	+ Examples: "Data Analysis", "Data Mining", "Data Visualization"

## Insights & Trends
1. **Growing demand for AI and machine learning professionals**
2. **Increasing importance of cloud computing and data analysis**
3. **Rise of product management and business analysis roles**
4. **Expansion of sales performance analysis and marketing specialist roles**
5. **Growing need for software development and technical expertise**

## Summary
The job market research report highlights the growing demand for AI and machine learning professionals, as well as increasing importance of cloud computing and data analysis. Product management and business analysis roles are also on the rise, while sales performance analysis and marketing specialist roles continue to expand. Software development and technical expertise remain in high demand, particularly with a focus on cloud platforms and programming languages like Python and Java.

---