"""Utils."""
from langchain_openai import ChatOpenAI

from config.config import MODEL


def get_llm_for_tweet_generation(max_tokens: int = 4096) -> ChatOpenAI:
    """Returns an OpenAI LLM."""
    return ChatOpenAI(temperature=0.5, model=MODEL, max_tokens=max_tokens)
