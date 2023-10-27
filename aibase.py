# BASE.py

# Langchain imports
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_retriever_tool, create_conversational_retrieval_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts.prompt import PromptTemplate
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema import ChatMessage

#stream
from langchain.callbacks.streamlit.streamlit_callback_handler import LLMThought
from streamlit.delta_generator import DeltaGenerator
from langchain.callbacks import StreamlitCallbackHandler

#toolkit
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import StructuredTool
from dataclasses import dataclass, field

#File imports


#agent
from langchain.agents.types import AgentType
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, BaseMultiActionAgent,BaseSingleActionAgent, initialize_agent, ZeroShotAgent, Tool, load_tools, AgentType, ConversationalChatAgent, AgentExecutor
from langchain.tools.base import BaseTool
from langchain.chains import LLMChain
from langchain.schema import Document, AgentAction, AgentFinish
from langchain.tools import tool
from dotenv import load_dotenv

#other imports
import os
from typing import List, Callable

load_dotenv()

# Initialize OpenAI

# DATA STORAGE
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True, output_key='output')

# LLM AND MODELS
llm = ChatOpenAI(temperature=0.8, model="gpt-3.5-turbo", streaming=True,verbose=True)
llm_chain = None  # Initialize as None, and update it later

def initialize_agent_executor(tools, prompt_template):
    global llm_chain  # Use the global llm_chain variable
    llm_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)

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
