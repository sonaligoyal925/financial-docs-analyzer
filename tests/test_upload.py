import requests

file_path = "sample.pdf"  
url = "http://127.0.0.1:8000/analyze"
query = "Summarize this financial document"

with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"query": query}
    response = requests.post(url, files=files, data=data)

print(response.json())
