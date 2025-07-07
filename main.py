from agents.base_agent import Agent
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
    

if __name__ == "__main__":
    main()
