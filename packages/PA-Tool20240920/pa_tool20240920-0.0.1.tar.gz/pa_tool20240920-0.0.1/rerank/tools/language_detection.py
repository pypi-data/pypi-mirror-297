from promptflow import tool
from langdetect import detect

@tool
def my_python_tool(question: str) -> str:
    return detect(question)

