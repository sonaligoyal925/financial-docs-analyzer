# agents.py
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
import openai

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = os.environ.get("OPENROUTER_API_BASE", "https://api.openrouter.ai/v1")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY environment variable. Set it and restart.")

openai.api_key = OPENROUTER_API_KEY
openai.api_base = OPENROUTER_API_BASE  

class SimpleLLM:
    def __init__(self, model="gpt-4o-mini", temperature=0.2, max_tokens=800):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Synchronous wrapper for chat completion. Returns assistant text.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in financial document analysis. Be cautious, cite uncertainty, and do NOT provide personalized investment advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens)
            )
            text = response.choices[0].message.content.strip()
            return text
        except Exception as e:
            return f"[LLM-ERROR] Failed to generate text: {str(e)}"

llm = SimpleLLM()

financial_analyst = Agent(
    role="Financial Document Analyst",
    goal="Read the supplied financial document carefully, summarize the key financial statements and metrics, highlight potential data issues or anomalies, and provide high-level observations. Do NOT provide personalized investment or legal advice. Recommend consulting a licensed professional for actionable decisions.",
    verbose=True,
    memory=False,
    backstory=(
        "You're a cautious and competent financial analyst. Your aim is to produce clear summaries, flag questionable items, "
        "note assumptions, and explain uncertainty. Do not invent facts. If the document lacks information, state that explicitly."
    ),
    tool=[],  
    llm=llm,
    max_iter=3,
    max_rpm=60,
    allow_delegation=False
)

verifier = Agent(
    role="Document Verifier",
    goal="Determine whether the uploaded file is a financial document and summarize the evidence for that decision (e.g., presence of balance sheet, income statement, cash flow, line items, accounting dates). If not a financial doc, explain why. Do not blindly approve documents.",
    verbose=True,
    memory=False,
    backstory=(
        "You are trained to verify document types by looking for structural clues and common financial terms. When uncertain, ask for clarification or report missing evidence."
    ),
    tool=[],
    llm=llm,
    max_iter=2,
    max_rpm=60,
    allow_delegation=False
)

investment_advisor = Agent(
    role="High-level Investment Educator (non-actionable)",
    goal="Provide general, educational information about investment concepts relevant to the document (e.g., what a high debt-to-equity ratio means generally). Include an explicit disclaimer that this is educational only and not financial advice.",
    verbose=True,
    memory=False,
    backstory=(
        "You explain investment concepts in plain English and avoid making specific buy/sell calls."
    ),
    tool=[],
    llm=llm,
    max_iter=2,
    max_rpm=60,
    allow_delegation=False
)
