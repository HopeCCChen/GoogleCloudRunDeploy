# 使用官方的 Python 輕量版映像檔作為基底
# Slim 版本體積較小，適合正式環境部署
FROM python:3.9-slim

# 設定容器內的工作目錄
WORKDIR /app

# 將當前目錄的所有檔案複製到容器內的 /app 目錄
COPY . .

# 安裝 requirements.txt 中列出的所有依賴套件
# --no-cache-dir 可以減少映像檔體積
RUN pip install --no-cache-dir -r requirements.txt

# 設定容器啟動時執行的指令
# 使用 gunicorn 作為 Production WSGI Server
# --bind :$PORT: 綁定 Cloud Run 指定的 Port
# --workers 1 --threads 8: 設定執行緒數量，提高並發處理能力
# --timeout 0: 防止 Cloud Run 在冷啟動時逾時
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app