# # import os  # read env variables, like API Keys
# # from dotenv import load_dotenv  # open API keys
# # from langchain_openai import ChatOpenAI  # modern wrapper
# # from langchain.prompts import PromptTemplate
# # from langchain.chains import LLMChain


# # load_dotenv() #load my env

# # llm = ChatOpenAI(model="gpt-3.5-turbo")

# # #the {abstract is a placeholder} to be filled in 
# # template = """
# # You are a medical research explainer. 
# # Summarize the following PubMed abstract in plain English.
# # Highlight any implications for chronic health.

# # Abstract:
# # {abstract}
# # """

# # prompt = PromptTemplate(input_variables=["abstract"], template=template)
# # # tells LangChain what placeholders exist; full prompt created

# # summarizer_chain = LLMChain(llm=llm, prompt=prompt) #sends it out; glues model and template together
# # # data (abstract)-->insert into prompt-->send to model --> return output

# # def summarize(abstracts):
# #     """
# #     Summarize a list of abstracts.
# #     """
# #     return [summarizer_chain.run(abstract=ab) for ab in abstracts]

# # import os
# # from dotenv import load_dotenv
# # from langchain_openai import ChatOpenAI
# # from langchain.prompts import PromptTemplate
# # from langchain.chains import LLMChain

# # load_dotenv()

# # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# # template = """
# # You are a medical research explainer. 
# # Summarize the following PubMed study conclusion in easy to understand English.
# # Include implications for health & actionable solutions. 
# # Be sure to include the primary author and year of the study.
# # It is integral you mention how it is relevant to what the query term was. 

# # Title: {title}
# # Authors: {authors}
# # Year: {year}
# # Conclusion: {abstract}
# # """
# # prompt = PromptTemplate(input_variables=["title","authors","year","abstract"], template=template)
# # summarizer_chain = LLMChain(llm=llm, prompt=prompt)

# # def summarize_conclusions(studies):
# #     """
# #     Summarize a list of study dictionaries.
# #     Each study dict has 'title','authors','year','abstract'
# #     """
# #     return [summarizer_chain.run(
# #         title=st["title"],
# #         authors=st["authors"],
# #         year=st["year"],
# #         abstract=st["abstract"]
# #     ) for st in studies]

# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
# from langchain.chains import LLMChain

# load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# template = """
# You are a medical research explainer. 
# Summarize the following PubMed study conclusion in easy to understand English.
# Include implications for health & actionable solutions. 
# Be sure to include the primary author and year of the study.
# It is integral you mention how it is relevant to what the query term was. 

# Title: {title}
# Authors: {authors}
# Year: {year}
# Conclusion: {abstract}
# """
# prompt = PromptTemplate(
#     input_variables=["title","authors","year","abstract"],
#     template=template
# )
# summarizer_chain = LLMChain(llm=llm, prompt=prompt)

# def summarize_conclusions(studies):
#     """
#     Summarize a list of study dictionaries.
#     Each study dict must have 'title','authors','year','abstract','pmid'.
#     """
#     summaries = []
#     for st in studies:
#         summary = summarizer_chain.run(
#             title=st["title"],
#             authors=st["authors"],
#             year=st["year"],
#             abstract=st["abstract"]
#         )
        
#         # 🔗 Add PubMed link
#         pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{st['pmid']}/"
#         linked_header = f"[**{st['title']}** ({st['authors']}, {st['year']})]({pubmed_url})"
        
#         # Combine header + summary
#         summaries.append(f"{linked_header}\n\n{summary}")
    
#     return summaries

# summarization_pipeline.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment")

# LangChain imports
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.chains import LLMChain
from langchain_openai import ChatOpenAI

# Your own modules
# from pubmed_search import search_pubmed
# from summarizer import summarize_conclusions

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# Prompt template for summarization
summarization_prompt = PromptTemplate(
    input_variables=["text"],
    template="Please summarize the following text clearly and concisely:\n\n{text}"
)

# Create LLMChain for summarization
summarization_chain = LLMChain(
    llm=llm,
    prompt=summarization_prompt
)

# Example function to summarize PubMed articles
def summarize_pubmed_articles(query, max_articles=5):
    """
    Fetches PubMed articles for a query and summarizes conclusions.
    """
    # articles = search_pubmed(query, max_results=max_articles)  # Your own function
    articles = [
        {"title": "Example Article 1", "abstract": "This is the first article abstract."},
        {"title": "Example Article 2", "abstract": "Second article abstract goes here."}
    ]  # Placeholder for testing
    
    summaries = []
    for article in articles:
        text_to_summarize = article.get("abstract", "")
        # Use LLM chain to summarize
        summary = summarization_chain.run({"text": text_to_summarize})
        summaries.append({
            "title": article["title"],
            "summary": summary
        })
    
    return summaries

# Test run
if __name__ == "__main__":
    results = summarize_pubmed_articles("elephant conservation")
    for r in results:
        print(f"Title: {r['title']}\nSummary: {r['summary']}\n")
