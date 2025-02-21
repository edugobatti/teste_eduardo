import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from src.agents.agent import OpenAIAgent
import subprocess
import threading

agent = OpenAIAgent()

app = FastAPI()


@app.get("/sales-insights")
def get_sales_insights(question: Optional[str] = Query(None, description="Pergunta sobre insights de vendas")):
    """
    Retorna insights baseados na pergunta fornecida.
    """
    if not question:
        raise HTTPException(status_code=400, detail="Por favor, forneça uma pergunta válida.")
    else:
       response = agent.execute(question)
    
       return {"content": response['output']}
    

@app.get("/top-product")
def get_top_product():
    """
    Retorna o produto mais vendido.
    """ 
    response = agent.execute("Quais são os produtos mais vendidos e suas quantidades")
    return {"content": response['output']}


# Função para iniciar o Streamlit
def start_streamlit():
    streamlit_command = ["streamlit", "run", "./src/playground/playground.py"]
    subprocess.Popen(streamlit_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Iniciar a API e o Streamlit
if __name__ == "__main__":
    # Inicia o Streamlit em uma thread separada
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()

    # Inicia a API FastAPI
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
