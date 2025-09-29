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

def search_pubmed_conclusions(query, n=5, advanced_query=None):
    """
    Search PubMed for a query and optional advanced query.
    Returns top `n` study conclusions with pmid, title, authors, year, abstract.
    """
    def fetch_studies(q, limit):
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        fetch_multiplier = 3
        retmax = limit * fetch_multiplier

        # Step 1: Search IDs
        search_url = f"{base_url}esearch.fcgi?db=pubmed&term={q}&retmax={retmax}&retmode=json"
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
            pmid_el = article.find(".//PMID")
            if pmid_el is None or pmid_el.text is None:
                continue
            pmid = pmid_el.text.strip()

            title_el = article.find(".//ArticleTitle")
            title = title_el.text.strip() if title_el is not None else "No title"

            abstract_el = article.find(".//Abstract/AbstractText")
            if abstract_el is None or abstract_el.text is None:
                continue
            abstract = abstract_el.text.strip()

            journal_year_el = article.find(".//Journal/JournalIssue/PubDate/Year")
            year = journal_year_el.text if journal_year_el is not None else "Unknown"

            authors_el = article.findall(".//AuthorList/Author")
            authors = []
            for a in authors_el[:3]:
                last = a.find("LastName")
                first = a.find("ForeName")
                if last is not None and first is not None:
                    authors.append(f"{first.text} {last.text}")
            authors_str = ", ".join(authors) if authors else "Unknown"

            studies.append({
                "pmid": pmid,
                "title": title,
                "authors": authors_str,
                "year": year,
                "abstract": abstract
            })

            if len(studies) >= limit:
                break

        return studies[:limit]

    # Fetch primary query results
    primary_studies = fetch_studies(query, n)

    # Fetch advanced query results if provided
    if advanced_query:
        advanced_studies = fetch_studies(advanced_query, n)
        # Merge and remove duplicates by pmid
        combined = {s['pmid']: s for s in primary_studies + advanced_studies}
        return list(combined.values())[:n]

    return primary_studies
