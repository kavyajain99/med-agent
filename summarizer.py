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
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# Use GPT-3.5 for low-cost testing
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# Prompt now asks to summarize conclusions only
template = """
You are a medical research explainer. 
Summarize the following PubMed conclusion in plain English.
Highlight any implications for chronic health, and make it actionable and consise. 
Emphasize information that is not common knowledge or mainstream, as readers are looking for new ideas and solutions.  

Conclusion:
{conclusion}
"""
prompt = PromptTemplate(input_variables=["conclusion"], template=template)
summarizer_chain = LLMChain(llm=llm, prompt=prompt)

def summarize_conclusions(conclusions):
    """
    Summarize a list of PubMed conclusions.
    Returns a list of plain-English summaries focused on chronic health implications.
    """
    return [summarizer_chain.run(conclusion=c) for c in conclusions]
