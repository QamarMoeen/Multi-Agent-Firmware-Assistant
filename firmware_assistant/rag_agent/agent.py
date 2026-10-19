
from google.adk.agents import Agent

from ..prompts.rag_prompt import RAG_PROMPT
from ..rag.retriever import search_documents


rag_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="rag_agent",
    description=(
        "Searches project documents and answers questions "
        "using retrieved technical information."
    ),
    instruction=RAG_PROMPT,
    tools=[search_documents],
)