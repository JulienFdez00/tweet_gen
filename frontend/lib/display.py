"""Frontend display."""

import streamlit as st
import streamlit.components.v1 as components

from config.config import PATH_LOGO


def display_header(
    title: str = "Tweet Generator",
    sub_title: str = "Use your archive to generate new tweets",
    title_color: str = " #47474a",
) -> None:  # noqa: E501
    st.divider()
    st.markdown(f"<h1 style='text-align: center; color: {title_color};'>{title}</h1>", unsafe_allow_html=True)
    st.write(f"<h3 style='text-align: center; color: {title_color};'>{sub_title}</h3>", unsafe_allow_html=True)
    st.divider()


def set_page_config() -> None:
    st.set_page_config(
        page_title="Tweet Generator",
    )

def set_sidebar_theme() -> None:
    st.html(
        """
    <style>
    [data-testid="stSidebarContent"] {
        color: #f5f5f5;
        background-color: #47474a;
    }
    </style>
    """
    )
    st.sidebar.image(PATH_LOGO, use_column_width=True)
    st.sidebar.markdown("By JulienFdez00")


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

def display_messages() -> None:
    for chat in st.session_state["chat_history"]:
        with st.container():
            with st.chat_message("user"):
                st.write(chat["user"])
            with st.chat_message("assistant"):
                st.write(chat["assistant"])
                copy_to_clipboard_button(chat["assistant"])
