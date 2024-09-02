"""Utils."""
from langchain_openai import ChatOpenAI

from config.config import MODEL, TEMPERATURE


def get_llm_for_tweet_generation(max_tokens: int = 128) -> ChatOpenAI:
    """Returns an OpenAI LLM."""
    return ChatOpenAI(temperature=TEMPERATURE, model=MODEL, max_tokens=max_tokens)
