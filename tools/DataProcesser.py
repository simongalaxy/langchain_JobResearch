import re

def markdown_to_text(result) -> str:

    markdown_content = result.markdown
    plain_text = re.sub(r'[#*`>-]', '', markdown_content)  # remove common markdown symbols
    
    return plain_text.strip()


def remove_duplicates_by_id(jobAds) -> list[dict]:
    
    seen = set()
    unique_jobAds = []
    for job in jobAds:
        job_id = job.url.split("?")[0].split("/")[-1]
        if job_id not in seen:
            seen.add(job_id)
            dict = {
                "job_id": job_id,
                "jobAd": job
            }
            unique_jobAds.append(dict)
    
    return unique_jobAds