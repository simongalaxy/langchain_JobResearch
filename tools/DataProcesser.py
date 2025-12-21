import re

def markdown_to_text(result) -> str:

    markdown_content = result.markdown
    plain_text = re.sub(r'[#*`>-]', '', markdown_content)  # remove common markdown symbols
    
    return plain_text.strip()


def get_unique_jobAds_by_id(jobAds):
    
    seen = set()
    unique_jobAds = []
    
    for job in jobAds:
        job_id = job.url.split("?")[0].split("/")[-1]
        if job_id not in seen:
            seen.add(job_id)
            unique_jobAds.append(job)
    
    return unique_jobAds

def get_job_id(job) -> str:
    return job.url.split("?")[0].split("/")[-1]
