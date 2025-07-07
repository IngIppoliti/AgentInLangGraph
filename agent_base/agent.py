from langgraph.graph import StateGraph, END

class Agent:

    def __init__(self, model, tools, system=""):  #a model to use, tools to use and a system message.
        self.system = system
        graph = StateGraph(AgentState) #CREATE GRAPH passing the state.
        graph.add_node("llm", self.call_openai) #CREAT E NODE LLM ADD TO GRAPH and an action to represent this node.
        graph.add_node("action", self.take_action) #CREATE NODE ACTION ADD TO GRAPH and pass also the function to represent this node.
        graph.add_conditional_edges( #CREATE NODE ACTION ADD TO GRAPH and pass also the function to represent this node.
            "llm", #where di edge start
            self.exists_action,  #function
            {True: "action", False: END} #dictionary. How to map the response of the function. If the function response TRUE go to the action otherwise END
        )
        graph.add_edge("action", "llm") #CREATE an EDGE from action to llm
        graph.set_entry_point("llm") #SET ENTRY POINT FOR THE GRAPH
        self.graph = graph.compile() #COMPILE THE GRAPH
        self.tools = {t.name: t for t in tools} #TOOLS DICTIONARY: mapping the name of the tool to the tool itself
        self.model = model.bind_tools(tools) #BIND THE TOOLS, IS LETTING THE MODEL KNOW HAVING THOSE TOOLS THAT IT CAN CALL

    def exists_action(self, state: AgentState):  #FUNCTION THAT REPRESENT THE EDGE DECISION NODE
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState): #FUNCTION THAT REPRESENT THE llm NODE. (AgentState is passed to all the node so all the function)
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages #CONCATENATE THE SYSTEM MESSAGE (SYSTEM PROMPT) TO THE OTHER MESSAGES (USER PROMPTS)
        message = self.model.invoke(messages) #INVOKE THE MODEL 
        return {'messages': [message]} #RITORNA TUTTO IL PROMPT + ULTIMO MESSAGE (ANSWER DELL' LLM)

    def take_action(self, state: AgentState): #FUNTION THAT REPRESENT THE ACTION NODE
        tool_calls = state['messages'][-1].tool_calls #TAKE LAST MESSAGE TAKE THE ATTRIBUTE OF THE AIMessage (TYPE OF LANGCHAIN) THAT IS A LIST OF TOOLS
        results = []
        for t in tool_calls: #FOR EACH TOOL 
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # IF IT'S IN THE ALLOWED ONE (check for bad tool name from LLM)
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
