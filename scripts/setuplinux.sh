#!/bin/bash

echo "🔧 Creando entorno virtual..."

python3 -m venv linuxenv
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r ../api/requirements.txt

echo "🤖 Verificando Ollama..."

if ! command -v ollama &> /dev/null
then
    echo "Instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "📥 Descargando modelo..."
ollama pull llama3

echo "✅ Setup completo"
