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
    including pmid, title, authors, year, and abstract.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    fetch_multiplier = 3  # Fetch extra abstracts to ensure we get n relevant
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

    studies = []

    for article in root.findall(".//PubmedArticle"):
        # Extract PMID
        pmid_el = article.find(".//PMID")
        if pmid_el is None or pmid_el.text is None:
            continue
        pmid = pmid_el.text.strip()

        # Extract title
        title_el = article.find(".//ArticleTitle")
        title = title_el.text.strip() if title_el is not None else "No title"

        # Extract abstract
        abstract_el = article.find(".//Abstract/AbstractText")
        if abstract_el is None or abstract_el.text is None:
            continue
        abstract = abstract_el.text.strip()

        # Extract year
        journal_year_el = article.find(".//Journal/JournalIssue/PubDate/Year")
        year = journal_year_el.text if journal_year_el is not None else "Unknown"

        # Extract authors (up to 3)
        authors_el = article.findall(".//AuthorList/Author")
        authors = []
        for a in authors_el[:3]:
            last = a.find("LastName")
            first = a.find("ForeName")
            if last is not None and first is not None:
                authors.append(f"{first.text} {last.text}")
        authors_str = ", ".join(authors) if authors else "Unknown"

        # Append study dict
        studies.append({
            "pmid": pmid,
            "title": title,
            "authors": authors_str,
            "year": year,
            "abstract": abstract
        })

        if len(studies) >= n:
            break

    return studies[:n]

