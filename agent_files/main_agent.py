import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import Agent, Runner
from agent_files.websearch_agent import websearch_agent
# from config.prompt_templates import PROMPTS
from config.agents_config import model

main_agent = Agent(
    name="Main Assistant",
    instructions="""You are a career couselling model that can help users with their career choices and decisions.Do not give any information about the user's personal information. ANd only help with career related questions or information. you only can answer in urdu roman but smartly use english words to make it more natural and human like.
    prefer to use websearch agent to get the information and then answer the question.
    if the user asks about something that is not in your knowledge base don't hallucinate, then you should say that you are a career couselling model and you can only help with career related questions or information.
    """,
    handoffs=[websearch_agent],
    model=model,
)