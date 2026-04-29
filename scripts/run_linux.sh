#!/bin/bash

source venv/bin/activate

echo "🚀 Iniciando API..."
uvicorn app:app --host 0.0.0.0 --port 8000 --reload