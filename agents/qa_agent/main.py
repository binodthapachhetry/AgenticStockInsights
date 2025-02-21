from fastapi import FastAPI
from typing import Optional
import requests
import os

app = FastAPI()

SEMANTIC_SEARCH_URL = os.environ.get("SEMANTIC_SEARCH_URL", "http://semantic-search-agent:8000")

@app.get("/ask")
def ask(q: str):
    """
    Example retrieval-augmented Q&A:
    1. Fetch docs from semantic-search-agent
    2. Combine them
    3. Prompt an LLM (like GPT-4)
    """
    # 1. Retrieve relevant docs
    search_resp = requests.get(f"{SEMANTIC_SEARCH_URL}/search", params={"q": q})
    search_data = search_resp.json()  # you'd parse to get top documents

    # 2. Combine docs into a prompt
    context = f"Docs found: {search_data['result']}"
    prompt = f"""
    You are a financial AI. Based on the following context, answer: {q}
    Context: {context}
    """
    # 3. Call LLM (OpenAI, Vertex, or local)
    answer_text = "Mock Q&A response based on context."

    return {"answer": answer_text}