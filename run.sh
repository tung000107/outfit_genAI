#!/bin/bash
# OutfitGenAI 啟動腳本

echo "🚀 啟動 OutfitGenAI..."
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  找不到 .env 檔案，請先複製 .env.example 並設定 API Key"
    echo "   cp .env.example .env"
    echo "   然後編輯 .env 檔案，填入你的 OpenAI API Key"
    exit 1
fi

# Method 1: Run Streamlit only (local access)
# streamlit run app.py

# Method 2: Run with ngrok (public access)
python run_with_ngrok.py
