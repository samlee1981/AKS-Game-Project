# 使用輕量級的 Python 映像檔
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /appbc

# 複製檔案
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app_bc.py .

# 開放 5000 埠號
EXPOSE 5000

# 執行程式
CMD ["python", "app_bc.py"]