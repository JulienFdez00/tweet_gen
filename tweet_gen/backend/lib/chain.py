# ruff: noqa: E501
"""Tweet generation Chain."""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from backend.lib.prompts import TWEET_PROMPT_TEMPLATE
from backend.lib.utils import get_llm_for_tweet_generation


def get_tweet_generation_chain(prompt: ChatPromptTemplate = TWEET_PROMPT_TEMPLATE) -> Runnable:
    """Returns the RFP summerization chain."""
    llm = get_llm_for_tweet_generation()
    return prompt | llm | {"response": StrOutputParser()}
