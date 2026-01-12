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

# 2. PubMed Search Logic
def search_pubmed(query, max_results=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    q_encoded = quote(query)
    
    # Step 1: Search IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={q_encoded}&retmax={max_results}&retmode=json"
    try:
        search_resp = requests.get(search_url).json()
        ids = search_resp.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        # Step 2: Fetch Details
        fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
        fetch_resp = requests.get(fetch_url)
        root = ElementTree.fromstring(fetch_resp.content)
        
        articles = []
        for article in root.findall(".//PubmedArticle"):
            pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else ""
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
            abstract_text = ""
            for abs_part in article.findall(".//AbstractText"):
                if abs_part.text:
                    abstract_text += abs_part.text + " "
            
            if abstract_text:
                articles.append({"pmid": pmid, "title": title, "abstract": abstract_text.strip()})
        return articles
    except Exception as e:
        st.error(f"Error fetching PubMed data: {e}")
        return []

# 3. AI Model & Chain Setup (Modern Syntax)
if OPENAI_API_KEY:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    template = """
    You are a medical research explainer. 
    Summarize the following PubMed abstract in plain, easy-to-understand English.
    Highlight the key findings and potential health implications.

    Title: {title}
    Abstract: {abstract}
    """
    
    prompt = PromptTemplate.from_template(template)
    
    # This replaces the broken LLMChain
    summarize_chain = prompt | llm | StrOutputParser()
else:
    st.error("OPENAI_API_KEY not found. Please check your environment variables.")

# 4. Streamlit UI
st.set_page_config(page_title="Med-Agent AI", layout="wide")
st.title("🩺 Med-Agent AI Assistant")
st.write("Summarizing medical research into plain English.")

query = st.text_input("Enter a health topic (e.g., 'Mediterranean diet and heart health'):")
max_studies = st.slider("Number of studies:", 1, 5, 3)

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please enter a search term.")
    else:
        with st.spinner("Searching PubMed and generating summaries..."):
            results = search_pubmed(query, max_results=max_studies)
            
            if not results:
                st.warning("No research found for that topic.")
            else:
                for i, study in enumerate(results, 1):
                    # Run the modern chain
                    summary = summarize_chain.invoke({
                        "title": study["title"],
                        "abstract": study["abstract"]
                    })
                    
                    st.subheader(f"Study {i}: {study['title']}")
                    st.markdown(f"**Source:** [PubMed Link](https://pubmed.ncbi.nlm.nih.gov/{study['pmid']}/)")
                    st.write(summary)
                    st.divider()

# Footer Medical Disclaimer
st.caption("Disclaimer: This tool provides summaries of research for informational purposes only. Always consult a medical professional for health advice.")