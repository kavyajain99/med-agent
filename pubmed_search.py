# import requests #HTTP requests like with Jattin 
# from xml.etree import ElementTree #parse XML,kinda like the JSON proj

# def search_pubmed(query, max_results=5):
#     """
#     Search PubMed for a query and return abstracts.
#     """
#     #api URL 
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
#     search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
#     search_resp = requests.get(search_url).json() #JSON dict
#     ids = search_resp["esearchresult"]["idlist"] #saves em by the IDs

#     # Fetch details
#     fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml" #url all built up 
#     fetch_resp = requests.get(fetch_url) #get request
#     root = ElementTree.fromstring(fetch_resp.content) #beyond me... Parses the XML response into an ElementTree object, which lets you navigate the XML like a tree structure.

#     abstracts = []
#     for article in root.findall(".//AbstractText"):
#         if article.text:
#             abstracts.append(article.text)
#     return abstracts

import requests
from xml.etree import ElementTree

def search_pubmed_conclusions(query, n=5):
    """
    Search PubMed for a query and return exactly `n` conclusions,
    along with the first author and publication year.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # 1️⃣ Search for PubMed IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={n*2}&retmode=json"
    search_resp = requests.get(search_url).json()
    ids = search_resp["esearchresult"]["idlist"]
    
    if not ids:
        return [{"author": "N/A", "year": "N/A", "conclusion": "No studies found. Try another query."}] * n
    
    # 2️⃣ Fetch full abstracts in XML
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
    fetch_resp = requests.get(fetch_url)
    root = ElementTree.fromstring(fetch_resp.content)
    
    studies = []
    
    for article in root.findall(".//PubmedArticle"):
        # Extract first author
        author_elem = article.find(".//Author[1]/LastName")
        first_author = author_elem.text if author_elem is not None else "Unknown"
        
        # Extract publication year
        year_elem = article.find(".//PubDate/Year")
        if year_elem is None:
            # fallback if no Year in PubDate
            medline_date = article.find(".//PubDate/MedlineDate")
            pub_year = medline_date.text.split()[0] if medline_date is not None else "Unknown"
        else:
            pub_year = year_elem.text
        
        # Extract conclusion section
        conc_texts = [t.text for t in article.findall(".//AbstractText[@Label='CONCLUSIONS']") if t.text]
        if conc_texts:
            conclusion = " ".join(conc_texts)
        else:
            # Fallback: last section of abstract
            all_sections = [t.text for t in article.findall(".//AbstractText") if t.text]
            conclusion = all_sections[-1] if all_sections else "No clear conclusion provided in this study."
        
        studies.append({"author": first_author, "year": pub_year, "conclusion": conclusion})
    
    # Ensure exactly n results
    if len(studies) < n:
        studies += [{"author": "N/A", "year": "N/A", "conclusion": "No conclusion available."}] * (n - len(studies))
    else:
        studies = studies[:n]
    
    return studies
