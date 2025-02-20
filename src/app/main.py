import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from src.agents.agent import OpenAIAgent
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
    
       return {"response": response['output']}
    

@app.get("/top-product")
def get_top_product():
    """
    Retorna o produto mais vendido.
    """ 
    response = agent.execute("Quais são os produtos mais vendidos e suas quantidades")
    return {"response": response['output']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
