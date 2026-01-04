# Google Cloud Run x LINE Bot 範例專案

這是一個示範如何將 Python Flask LINE Bot 部署至 Google Cloud Run 的專案。專案使用 Docker 容器化技術，並透過 Gunicorn 作為 WSGI 伺服器來處理並發請求。

## 📁 檔案結構

```
line-bot-cloudrun/
├── main.py              # 應用程式主程式 (Flask + LINE Bot SDK)
├── requirements.txt     # Python 依賴套件清單
├── Dockerfile          # 定義容器建置流程與啟動指令
└── README.md           # 本說明文件
```

## 🚀 本地端開發

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

請確保環境中有以下變數（或在程式中暫時寫死）：

- `CHANNEL_ACCESS_TOKEN`
- `CHANNEL_SECRET`

### 3. 啟動伺服器

```bash
python main.py
```

## 🐳 Docker 部署說明

本專案使用 Dockerfile 進行容器化。

### 啟動指令詳解

在 Dockerfile 的最後一行，我們使用了以下指令來啟動服務：

```dockerfile
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

**參數說明：**

| 參數 | 說明 |
|------|------|
| `exec gunicorn` | 使用 Gunicorn 作為生產環境的 WSGI HTTP Server |
| `--bind :$PORT` | 綁定 Google Cloud Run 自動注入的環境變數 `$PORT`（通常為 8080） |
| `--workers 1` | 設定 Worker Process 的數量。對於 Cloud Run 這種無伺服器環境，通常建議設為 1，並利用執行緒處理並發 |
| `--threads 8` | 每個 Worker 內的執行緒數量。這允許單個容器實例同時處理多個請求（Concurrency） |
| `--timeout 0` | 將逾時設為 0（無限制），這是 Cloud Run 的官方建議設定，用以防止在冷啟動（Cold Start）時因等待過久而被 Gunicorn 強制終止 |
| `main:app` | 指定要執行的 Python 模組（main.py）與 Flask 實例名稱（app） |

## ☁️ 部署至 Google Cloud Run

在開始部署之前，建議先查詢並確認您的 GCP 專案資訊，以便填寫指令中的 `[PROJECT-ID]`。

### 步驟 1：登入並查詢專案資訊

```bash
# 登入 Google Cloud
gcloud auth login

# 列出帳號下所有專案（記下您的 PROJECT_ID）
gcloud projects list

# 設定當前操作的專案（選用）
gcloud config set project [PROJECT-ID]
```

### 步驟 2：建置並上傳映像檔

```bash
# 將 [PROJECT-ID] 替換為上一步查詢到的 ID
gcloud builds submit --tag gcr.io/[PROJECT-ID]/line-bot
```

### 步驟 3：部署至 Cloud Run

```bash
gcloud run deploy line-bot \
  --image gcr.io/[PROJECT-ID]/line-bot \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars="CHANNEL_ACCESS_TOKEN=您的Token,CHANNEL_SECRET=您的Secret"
```

**注意事項：**

- 請將 `[PROJECT-ID]` 替換為您的 Google Cloud 專案 ID
- 請將 `您的Token` 和 `您的Secret` 替換為您在 LINE Developers Console 取得的實際值
- 部署完成後，系統會顯示服務的 URL，格式類似：`https://line-bot-xxxxxxxxxx-an.a.run.app`

### 步驟 4：設定 LINE Bot Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Messaging API Channel
3. 在「Messaging API」頁籤中，找到「Webhook URL」
4. 填入您的 Cloud Run 服務 URL，並加上 `/callback` 路徑，例如：
   ```
   https://line-bot-xxxxxxxxxx-an.a.run.app/callback
   ```
5. 點擊「Verify」驗證 Webhook
6. 開啟「Use webhook」選項

## 🔧 常見問題

### 如何查看服務日誌？

```bash
gcloud run services logs read line-bot --region=asia-northeast1
```

### 如何更新服務？

修改程式碼後，重新執行步驟 2 和步驟 3。

### 如何刪除服務？

```bash
gcloud run services delete line-bot --region=asia-northeast1
```

## 📚 相關資源

- [Google Cloud Run 官方文件](https://cloud.google.com/run/docs)
- [LINE Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)
- [Gunicorn 官方文件](https://docs.gunicorn.org/)

## 📄 授權

MIT License