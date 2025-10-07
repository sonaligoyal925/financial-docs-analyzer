# tools.py
import os
from dotenv import load_dotenv
load_dotenv()

import io
from typing import List

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

try:
    from crewai_tools.tools.serper_dev_tool import SerperDevTool
    search_tool = SerperDevTool()
except Exception:
    search_tool = None  

class FinancialDocumentTool:
    """
    Utility class providing safe helpers to load and sanitize text out of PDFs.
    Methods are synchronous to keep compatibility with frameworks that expect sync callables.
    """

    @staticmethod
    def read_pdf_text(path: str = "data/sample.pdf") -> str:
        """
        Read text from a PDF file and return a cleaned string.
        Falls back to returning a descriptive error string if reading fails.
        """
        if not os.path.exists(path):
            return f"[ERROR] File not found: {path}"

        if PyPDF2 is None:
            return "[ERROR] PyPDF2 is not installed. Install it (pip install PyPDF2) to enable PDF parsing."

        try:
            text_pages: List[str] = []
            with open(path, "rb") as fh:
                reader = PyPDF2.PdfReader(fh)
                for page in reader.pages:
                    content = page.extract_text() or ""

                    while "\n\n" in content:
                        content = content.replace("\n\n", "\n")
                    text_pages.append(content.strip())
            full_text = "\n\n".join(text_pages).strip()
            if not full_text:
                return "[WARN] PDF parsed but no textual content was extracted."
            return full_text
        except Exception as e:
            return f"[ERROR] Failed to read PDF: {str(e)}"

class InvestmentTool:
    """
    Simple, safe investment-observation tool. Produces non-actionable observations.
    """

    @staticmethod
    def summarize_financials(text: str) -> str:
        """
        Very small heuristic-based summarizer: looks for common financial statement words and reports presence.
        This is intentionally conservative: it returns observations and limitations, not buy/sell advice.
        """
        if not text or text.startswith("[ERROR]"):
            return f"[InvestmentTool] Cannot analyze: {text}"

        keywords = {
            "balance_sheet": ["balance sheet", "total assets", "total liabilities", "shareholders' equity", "equity"],
            "income_statement": ["income statement", "profit", "revenue", "net income", "earnings"],
            "cash_flow": ["cash flow", "operating activities", "investing activities", "financing activities"],
            "ratios": ["debt", "debt-to-equity", "current ratio", "gross margin", "operating margin", "ebitda"]
        }

        found = {}
        lowered = text.lower()
        for k, kwlist in keywords.items():
            found[k] = any(kw in lowered for kw in kwlist)

        observations = []
        observations.append("Summary of detected content:")
        for k, present in found.items():
            observations.append(f"- {k.replace('_',' ').title()}: {'Present' if present else 'Not detected'}")

        if found["balance_sheet"] and "total liabilities" in lowered and "total assets" in lowered:
            observations.append("- Heuristic: Balance sheet items detected. Consider checking asset/liability breakdowns for unusual lines.")
        if "auditor" in lowered or "audited" in lowered:
            observations.append("- Auditor language detected. Check for audit opinions or qualifications.")
        if "restatement" in lowered or "restate" in lowered:
            observations.append("- Restatement language detected — investigate accounting changes.")
        if not any(found.values()):
            observations.append("- No obvious financial statements detected in the text. The file may be a summary or a non-financial document.")

        observations.append("\nDisclaimer: These are high-level observations only. This tool does NOT provide personalized investment advice. Consult a licensed financial professional for decisions.")
        return "\n".join(observations)

class RiskTool:
    """
    Basic risk-flagging tool that highlights potential red flags in financial text.
    """

    @staticmethod
    def flag_risks(text: str) -> str:
        if not text or text.startswith("[ERROR]"):
            return f"[RiskTool] Cannot analyze: {text}"

        lowered = text.lower()
        flags = []

        if "going concern" in lowered:
            flags.append("Going concern language found — the company may have liquidity or solvency concerns.")
        if "significant uncertainty" in lowered or "material uncertainty" in lowered:
            flags.append("Material uncertainty language present — review management discussion carefully.")
        if "restated" in lowered or "restatement" in lowered:
            flags.append("Historical restatements detected — check prior period comparatives.")
        if "related party" in lowered:
            flags.append("Related party transactions mentioned — examine for potential conflicts of interest.")
        if "litigation" in lowered or "lawsuit" in lowered:
            flags.append("Litigation references found — assess potential contingent liabilities.")

        if not flags:
            flags.append("No high-confidence textual risk flags detected with simple heuristics. This does not imply no risk exists; use thorough quantitative analysis for risk assessment.")

        flags.append("\nDisclaimer: These are heuristic flags based on text presence only. They are not a substitute for a full forensic review.")
        return "\n".join(flags)
