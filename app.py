import os
import requests
import streamlit as st
from dotenv import load_dotenv
from xml.etree import ElementTree
from urllib.parse import quote

# 1. Setup & Environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangChain Modern Imports
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 2. PubMed Search Logic (Now extracts Authors and Year)
def search_pubmed_conclusions(query, n=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    q_encoded = quote(query)
    
    # Step 1: Search IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={q_encoded}&retmax={n}&retmode=json"
    try:
        search_resp = requests.get(search_url).json()
        ids = search_resp.get("esearchresult", {}).get("idlist", [])
        if not ids: return []

        # Step 2: Fetch Details
        fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
        fetch_resp = requests.get(fetch_url)
        root = ElementTree.fromstring(fetch_resp.content)
        
        studies = []
        for article in root.findall(".//PubmedArticle"):
            # Extract basic info
            pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else ""
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
            
            # Extract Year
            year_el = article.find(".//Journal/JournalIssue/PubDate/Year")
            year = year_el.text if year_el is not None else "Unknown Year"
            
            # Extract Authors (First 3)
            authors_list = []
            for auth in article.findall(".//Author")[:3]:
                last = auth.find("LastName")
                first = auth.find("ForeName")
                if last is not None and first is not None:
                    authors_list.append(f"{first.text} {last.text}")
            authors_str = ", ".join(authors_list) if authors_list else "Unknown Author"

            # Extract Abstract
            abstract_text = ""
            for abs_part in article.findall(".//AbstractText"):
                if abs_part.text:
                    abstract_text += abs_part.text + " "
            
            if abstract_text:
                studies.append({
                    "pmid": pmid, 
                    "title": title, 
                    "authors": authors_str, 
                    "year": year, 
                    "abstract": abstract_text.strip()
                })
        return studies
    except Exception as e:
        st.error(f"Error fetching PubMed data: {e}")
        return []

# 3. AI Setup with YOUR Specific Template
if OPENAI_API_KEY:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5) # Using your 0.5 temp
    
    template = """
    You are a medical research explainer. 
    Summarize the following PubMed study conclusion in easy to understand English.
    Include implications for health & actionable solutions. 
    Be sure to include the primary author and year of the study.
    It is integral you mention how it is relevant to what the query term was. 

    Title: {title}
    Authors: {authors}
    Year: {year}
    Conclusion: {abstract}
    Query: {query}
    """
    
    prompt = PromptTemplate(
        input_variables=["title", "authors", "year", "abstract", "query"],
        template=template
    )
    
    # The modern "Chain"
    summarizer_chain = prompt | llm | StrOutputParser()

# 4. The Summarization Helper (Like your original version)
def summarize_conclusions(studies, query_term):
    summaries = []
    for st_dict in studies:
        # Run the chain using .invoke
        summary = summarizer_chain.invoke({
            "title": st_dict["title"],
            "authors": st_dict["authors"],
            "year": st_dict["year"],
            "abstract": st_dict["abstract"],
            "query": query_term
        })
        
        # Build the header with the PubMed link exactly like your example
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{st_dict['pmid']}/"
        linked_header = f"### [**{st_dict['title']}** ({st_dict['authors']}, {st_dict['year']})]({pubmed_url})"
        
        summaries.append(f"{linked_header}\n\n{summary}")
    return summaries

# 5. Streamlit UI
st.set_page_config(page_title="Health Research Agent", layout="wide")
st.title("🩺 Health Research Agent")
st.write("Enter a health topic and get PubMed research summaries in plain English.")

query = st.text_input("Search PubMed for:")
max_results = st.slider("Number of studies:", 1, 10, 5)

if st.button("Summarize Research"):
    if not query:
        st.error("Please enter a search query.")
    else:
        with st.spinner("Fetching and summarizing..."):
            studies = search_pubmed_conclusions(query, n=max_results)
            
            if not studies:
                st.warning("No studies found. Try another query.")
            else:
                summaries = summarize_conclusions(studies, query)
                for s in summaries:
                    st.markdown(s)
                    st.divider()

# Footer
st.caption("Disclaimer: This tool provides summaries of research for informational purposes only. Always consult a medical professional.")