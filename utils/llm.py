"""
LLM Configuration
------------------
Central place where we create the LLM client used by every agent.
Keeping this in one file means if you ever want to switch providers
(e.g. OpenAI -> Anthropic Claude), you only change it here.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load variables from the local .env file into the environment
load_dotenv()


def get_llm(temperature: float = 0.2):
    """
    Returns a configured chat LLM.

    temperature=0.2 is intentionally LOW for a support system:
    - Low temperature = more deterministic, focused, less "creative" output.
    - We want consistent, predictable troubleshooting answers, not
      imaginative or varied ones, since incorrect creativity here
      could mean wrong IT instructions.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Copy .env.example to .env and add your key."
        )
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature,
        api_key=api_key,
    )
