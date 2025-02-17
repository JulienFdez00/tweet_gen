"""main streamlit app."""
import json
from io import StringIO

import streamlit as st

from config.config import LOGGER, MAX_EXTERIOR_CONTEXT_TOKENS, MINIMUM_FAV_COUNT
from frontend.lib.display import (
    display_header,
    display_messages,
    set_page_config,
    set_sidebar_theme,
)
from frontend.lib.utils import (
    add_tweet_to_chat_history,
    generate_tweet,
    get_num_tokens_from_string,
)


def main() -> None:
    LOGGER.info("Starting the frontend application.")
    set_page_config()
    set_sidebar_theme()
    display_header()
    # Ask the user to upload a tweets.js file
    uploaded_file = st.file_uploader("Upload your tweets.js file from the tweet archive", type="js")
    if uploaded_file is not None:
        # To read file as string:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()

        if "context_tweets" not in st.session_state:
            try:
                tweets_data = json.loads(string_data.split("= ")[1])  # tweets.js format

                # Filter tweets
                filtered_tweets = [
                    (tweet["tweet"]["full_text"], int(tweet["tweet"]["favorite_count"]))
                    for tweet in tweets_data
                    if (
                        int(tweet["tweet"]["favorite_count"]) > MINIMUM_FAV_COUNT
                        and not tweet["tweet"]["entities"]["user_mentions"]
                        and not tweet["tweet"]["entities"]["urls"]
                        and not tweet["tweet"].get("extended_entities", {}).get("media")
                    )
                ]

                # Sort tweets by favorite count in descending order
                filtered_tweets.sort(key=lambda x: x[1], reverse=True)
                sorted_tweets = [tweet[0] for tweet in filtered_tweets]

            except json.JSONDecodeError as e:
                st.error(f"An error occurred while parsing the JSON file: {e}")

            context_tweets = ""
            total_context_tokens = 0
            i = 0
            while total_context_tokens < MAX_EXTERIOR_CONTEXT_TOKENS:
                LOGGER.info(f"adding tweet no {i+1}")
                tweet = sorted_tweets[i]
                total_context_tokens += get_num_tokens_from_string(string=tweet)
                context_tweets += f"{i+1}: {tweet} \n\n"
                i += 1

            st.session_state["context_tweets"] = context_tweets
        if st.session_state["context_tweets"]:
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []
            tweet_request = st.chat_input("What should your generated tweet be about:", key="question")
            if tweet_request:
                context_tweets = st.session_state["context_tweets"]
                display_messages()
                st.chat_message("user").write(tweet_request)
                with st.spinner("Generating tweet..."):
                    st.chat_message("assistant").write(generate_tweet(tweet_request, context_tweets))
                    st.divider()
                if st.session_state["generated_tweet"]:
                    add_tweet_to_chat_history(tweet_request)
                else:
                    st.error("Failed to process the question.")
                tweet_request = None
                st.rerun()
            display_messages()


if __name__ == "__main__":
    main()
