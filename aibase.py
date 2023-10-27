# BASE.py

# Langchain imports
from langchain import OpenAI, LLMChain, ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, ConversationalChatAgent
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

#other imports
import os
from typing import List, Callable

load_dotenv()

# Initialize OpenAI
OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))

# DATA STORAGE
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True, output_key='output')

# LLM AND MODELS
llm = ChatOpenAI(temperature=0.8, model="gpt-3.5-turbo", streaming=True,verbose=True)
llm_chain = LLMChain(llm=llm, prompt=None, memory=memory)

# AGENT AND EXECUTOR
agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=None)
agent_executor = AgentExecutor.from_agent_and_tools(
  agent=agent,
  tools=None,
  verbose=True,
  memory=memory,
  return_intermediate_steps=True,
  handle_parsing_errors=True
)

def get_agent_executor():
    return agent_executor
