from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI  # or your LLM of choice
# import other needed LangChain modules

# Example initialization - customize with your setup
llm = OpenAI(temperature=0)
tools = []  # your tools here if any

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def run_langchain_agent(prompt: str) -> str:
    result = agent.run(prompt)
    return result
