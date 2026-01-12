# app.py
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Correct LangChain Imports
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain             # <--- MUST NOT BE langchain_core
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
