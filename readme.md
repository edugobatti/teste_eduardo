# Sales Insights API

Esta API fornece insights de vendas utilizando um agente OpenAI para responder perguntas sobre vendas e listar os produtos mais vendidos.

## Tecnologias Utilizadas
- Langchain
- FastAPI
- OpenAI API
- Pydantic
- Uvicorn

## Como Executar

### Pré-requisitos
- Python 3.11+
- Instalar dependências:
  ```bash
  pip install -r requeriments.txt
  ```

### Iniciar a API
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```
### Iniciar a API
#### É necessario colocar a API key no .env
```bash
OPENAI_API_KEY=
```


## Endpoints Disponíveis

### `GET /sales-insights`
**Descrição:** Retorna insights baseados em uma pergunta fornecida.

**Parâmetro de Query:**
- `question` (string, opcional): Pergunta sobre insights de vendas.

**Exemplo de Requisição:**
```bash
curl -X 'GET' 'sales-insights?question={"quantos usuarios tenho na base"}' -H 'accept: application/json'
```

**Resposta Exemplo:**
```json
{
   "response": "Você tem 5 usuários na base de dados."
}
```

### `GET /top-product`
**Descrição:** Retorna o produto mais vendido.

**Exemplo de Requisição:**
```bash
curl -X 'GET' 'http://localhost:5000/top-product' -H 'accept: application/json'
```

**Resposta Exemplo:**
```json
{
  "response": "Os produtos mais vendidos e suas quantidades são:\n\n1. **Product E** - 39 unidades\n2. **Product A** - 22 unidades\n3. **Product B** - 19 unidades\n4. **Product C** - 18 unidades\n5. **Product D** - 14 unidades"
}
```



