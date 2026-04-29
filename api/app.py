from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import os

app = FastAPI()

# 🔹 Modelo
llm = Ollama(
    model="llama3",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

# 🔹 Embeddings
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🔹 Cargar documentos
documents = SimpleDirectoryReader("docs").load_data()

parser = SentenceSplitter(chunk_size=500, chunk_overlap=50)

index = VectorStoreIndex.from_documents(
    documents,
    transformations=[parser],
    embed_model=embed_model
)

query_engine = index.as_query_engine(llm=llm)


# 🧾 Request schema
class ChatRequest(BaseModel):
    message: str


# 🌐 Endpoint tipo Claude / GPT
@app.post("/chat")
def chat(req: ChatRequest):
    response = query_engine.query(req.message)

    return {
        "response": str(response),
        "model": "llama3-local",
        "status": "ok"
    }


# 🧪 Health check
@app.get("/")
def root():
    return {"status": "running"}
