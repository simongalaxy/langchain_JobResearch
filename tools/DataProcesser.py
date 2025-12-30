import re

def markdown_to_text(result) -> str:
    markdown_content = result.markdown
    plain_text = re.sub(r'[#*`>-]', '', markdown_content)  # remove common markdown symbols
    
    return plain_text.strip()



