import os
from pathlib import Path
import textwrap

def write_report(keyword: str, markdown: str) -> str:
    
    # generate filename by daily press release url.
    filename = f"Job_Report_keyword-{keyword}.md"
    filepath = "./reports/"
    
    # generate report in text file.
    with open(os.path.join(filepath, filename), "w", encoding="utf-8") as file:
        file.write(markdown + "\n")
        
    return filename
        