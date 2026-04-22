import os
from pathlib import Path
import textwrap
from datetime import datetime

def write_report(keyword: str, markdown: str) -> str:
    
    # generate filename by daily press release url.
    # Get current date and time
    now = datetime.now()

    # Format as text
    current_time_text = now.strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"Job_Report_keyword_{keyword}_{current_time_text}.md"
    filepath = "./reports/"
    
    os.makedirs(filepath, exist_ok=True)
    
    # generate report in text file.
    with open(os.path.join(filepath, filename), "w", encoding="utf-8") as file:
        file.write(markdown + "\n")
        
    return filename
        