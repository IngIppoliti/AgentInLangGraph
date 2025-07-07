from langchain_community.tools.tavily_search import TavilySearchResults

def create_search_tool(max_results=4):
    return TavilySearchResults(max_results=max_results)
