"""
Run OutfitGenAI with ngrok tunnel for external access.
This script starts the Streamlit app and creates an ngrok tunnel.
"""
import os
import subprocess
import time
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

NGROK_PATH = "/opt/homebrew/bin/ngrok"

def main():
    # Check for ngrok auth token
    ngrok_token = os.getenv("NGROK_AUTH_TOKEN")

    if ngrok_token and ngrok_token != "your_ngrok_auth_token_here":
        print("🔧 配置 ngrok 認證...")
        subprocess.run([NGROK_PATH, "config", "add-authtoken", ngrok_token], check=True)
    else:
        print("⚠️  未設定 NGROK_AUTH_TOKEN，請在 .env 檔案中設定")
        print("   取得 token: https://dashboard.ngrok.com/get-started/your-authtoken")
        return

    print("🚀 啟動 OutfitGenAI...")
    print("=" * 50)

    # Start Streamlit in background
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for Streamlit to start
    time.sleep(3)
    print("✅ Streamlit 已啟動在 http://localhost:8501")

    # Start ngrok tunnel
    print("🌐 建立 ngrok tunnel...")
    ngrok_process = subprocess.Popen(
        [NGROK_PATH, "http", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for ngrok to start
    time.sleep(3)

    # Get public URL from ngrok API
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as response:
            data = json.loads(response.read().decode())
            if data.get("tunnels"):
                public_url = data["tunnels"][0]["public_url"]
                print("=" * 50)
                print(f"🎉 公開網址: {public_url}")
                print("=" * 50)
                print("\n📋 請將此網址分享給助教！")
                print("按 Ctrl+C 停止服務\n")
            else:
                print("❌ 無法取得 ngrok URL")
    except Exception as e:
        print(f"❌ 無法連接 ngrok API: {e}")

    try:
        # Keep running
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n⏹️  正在停止服務...")
        ngrok_process.terminate()
        streamlit_process.terminate()
        print("👋 服務已停止")


if __name__ == "__main__":
    main()
