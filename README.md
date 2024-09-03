# Tweet Generator

Use your tweet archive to generate new, original tweets.

## Quickstart

### Step 0

Download an archive of your tweets. You will use the "tweets.js" file located in the "data" folder of your archive.

### Step 1

Create a virtual environment with Python 3.10 and install the required libraries by running

 ```bash
    pip install -r requirements.txt
 ```

### Step 2

Create an .env file and add your OpenAI API key (OPENAI_API_KEY="sk-xxx"). You can also do so by running the following command in your terminal:

 ```bash
    export OPENAI_API_KEY="sk-xxx"
 ```

### Step 3

To start the backend server locally:

```bash
   make run_backend
```

### Step 4

Run the app locally:

```bash
   make run_frontend
```

## User Guidelines

Be detailed in your tweet requests, generated tweets can be somewhat formulaic if you don't give the model clear guidelines. Ex: "Generate a humorous and laconic tweet about bad hair days" is better than "bad hair days".

## Necessary Improvements

Impersonation still isn't perfect, the model is very sensitive to the prompt so feel free to play around with it. 

## Notes

I feel like giving permissive content sensitivity guidelines makes tweets in general less formulaic, even ones that aren't particularly vulgar or offensive. Obviously please refrain from posting insensitive or vulgar stuff online yadda yadda yadda.
