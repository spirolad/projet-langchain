# Pour permettre à l'agent de répondre à des questions ouvertes : actualités financières, informations sur une entreprise, cours récents non couverts par les autres outils.

from tavily import TavilyClient
import os

def answer_open_question(input: str):
    client = TavilyClient(os.getenv('TAVILY_API_KEY'))
    response = client.search(
        query=input,
        search_depth="advanced"
    )
    return response