# **Google Cloud Run x LINE Bot 範例專案**

這是一個示範如何將 Python Flask LINE Bot 部署至 Google Cloud Run 的專案。專案使用 Docker 容器化技術，並透過 Gunicorn 作為 WSGI 伺服器來處理並發請求。

## **📁 檔案結構**

* main.py: 應用程式主程式 (Flask \+ LINE Bot SDK)。  
* requirements.txt: Python 依賴套件清單。  
* Dockerfile: 定義容器建置流程與啟動指令。

## **🚀 本地端開發 (Local Development)**

1. **安裝依賴套件**  
   pip install \-r requirements.txt

2. 設定環境變數  
   請確保環境中有以下變數 (或在程式中暫時寫死)：  
   * CHANNEL\_ACCESS\_TOKEN  
   * CHANNEL\_SECRET  
3. **啟動伺服器**  
   python main.py

## **🐳 Docker 部署說明**

本專案使用 Dockerfile 進行容器化。

### **啟動指令詳解**

在 Dockerfile 的最後一行，我們使用了以下指令來啟動服務：

CMD exec gunicorn \--bind :$PORT \--workers 1 \--threads 8 \--timeout 0 main:app

參數說明：

* **exec gunicorn**: 使用 Gunicorn 作為生產環境的 WSGI HTTP Server。  
* **\--bind :$PORT**: 綁定 Google Cloud Run 自動注入的環境變數 $PORT (通常為 8080)。  
* **\--workers 1**: 設定 Worker Process 的數量。對於 Cloud Run 這種無伺服器環境，通常建議設為 1，並利用執行緒處理並發。  
* **\--threads 8**: 每個 Worker 內的執行緒數量。這允許單個容器實例同時處理多個請求 (Concurrency)。  
* **\--timeout 0**: 將逾時設為 0 (無限制)，這是 Cloud Run 的官方建議設定，用以防止在冷啟動 (Cold Start) 時因等待過久而被 Gunicorn 強制殺死。  
* **main:app**: 指定要執行的 Python 模組 (main.py) 與 Flask 實例名稱 (app)。

### **部署指令 (Google Cloud SDK)**

在開始部署之前，建議先查詢並確認您的 GCP 專案資訊，以便填寫指令中的 \[PROJECT-ID\]。

1. **登入並查詢專案資訊**  
   \# 登入 Google Cloud  
   gcloud auth login

   \# 列出帳號下所有專案 (記下您的 PROJECT\_ID)  
   gcloud projects list

   \# 設定當前操作的專案 (選用)  
   gcloud config set project \[PROJECT-ID\]

2. **建置並上傳映像檔**  
   \# 將 \[PROJECT-ID\] 替換為上一步查詢到的 ID  
   gcloud builds submit \--tag gcr.io/\[PROJECT-ID\]/line-bot

3. **部署至 Cloud Run**  
   gcloud run deploy line-bot \\  
     \--image gcr.io/\[PROJECT-ID\]/line-bot \\  
     \--platform managed \\  
     \--region asia-northeast1 \\  
     \--allow-unauthenticated \\  
     \--set-env-vars="CHANNEL\_ACCESS\_TOKEN=您的Token,CHANNEL\_SECRET=您的Secret"  
