from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_financial_document_task

app = FastAPI(title="Financial Document Analyzer")

async def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    if asyncio.iscoroutine(result):
        result = await result
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if query == "" or query is None:
            query = "Analyze this financial document for investment insights"
            
        response = await run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
