import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import search_tool, FinancialDocumentTool
from openai import OpenAI

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and provide investment insights based on the query: {query}",
    verbose=True,
    memory=True,
    backstory="You are an experienced financial analyst who provides accurate investment recommendations.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify uploaded document and ensure it is a financial report",
    verbose=True,
    memory=True,
    backstory="Check that the document is financial and provide confirmation",
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Recommend investments based on the financial document",
    verbose=True,
    backstory="Provide actionable investment advice with proper reasoning",
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Provide risk analysis for investments mentioned in the document",
    verbose=True,
    backstory="Assess potential risks and volatility in investments",
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
