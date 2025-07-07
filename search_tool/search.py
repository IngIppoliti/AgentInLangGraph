#Tavily Search API is a specialized search engine designed for Large Language Models (LLMs) and AI agents. It provides real-time, accurate, and unbiased information from the web.
#the advantage is that it acts as a search engine accessing web updated information but return answer that are structured to be consumed bu agents (JSON format)

from langchain_community.tools.tavily_search import TavilySearchResults

def create_search_tool(max_results=4):
    return TavilySearchResults(max_results=max_results)
