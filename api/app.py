from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter

app = FastAPI()

llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = SimpleDirectoryReader("docs").load_data()

parser = SentenceSplitter(chunk_size=500, chunk_overlap=50)

index = VectorStoreIndex.from_documents(
    documents,
    transformations=[parser],
    embed_model=embed_model
)

query_engine = index.as_query_engine(llm=llm)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/preguntar")
def preguntar(q: str):
    response = query_engine.query(q)
    return {"respuesta": str(response)}