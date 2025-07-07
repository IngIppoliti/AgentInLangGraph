from agent_base import Agent
from agent_with_memory import AgentMemory
from search_tool.search import create_search_tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver  #for persistency


def call_example_with_human_in_the_loop_and_streaming(agent):
        messages = [HumanMessage(content="Whats the weather in SF?")]
        thread = {"configurable": {"thread_id": "1"}}
        for event in abot_memory.graph.stream({"messages": messages}, thread):
            for v in event.values():
                print(v)
        
        abot_memory.graph.get_state(thread) #return current thread state (in this case you would see that is blocked just before the call of the action
        abot_memory.graph.get_state(thread).next #restituisce the next status (in this case will return action as next state)
        for event in abot_memory.graph.stream(None, thread):  #if you invoke again the agent in a stream way
            for v in event.values():
                print(v)

def main():
    model = ChatOpenAI(model="gpt-4", temperature=0)
    prompt=                """You are a smart research assistant. Use the search engine to look up information. \
                            You are allowed to make multiple calls (either together or in sequence). \
                            Only look up information when you are sure of what you want. \
                            If you need to look up some information before asking a follow up question, you are allowed to do that!"""
                        
    tools = [create_search_tool()]

    #------------------------------------- AGENT TYPE-------------------------
    
    #NO MEMORY
    abot = Agent(model=model, tools=tools, system=prompt)

    #WITH MEMORY AND HUMAN IN THE LOOP (Look in the code of AgentMemory)
    #memory = SqliteSaver.from_conn_string(":memory:")
    #abot_memory = AgentMemory (model=model, tools=tools, system=prompt, checkpointer=memory)

    
    #--------------------------------------- SAMPLES ----------------------------
    
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


    #THIRD EXAMPLE (STREAMING AND HUMAN IN THE LOOP)
    #    call_example_with_human_in_the_loop_and_streaming(agent=abot_memory )



if __name__ == "__main__":
    main()
