import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Dict

# ==========================================================
# 🔐 Load API Key Securely from Environment
# ==========================================================
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment")

# ==========================================================
# 🌐 OpenRouter Configuration
# ==========================================================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"  # You can change this

# ==========================================================
# 🚀 Initialize FastAPI
# ==========================================================
app = FastAPI()

# ==========================================================
# 📦 Simple In-Memory Cache (Production → Use Redis)
# ==========================================================
response_cache: Dict[str, Dict] = {}

# ==========================================================
# 🧾 Request Schema
# ==========================================================
class PromptRequest(BaseModel):
    query: str

# ==========================================================
# 🧠 LLM Caller Function
# ==========================================================
def call_llm(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


# ==========================================================
# 🎯 Advanced Prompt Strategies
# ==========================================================

def zero_shot_prompt(query: str):
    """
    Purpose:
    Direct structured instruction without examples.
    Useful for clean task specification.
    """
    prompt = f"""
    You are a senior AI engineer.

    Task:
    {query}

    Provide:
    - Clear structured answer
    - Technical depth
    - Practical implementation details
    """
    return call_llm(prompt)


def few_shot_prompt(query: str):
    """
    Purpose:
    Provide examples before asking main question.
    Helps model understand format & style.
    """
    prompt = f"""
    Example 1:
    Question: Explain REST.
    Answer: REST is an architectural style...

    Example 2:
    Question: Explain JWT.
    Answer: JWT is a compact token format...

    Now answer:
    {query}
    """
    return call_llm(prompt)


def chain_of_thought_prompt(query: str):
    """
    Purpose:
    Encourage step-by-step reasoning.
    Improves logic quality.
    """
    prompt = f"""
    Solve the following step-by-step.
    Show reasoning clearly before final answer.

    Question:
    {query}
    """
    return call_llm(prompt)


def react_prompt(query: str):
    """
    Purpose:
    Reason + Act simulation.
    Useful in agent-based systems.
    """
    prompt = f"""
    Follow this structure:

    Thought:
    Action:
    Observation:
    Final Answer:

    Question:
    {query}
    """
    return call_llm(prompt)


def self_critique_prompt(query: str):
    """
    Purpose:
    Generate → Critique → Improve.
    Enterprise refinement pattern.
    """
    prompt = f"""
    Step 1: Provide answer to:
    {query}

    Step 2: Critique the answer for weaknesses.

    Step 3: Provide improved version.
    """
    return call_llm(prompt)


def multi_role_prompt(query: str):
    """
    Purpose:
    Multi-perspective expert evaluation.
    Used in system design reviews.
    """
    prompt = f"""
    Three experts will answer:

    1. Backend Engineer
    2. Security Engineer
    3. DevOps Engineer

    Each provides their perspective on:
    {query}
    """
    return call_llm(prompt)


def comparative_analysis(results: Dict[str, str]):
    """
    Purpose:
    Compare different prompting strategies.
    Ask model to rate them.
    """
    combined = "\n\n".join(
        [f"{k}:\n{v}" for k, v in results.items()]
    )

    prompt = f"""
    Analyze the following responses generated using different prompt strategies.

    Compare them based on:
    - Clarity
    - Technical depth
    - Logical structure
    - Practical usefulness

    Rate each out of 10.
    Provide comparative analysis.

    Responses:
    {combined}
    """

    return call_llm(prompt)


# ==========================================================
# 🧩 API Endpoint
# ==========================================================
@app.post("/run-prompts")
def run_prompts(request: PromptRequest):

    if request.query in response_cache:
        return response_cache[request.query]

    results = {
        "zero_shot": zero_shot_prompt(request.query),
        "few_shot": few_shot_prompt(request.query),
        "chain_of_thought": chain_of_thought_prompt(request.query),
        "react": react_prompt(request.query),
        "self_critique": self_critique_prompt(request.query),
        "multi_role": multi_role_prompt(request.query)
    }

    evaluation = comparative_analysis(results)

    final_response = {
        "results": results,
        "comparative_analysis": evaluation
    }

    response_cache[request.query] = final_response

    return final_response
