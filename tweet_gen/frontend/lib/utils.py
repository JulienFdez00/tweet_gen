"""Utils."""
import json
from typing import Generator

import requests
import streamlit as st
import streamlit.components.v1 as components
import tiktoken

from config.config import BACKEND_URL


def display_header(
    title: str = "Tweet Generator",
    sub_title: str = "Use your archive to generate new tweets",
    title_color: str = "#000000",
) -> None:  # noqa: E501
    st.divider()
    st.markdown(f"<h1 style='text-align: center; color: {title_color};'>{title}</h1>", unsafe_allow_html=True)
    st.write(f"<h3 style='text-align: center'>{sub_title}</h3>", unsafe_allow_html=True)
    st.divider()


def set_page_config() -> None:
    st.set_page_config(
        page_title="Tweet Generator",
    )


def copy_to_clipboard_button(content: str) -> None:
    # Unique identifier for each copy button
    unique_id = f"copyButton{hash(content)}"
    button_html = f"""
        <button id="{unique_id}" class="copy-button">Copy</button>
    """

    script_js = f"""
        <script>
        document.getElementById("{unique_id}").addEventListener("click", function() {{
            const tempInput = document.createElement('textarea');
            tempInput.value = `{content}`;
            document.body.appendChild(tempInput);
            tempInput.select()
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            this.textContent = 'Copied!'; // Optional: Change button text on copy
        }});
        </script>
    """
    components.html(button_html + script_js, height=30)


def generate_tweet(instructions: str, context_tweets: str) -> Generator:
    # Send the question to the backend RAG processing endpoint streaming
    data = {
        "tweet_request": instructions,
        "context_tweets": context_tweets,
    }
    answer = {"answer": ""}
    buffer = ""
    with requests.post(f"{BACKEND_URL}/tweet_generation", json=data, stream=True) as response:
        for chunk in response.iter_content(chunk_size=1024):
            buffer += chunk.decode("utf-8")
            try:
                formatted_buffer = "[" + buffer.replace("\n", "\\n").replace("}{", "},{") + "]"
                json_chunk = json.loads(formatted_buffer)
                buffer = ""  # Reset buffer after successful parsing
                for element in json_chunk:
                    for key, value in element.items():
                        if key == "answer":
                            yield value
                            answer[key] += value
            except json.JSONDecodeError:
                # Incomplete JSON, continue accumulating chunks
                continue

    st.session_state["generated_tweet"] = answer


def get_num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


def display_messages() -> None:
    for chat in st.session_state["chat_history"]:
        with st.container():
            with st.chat_message("user"):
                st.write(chat["user"])
            with st.chat_message("assistant"):
                st.write(chat["assistant"])
                copy_to_clipboard_button(chat["assistant"])


def add_tweet_to_chat_history(user_question: str) -> None:
    response_data = st.session_state["generated_tweet"]
    answer = response_data.get("answer", "No answer found.")
    st.session_state["chat_history"].append(
        {
            "user": user_question,
            "assistant": answer,
        }
    )
    st.session_state["generated_tweet"] = None
