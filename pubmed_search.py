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
    Search PubMed for a query and return top `n` study conclusions,
    including title, authors, and year. Automatically fetches extra abstracts
    to ensure we always get n summaries.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    fetch_multiplier = 3  # Fetch extra abstracts to ensure we get n relevant

    studies = []
    retmax = n * fetch_multiplier

    # Step 1: Search IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={retmax}&retmode=json"
    search_resp = requests.get(search_url).json()
    ids = search_resp["esearchresult"]["idlist"]
    if not ids:
        return []

    # Step 2: Fetch details
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
    fetch_resp = requests.get(fetch_url)
    root = ElementTree.fromstring(fetch_resp.content)

    for article in root.findall(".//PubmedArticle"):
        title_el = article.find(".//ArticleTitle")
        abstract_el = article.find(".//Abstract/AbstractText")
        journal_year_el = article.find(".//Journal/JournalIssue/PubDate/Year")
        authors_el = article.findall(".//AuthorList/Author")

        if abstract_el is None or abstract_el.text is None:
            continue

        # Extract authors
        authors = []
        for a in authors_el:
            last = a.find("LastName")
            first = a.find("ForeName")
            if last is not None and first is not None:
                authors.append(f"{first.text} {last.text}")
        year = journal_year_el.text if journal_year_el is not None else "Unknown"

        studies.append({
            "title": title_el.text if title_el is not None else "No title",
            "abstract": abstract_el.text,
            "authors": ", ".join(authors) if authors else "Unknown",
            "year": year
        })

        if len(studies) >= n:
            break

    return studies[:n]
