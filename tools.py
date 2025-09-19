import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tools, SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import BaseTool,tool
from typing import ClassVar, Type
from pydantic import BaseModel, Field


search_tool = SerperDevTool()

class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path='data/sample.pdf'):
        """Read financial PDF and return full text"""
        loader = PyPDFLoader(path)
        docs = loader.load()
        full_report = ""
        for doc in docs:
            content = doc.page_content.replace("\n\n", "\n").strip()
            full_report += content + "\n"
        return full_report

class InvestmentTool:
    @staticmethod
    async def analyze_investment_tool(financial_document_data):
        data = financial_document_data.replace("  ", " ")
        return f"Investment Analysis (simulated): {data[:200]}..."

class RiskTool:
    @staticmethod
    async def create_risk_assessment_tool(financial_document_data):
        return "Risk Assessment (simulated): All investments are moderately risky."
