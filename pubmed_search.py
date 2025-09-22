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

def search_pubmed_conclusions(query, max_results=5):
    """
    Search PubMed for a query and return only conclusions from abstracts.
    If a conclusion section is not found, fallback to full abstract text.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # Step 1: Search PubMed for IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    search_resp = requests.get(search_url).json()
    ids = search_resp["esearchresult"]["idlist"]

    if not ids:
        return []

    # Step 2: Fetch detailed records
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
    fetch_resp = requests.get(fetch_url)
    root = ElementTree.fromstring(fetch_resp.content)

    conclusions = []

    # Extract labeled conclusions
    for article in root.findall(".//AbstractText"):
        label = article.attrib.get("Label", "").lower()
        if label in ("conclusion", "conclusions") and article.text:
            conclusions.append(article.text)

    # Fallback: if no labeled conclusion, use full abstract
    if not conclusions:
        for article in root.findall(".//AbstractText"):
            if article.text:
                conclusions.append(article.text)

    return conclusions
