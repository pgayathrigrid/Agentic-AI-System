import os
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
from google import genai
import requests
from bs4 import BeautifulSoup

# -----------------------------
# Setup
# -----------------------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# Load RAG data
# -----------------------------
with open("data/processed/chunks.json") as f:
    chunks = json.load(f)

index = faiss.read_index("vectorstores/faiss_index.index")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# TOOL 1: RAG
# -----------------------------
def rag_tool(query):
    q_emb = np.array(embed_model.encode([query]), dtype="float32")
    distances, indices = index.search(q_emb, 5)

    context = ""
    for i in indices[0]:
        context += chunks[i]["text"] + "\n"

    return context

# -----------------------------
# TOOL 2: Web Search (Google News)
# -----------------------------
def web_tool(query):
    import xml.etree.ElementTree as ET

    try:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '%20')}"
        response = requests.get(url, timeout=5)

        root = ET.fromstring(response.content)

        results = []
        for item in root.findall(".//item")[:5]:
            title = item.find("title").text
            link = item.find("link").text

            results.append(f"{title}\nSource: {link}")

        if not results:
            return "No news found."

        return "\n\n".join(results)

    except Exception as e:
        return f"News fetch failed: {str(e)}"

# -----------------------------
# TOOL 3: Financial (Stable API)
# -----------------------------
def financial_tool(query):
    import yfinance as yf

    try:
        tickers = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]

        results = []
        for t in tickers:
            stock = yf.Ticker(t)
            price = stock.info.get("currentPrice", "N/A")
            results.append(f"{t} - {price}")

        return "Top Stocks:\n" + "\n".join(results)

    except Exception as e:
        return f"Financial data fetch failed: {str(e)}"

# -----------------------------
# TOOL 4: News Agent (A2A)
# -----------------------------
def news_agent_tool(query):
    try:
        response = requests.get(
            "http://127.0.0.1:5001/news",
            params={"q": query},
            timeout=5
        )
        data = response.json()
        return "\n\n".join(data["news"])

    except Exception as e:
        return f"News agent failed: {str(e)}"

# -----------------------------
# TOOL 5: Canvas (Report Generator)
# -----------------------------
def canvas_tool(query, context):
    prompt = f"""
    You are a report generator.

    Create a well-structured report using the information below.

    Include:
    - Title
    - Key Points
    - Detailed Explanation
    - Conclusion

    Question:
    {query}

    Context:
    {context}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# -----------------------------
# PLANNER
# -----------------------------
def plan(query):
    q = query.lower()

    # Financial (ONLY for live data)
    if any(word in q for word in ["stock", "crypto", "currency"]):
        if any(word in q for word in ["today", "price", "latest", "live", "top"]):
            return "financial"

    # News
    if any(word in q for word in ["news", "latest updates", "recent"]):
        return "web"

    # Default
    return "rag"

# -----------------------------
# EXECUTION
# -----------------------------
def execute(query, tool):
    if tool == "rag":
        return rag_tool(query)

    elif tool == "web":
        return web_tool(query)

    elif tool == "news_agent":
        return news_agent_tool(query)

    elif tool == "financial":
        return financial_tool(query)

    elif tool == "canvas":
        base_context = rag_tool(query)
        return canvas_tool(query, base_context)
    

# -----------------------------
# SYNTHESIZER
# -----------------------------
def synthesize(query, context):
    prompt = f"""
    You are a helpful AI assistant.

    Give a clear, concise answer.

    Rules:
    - Keep the answer short (5–8 lines max)
    - Use simple language
    - No unnecessary details
    - No "direct" or "indirect" sections
    - Only give bullet points if really needed
    - Answer like a normal chatbot, not a report

    Question:
    {query}

    Context:
    {context}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -----------------------------
# CRITIQUE LOOP
# -----------------------------
def critique(answer, query):
    prompt = f"""
    You are a strict reviewer.

    Question: {query}

    Answer:
    {answer}

    ONLY do the following:

    - If the answer is clearly wrong or empty → suggest a better follow-up question.
    - Otherwise → respond ONLY with: GOOD
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()

# -----------------------------
# MAIN AGENT
# -----------------------------
def agent(query, max_iter=2):
    current_query = query

    for _ in range(max_iter):
        tool = plan(current_query)
        context = execute(current_query, tool)

        # Special case: financial
        if tool == "financial":
            return context

        answer = synthesize(current_query, context)

        feedback = critique(answer, current_query)

        if feedback.upper() == "GOOD":
            return answer

        current_query = feedback

    return answer

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    q = input("Ask: ")
    print("\nAnswer:\n")
    print(agent(q))