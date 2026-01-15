import os
from pathlib import Path
import textwrap

def write_report(keyword: str, markdown: str) -> str:
    
    # generate filename by daily press release url.
    
    filename = f"Job_Report_keyword-{keyword}.txt"
    filepath = "./reports/"
    
    # define the desired page width.
    width_limit = 70
    formatted_text = textwrap.fill(textwrap.dedent(markdown).strip(), width=width_limit)
    

    # generate report in text file.
    with open(os.path.join(filepath, filename), "w", encoding="utf-8") as file:
        file.write(formatted_text + "\n")
        
    return filename
        