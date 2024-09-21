from promptflow import tool
from promptflow.connections import CustomConnection
import cohere
from cohere.client import Client
import json

@tool
def cohere_rerank(docs:list, question:str , myconn: CustomConnection) -> str:
    client = Client(
        base_url=myconn.configs['api_base'],
        api_key=myconn.secrets['api_key']
    )


    response = client.rerank(
        model="rerank-english-v3.0",
        query=question,
        documents=docs,
        top_n=5,
        return_documents=True,
    )
    print(response)
    print(response.json())

    response = json.loads(response.json())
    
    documents = []
    for result in response["results"]:
        documents.append(result["document"])
    return documents

