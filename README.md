# OutfitGenAI

AI 個人化穿搭生成系統 - 結合 GPT-4o 與 DALL-E 3，根據你的需求生成專屬穿搭建議與示意圖。

## 功能特色

- **照片分析**：上傳照片，AI 會分析你的整體氣質與色彩
- **文字描述**：輸入風格需求（如韓系、日系、職場正式等）
- **多選項設定**：選擇季節、場合、色調偏好
- **穿搭建議**：GPT-4o 生成詳細的穿搭文字建議
- **視覺呈現**：DALL-E 3 生成時尚插畫風格的穿搭示意圖

## 系統架構

```
使用者輸入 (照片 + 風格描述 + 按鈕選擇)
    ↓
GPT-4o (with vision) → 文字穿搭建議 + 圖像 Prompt
    ↓
DALL-E 3 → 穿搭示意圖
    ↓
Streamlit 前端展示
```

## 技術棧

- **前端**：Streamlit
- **文字生成**：OpenAI GPT-4o API
- **圖像生成**：OpenAI DALL-E 3 API
- **外部存取**：ngrok

## 安裝與執行

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

```bash
cp .env.example .env
```

編輯 `.env` 檔案，填入你的 API Key：

```
OPENAI_API_KEY=your_openai_api_key_here
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here  # 選填，僅外部存取需要
```

### 3. 執行應用程式

**本地執行：**

```bash
streamlit run app.py
```

**使用 ngrok（外部存取）：**

```bash
python run_with_ngrok.py
```

或

```bash
./run.sh
```

## 專案結構

```
.
├── app.py                 # 主要 Streamlit 應用程式
├── run_with_ngrok.py      # ngrok 啟動腳本
├── run.sh                 # Shell 啟動腳本
├── requirements.txt       # Python 依賴
├── .env                   # 環境變數（API Keys）
├── .env.example           # 環境變數範例
└── utils/
    ├── __init__.py
    ├── llm.py             # LLM 整合（GPT-4o）
    └── image_gen.py       # 圖像生成（DALL-E 3）
```

## 使用方式

1. 開啟應用程式後，在左側面板輸入你的需求
2. **上傳照片**（選填）：系統會分析照片中的氣質與色彩
3. **描述風格**：輸入想要的穿搭風格
4. **選擇季節**：春季 / 夏季 / 秋季 / 冬季
5. **選擇場合**：約會 / 工作 / 校園 / 旅行
6. **選擇色調**：冷色系 / 暖色系 / 大地色 / 黑白灰
7. 點擊「生成穿搭建議」按鈕
8. 在右側查看 AI 生成的穿搭建議與示意圖

## 注意事項

- 需要有效的 OpenAI API Key 才能使用
- 上傳的照片僅用於風格分析，不會直接用於生成圖片
- 圖像生成可能需要數秒時間，請耐心等待

## 授權

陽明交通大學 GenAI 期末專案
