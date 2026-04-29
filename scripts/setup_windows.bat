@echo off

echo 🔧 Creando entorno virtual...
python -m venv venv

call venv\Scripts\activate

echo 📦 Instalando dependencias...
pip install --upgrade pip
pip install -r ..\api\requirements.txt

echo ⚠️ Asegurate de tener Ollama instalado manualmente
echo https://ollama.com/download

echo 📥 Descarga modelo:
echo ollama pull llama3

echo ✅ Setup completo
pause