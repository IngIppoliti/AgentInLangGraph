from agents.base_agent import Agent
from tools.search_tool import create_search_tool
from langchain_openai import ChatOpenAI

def main():
    model = ChatOpenAI(model="gpt-4", temperature=0)
    tools = [create_search_tool()]
    agent = Agent(model=model, tools=tools, system="You are a helpful AI agent.")
    agent.run()

if __name__ == "__main__":
    main()
