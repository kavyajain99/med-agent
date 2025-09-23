# import os  # read env variables, like API Keys
# from dotenv import load_dotenv  # open API keys
# from langchain_openai import ChatOpenAI  # modern wrapper
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# load_dotenv() #load my env

# llm = ChatOpenAI(model="gpt-3.5-turbo")

# #the {abstract is a placeholder} to be filled in 
# template = """
# You are a medical research explainer. 
# Summarize the following PubMed abstract in plain English.
# Highlight any implications for chronic health.

# Abstract:
# {abstract}
# """

# prompt = PromptTemplate(input_variables=["abstract"], template=template)
# # tells LangChain what placeholders exist; full prompt created

# summarizer_chain = LLMChain(llm=llm, prompt=prompt) #sends it out; glues model and template together
# # data (abstract)-->insert into prompt-->send to model --> return output

# def summarize(abstracts):
#     """
#     Summarize a list of abstracts.
#     """
#     return [summarizer_chain.run(abstract=ab) for ab in abstracts]

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

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
"""
prompt = PromptTemplate(input_variables=["title","authors","year","abstract"], template=template)
summarizer_chain = LLMChain(llm=llm, prompt=prompt)

def summarize_conclusions(studies):
    """
    Summarize a list of study dictionaries.
    Each study dict has 'title','authors','year','abstract'
    """
    return [summarizer_chain.run(
        title=st["title"],
        authors=st["authors"],
        year=st["year"],
        abstract=st["abstract"]
    ) for st in studies]