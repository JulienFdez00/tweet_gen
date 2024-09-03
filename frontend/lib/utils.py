"""Utils."""
from typing import Optional

import requests
import streamlit as st
import tiktoken

from config.config import BACKEND_URL, LOGGER


def generate_tweet(instructions: str, context_tweets: str) -> Optional[str]:
    data = {
        "tweet_request": instructions,
        "context_tweets": context_tweets,
    }
    response = requests.post(f"{BACKEND_URL}/tweet_generation", json=data)
    if response.status_code == 200:
        answer = response.json().get("answer")
        st.session_state["generated_tweet"] = answer.get("response", "")
        LOGGER.info(f"Generated tweet: {answer.get('response', '')}")
        return answer.get("response", "")
    st.session_state["generated_tweet"] = ""
    response.raise_for_status()
    return None


def get_num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


def add_tweet_to_chat_history(user_question: str) -> None:
    response_data = st.session_state["generated_tweet"]
    answer = response_data
    st.session_state["chat_history"].append(
        {
            "user": user_question,
            "assistant": answer,
        }
    )
    st.session_state["generated_tweet"] = None
