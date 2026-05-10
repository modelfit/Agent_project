from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import all_tools
from .prompt import SYSTEM_PROMPT
import os

root_agent = Agent(
    name="ساعد",
    model=LiteLlm(
        model="openrouter/openai/gpt-4.1-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
    ),
    description="مساعد مفيد",
    instruction=SYSTEM_PROMPT(),
    tools=all_tools,
)