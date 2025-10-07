# task.py
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor
from tools import FinancialDocumentTool, InvestmentTool, RiskTool, search_tool

verify_document_task = Task(
    description=(
        "Verify whether the uploaded file appears to be a financial report. "
        "Return a short judgment (Yes/No) and the evidence (terms/sections) that support the judgment. "
        "If not a financial document, explain why."
    ),
    expected_output=(
        "A JSON-like or bullet summary: {'is_financial_document': bool, 'evidence': [...], 'notes': '...'}\n"
        "Keep it concise and factual."
    ),
    agent=verifier,
    tools=[],
    async_execution=False,
)

analyze_financial_document = Task(
    description=(
        "Read the financial document at the provided file path and produce a careful, high-level analysis. "
        "Include: (1) short executive summary, (2) detected statements (balance sheet/income/cash flow), "
        "(3) top 5 observations, (4) data quality issues or missing data, (5) recommended next steps (non-actionable). "
        "Do NOT give personalized buy/sell recommendations."
    ),
    expected_output=(
        "Structured analysis with clear sections, bullet points for observations, and explicit limitations/disclaimer."
    ),
    agent=financial_analyst,
    tools=[],  
    async_execution=False,
)

investment_education = Task(
    description=(
        "Based on the financial analysis, provide high-level educational context about metrics that matter (e.g., what a declining gross margin typically implies). "
        "This must be explicitly non-actionable and include a disclaimer."
    ),
    expected_output="Clear, plain-language explanations of financial metrics and what they generally imply.",
    agent=investment_advisor,
    tools=[],
    async_execution=False,
)
