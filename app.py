# import streamlit as st
# from pubmed_search import search_pubmed #my own 
# from summarizer import summarize # mine 

# #main page
# st.set_page_config(page_title="Health Research Agent", layout="wide")

# #H1
# st.title("🩺 Health Research Agent")
# #body 
# st.write("Enter a health topic and get PubMed research summaries in plain English.")

# #textbox
# query = st.text_input("Search PubMed for:")
# #min, max, default 
# max_results = st.slider("Number of studies:", 1, 10, 5)

# #basically a super functional try catch 
# if st.button("Summarize Research"):
#     if not query:
#         st.error("Please enter a search query.")
#     else:
#         with st.spinner("Fetching and summarizing..."):
#             abstracts = search_pubmed(query, max_results=max_results)
            
#             if not abstracts:
#                 st.warning("No abstracts found. Try another query.")
#             else:
#                 summaries = summarize(abstracts)
#                 for i, s in enumerate(summaries, 1):
#                     st.subheader(f"Study {i}")
#                     st.write(s)

# import streamlit as st
# from pubmed_search import search_pubmed_conclusions
# from summarizer import summarize_conclusions

# st.set_page_config(page_title="Health Research Agent", layout="wide")
# st.title("🩺 Health Research Agent")
# st.write("Enter a health topic and get PubMed research conclusions summarized in plain English.")

# query = st.text_input("Search PubMed for:")
# advanced_query = st.text_input("Advanced/optional search query (e.g., more specific terms):")
# max_results = st.slider("Number of studies:", 1, 10, 5)

# if st.button("Summarize Research"):
#     if not query:
#         st.error("Please enter a search query.")
#     else:
#         # Combine queries if advanced query is provided
#         combined_query = f"{query} AND {advanced_query}" if advanced_query else query

#         with st.spinner("Fetching and summarizing..."):
#             conclusions = search_pubmed_conclusions(combined_query, n=max_results)
            
#             if not conclusions:
#                 st.warning("No conclusions found. Try another query.")
#             else:
#                 summaries = summarize_conclusions(conclusions)
#                 for i, s in enumerate(summaries, 1):
#                     st.subheader(f"Study {i}")
#                     st.write(s)

# app.py
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment")

# LangChain imports
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# Your own modules
# from pubmed_search import search_pubmed  # Uncomment if using
# from summarizer import summarize_conclusions  # Uncomment if using

# Initialize ChatOpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# Example usage: simple prompt
prompt = PromptTemplate(
    input_variables=["name"],
    template="Hello {name}, how are you today?"
)
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit app
st.title("Med-Agent AI Assistant")

name_input = st.text_input("Enter your name:", "Kavya")
if st.button("Greet"):
    response = chain.run({"name": name_input})
    st.write(response)

# Example for your summarizer/pubmed workflow
# st.text_area("Enter text to summarize:")
# if st.button("Summarize"):
#     summary = summarize_conclusions(input_text)
#     st.write(summary)
