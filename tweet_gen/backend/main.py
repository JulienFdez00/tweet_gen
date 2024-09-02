"""Main backend file."""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.lib.chain import get_tweet_generation_chain
from config.config import (
    BACKEND_API_DESCRIPTION,
    BACKEND_API_HOST,
    BACKEND_API_PORT,
    BACKEND_API_TITLE,
    BACKEND_API_VERSION,
    LOGGER,
    LOGGER_LEVEL,
)


class Question(BaseModel):
    """Represents a question submitted to the API for processing.

    Attributes:
        tweet_request (str): tweet topic
        context_tweets (str): reference tweets
    """

    tweet_request: str
    context_tweets: str


app = FastAPI(
    title=BACKEND_API_TITLE,
    version=BACKEND_API_VERSION,
    description=BACKEND_API_DESCRIPTION,
)


@app.post("/tweet_generation")
async def rag_query(question_body: Question) -> dict:
    tweet_request = question_body.tweet_request
    context_tweets = question_body.context_tweets
    try:
        LOGGER.info(f"Received tweet request: {tweet_request}")

        response = get_tweet_generation_chain().invoke(
            {"tweet_request": tweet_request, "context_tweets": context_tweets}
        )

        LOGGER.info(f"answer: {response}")
        return {"answer": response}
    except Exception as e:
        LOGGER.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=BACKEND_API_HOST,
        port=BACKEND_API_PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level=LOGGER_LEVEL.lower(),
    )
