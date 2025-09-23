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

import streamlit as st
from pubmed_search import search_pubmed_conclusions
from summarizer import summarize_conclusions

st.set_page_config(page_title="Health Research Agent", layout="wide")

st.title("🩺 Health Research Agent")
st.write("Enter a health topic and get PubMed research conclusions summarized in plain English.")

query = st.text_input("Search PubMed for:")
max_results = st.slider("Number of studies:", 1, 10, 5)

if st.button("Summarize Research"):
    if not query:
        st.error("Please enter a search query.")
    else:
        with st.spinner("Fetching and summarizing..."):
            conclusions = search_pubmed_conclusions(query, n=max_results)

            
            if not conclusions:
                st.warning("No conclusions found. Try another query.")
            else:
                summaries = summarize_conclusions(conclusions)
                for i, s in enumerate(summaries, 1):
                    st.subheader(f"Study {i} Summary")
                    st.write(s)
