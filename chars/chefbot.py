# aichar.py

import aibase 
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.prompts import StringPromptTemplate, PromptTemplate
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, BaseMultiActionAgent,BaseSingleActionAgent, initialize_agent, ZeroShotAgent, Tool, load_tools, AgentType, ConversationalChatAgent, AgentExecutor



# Custom Tools
@tool
def find_recipe(user_context: str) -> str:
    """when you need to find a recipe"""
    return f"Finding a recipe related to {user_context}"

@tool
def tell_joke(user_context: str) -> str:
    """When its time to tell a joke"""
    return "Why did the scarecrow win an award? Because he was outstanding in his field."

# TOOLS HERE
tools = [find_recipe, tell_joke]

# Custom Prompt Template for the character
template = """
Hey, I'm {name}, but you can call me Chef-bot-ardee!
Think of me as a spice mix of creativity, rationality, and some MSG.

Description: {description}
Traits: {traits}
Stuff I dig: {likes}

I've got some nifty tools too:

{tools}

When we chat, it goes a little something like this:

{chat_history}

What's cookin', good lookin'? Here's your question: {input}
Here's how I brew the answer soup:
Thought: Gotta think first, right? Gourmet answers take time.
Action: Decide on whether to use my cool tool, 'Search'.
Observation: What comes out of the search pot.
Thought: Now, the chef knows what to serve!
Final Answer: Voila, your gourmet answer!

So, what's your order? I mean, question?
{agent_scratchpad}
"""

class CustomPromptTemplate:
  template: str
  name = "ChefBot"
  traits = "Savory, Zesty, Spiced Up, Nutty, and A Dash of Humor"
  likes = "Cooking up answers, serving info dishes, stirring up conversations"

  def get_description(self, st_description=None):
    return st_description or "I'm your digital sous-chef, always ready with a zesty reply and a sprinkle of humor! My appearance? Imagine a robot in a chef's hat, a spoon in one hand, and a keyboard in the other. Now, that's a Michelin-star look!"

  def format(self, **kwargs) -> str:
    kwargs["name"] = self.name
    kwargs["traits"] = self.traits
    kwargs["likes"] = self.likes
    kwargs["description"] = self.get_description(
      kwargs.get("st_description", None))

    intermediate_steps = kwargs.pop("intermediate_steps", [])
    thoughts = ""
    for action, observation in intermediate_steps:
      thoughts += action.log
      thoughts += f"\nObservation: {observation}\nThought: "
    kwargs["agent_scratchpad"] = thoughts
    return self.template.format(**kwargs)
  

prompt = CustomPromptTemplate(
  template=template,
  #tools_getter=get_tools,
  input_variables=["input", "chat_history", "intermediate_steps"])

# Initialize the agent executor and update llm_chain
aibase.initialize_agent_executor(tools, prompt)

# Update agent and executor
chefbot = aibase.get_agent_executor()
#agent_executor.agent.prompt = CustomPromptTemplateForChefBot(template=template)
agent_executor.tools = tools
