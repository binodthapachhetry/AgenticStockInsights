from fastapi import FastAPI, Body
import requests
import os

app = FastAPI()

# You might store URLs or Pub/Sub topics for each agent as environment variables
DATA_INGESTOR_URL = os.environ.get("DATA_INGESTOR_URL", "http://data-ingestor-agent:8000")
SUMMARIZATION_URL = os.environ.get("SUMMARIZATION_URL", "http://summarization-agent:8000")
SENTIMENT_URL = os.environ.get("SENTIMENT_URL", "http://sentiment-agent:8000")
SEARCH_URL = os.environ.get("SEARCH_URL", "http://semantic-search-agent:8000")
QA_URL = os.environ.get("QA_URL", "http://qa-agent:8000")
ANALYTICS_URL = os.environ.get("ANALYTICS_URL", "http://analytics-agent:8000")

@app.get("/health")
def health():
    return {"status": "ok", "service": "orchestrator-agent"}

@app.post("/process_document")
def process_document(doc: dict = Body(...)):
    """
    Example flow:
    1. Forward raw doc to Summarization Agent
    2. Forward doc to Sentiment Agent
    3. Save doc to Semantic Search
    etc.
    """

    # 1. Summarize
    summary_resp = requests.post(f"{SUMMARIZATION_URL}/summarize", json={"text": doc["text"]})
    summary_data = summary_resp.json()

    # 2. Sentiment
    sentiment_resp = requests.post(f"{SENTIMENT_URL}/analyze", json={"text": doc["text"]})
    sentiment_data = sentiment_resp.json()

    # 3. Index in semantic search
    index_payload = {
        "text": doc["text"],
        "summary": summary_data["summary"],
        "sentiment": sentiment_data["sentiment_score"],
        "metadata": doc.get("metadata", {})
    }
    requests.post(f"{SEARCH_URL}/index", json=index_payload)

    return {
        "summary": summary_data["summary"],
        "sentiment_score": sentiment_data["sentiment_score"]
    }

@app.get("/ask")
def ask_question(q: str):
    """
    Orchestrates Q&A flow:
    1. Possibly forward user query to QA Agent
    2. QA Agent calls semantic search agent
    3. Return answer
    """
    resp = requests.get(f"{QA_URL}/ask", params={"q": q})
    return resp.json()