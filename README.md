# Financial Document Analyzer 🏦📄

A **comprehensive financial document analysis system** that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

---

## Project Overview

This system allows users to:

- Upload financial documents in PDF format
- Get AI-powered financial analysis
- Receive investment recommendations
- Perform risk assessments
- Extract market insights

The project uses **CrewAI agents** and **OpenAI LLM** to process and analyze documents intelligently.

---

## Features

- **Upload financial PDFs** through API endpoint.
- **Investment analysis** based on financial metrics.
- **Risk assessment** for high/low-risk evaluation.
- **Document verification** for validating uploaded PDFs.
- **Async-safe file handling** with automatic cleanup.
- **Simple API interface** using FastAPI.

---

## Setup Instructions

1. **Clone the repository**:

```bash
git clone (https://github.com/sonaligoyal925/financial-docs-analyzer)
cd financial-document-analyzer
```


2. **Create a virtual environment (optional)**:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```


3. **Install dependencies**:

```bash
pip install -r requirement.txt
```

4. **Set up environment variables:**

Create a .env file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

5. **Add sample financial document:**

Download a PDF (e.g., Tesla Q2 2025 update) and place it in data/

```bash
data/sample.pdf
```

6. **Run the API**:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

# API Documentation

## Health Check

**GET /**

```bash
Response:
{
    "message": "Financial Document Analyzer API is running"
}
```

## Analyze Financial Document

**POST /analyze**

Parameters:

file (UploadFile) – PDF file to analyze

query (string, optional) – Custom query for analysis (default: "Analyze this financial document for investment insights")

Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Provide investment insights for this document"

```

Response:
```bash
{
  "status": "success",
  "query": "Provide investment insights for this document",
  "analysis": "Investment analysis text...",
  "file_processed": "sample.pdf"
}

```


# Code Overview

1. **agents.py**

- Defines all AI agents *(financial_analyst, verifier, investment_advisor, risk_assessor)*
- Correctly initializes LLM
- Assigns appropriate tools to each agent
- Handles agent roles, goals, and memory

2. **main.py**

- FastAPI server
- File upload and cleanup handling
- Calls *CrewAI* agents to analyze document
- Includes **/** health endpoint and **/** analyze endpoint

3. **task.py**

- Defines CrewAI tasks:
        *analyze_financial_document* → main task for analysis
- Corrects async issues and cleans up prompts
- Ensures task receives *file_path* and query

4. **tools.py**

Implements:
- *FinancialDocumentTool* → reads PDF files
- *InvestmentTool* → placeholder for investment analysis
- *RiskTool* → placeholder for risk assessment
- Fixed PDF loading using PyPDFLoader
- Cleaned up whitespace and string formatting

# Bugs Fixed & Changes


| File        | Issue                                                           | Fix                                                                                   |
| ----------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `agents.py` | Undefined `llm` and wrong `tool` argument                       | Initialized `llm` using OpenAI API key; corrected `tools=[...]`                       |
| `main.py`   | Function name conflict & missing `file_path` in Crew            | Renamed endpoint to `analyze_file`; passed `file_path` correctly                      |
| `task.py`   | Async and tool issues; chaotic task description                 | Simplified description; passed correct tools; task now deterministic                  |
| `tools.py`  | `Pdf` undefined; async not awaited; inefficient string cleaning | Replaced with `PyPDFLoader`; optimized whitespace cleanup; async static methods fixed |
| All         | Inefficient prompts and hallucination                           | Simplified prompts for deterministic and meaningful output                            |


# References

- CrewAI Documentation
- FastAPI Documentation
- OpenAI API
- PyPDFLoader from LangChain
