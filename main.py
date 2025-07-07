from agents.base_agent import Agent
from agents.
from tools.search_tool import create_search_tool
from langchain_openai import ChatOpenAI

def main():
    model = ChatOpenAI(model="gpt-4", temperature=0)
    prompt=                "You are a smart research assistant. Use the search engine to look up information. \
                            You are allowed to make multiple calls (either together or in sequence). \
                            Only look up information when you are sure of what you want. \
                            If you need to look up some information before asking a follow up question, you are allowed to do that!"
                        
    tools = [create_search_tool()]
    agent = Agent(model=model, tools=tools, system=prompt)

    #FIRST EXAMPLE
    messages = [HumanMessage(content="What is the weather in sf?")]
    result = abot.graph.invoke({"messages": messages})
    
    #LOG OF THE PREVIOUS GRAPH INVOCATION
    #Calling: {'name': 'tavily_search_results_json', 'args': {'query': 'weather in San Francisco'}, 'id': 'call_PvPN1v7bHUxOdyn4J2xJhYOX'}
    #Back to the model!

    #SECOND EXAMPLE
    #messages = [HumanMessage(content="What is the weather in sf and la?")]
    #result = abot.graph.invoke({"messages": messages})

    #LOG OF THE PREVIOUS GRAPH INVOCATION
    #Calling: {'name': 'tavily_search_results_json', 'args': {'query': 'weather in San Francisco'}, 'id': 'call_1SqGYuEtOOFN1yiIHSQTPnvE'}
    #Calling: {'name': 'tavily_search_results_json', 'args': {'query': 'weather in Los Angeles'}, 'id': 'call_8RiM72Y7G8V7c3HEEAML1SKP'}
    #Back to the model!
    #AS you can see here before to go back to the model it performs 2 actions in the same transaction before to go to the model

if __name__ == "__main__":
    main()
