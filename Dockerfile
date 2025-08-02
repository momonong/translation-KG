FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製 poetry 設定檔（先複製，提高 cache 機會）
COPY pyproject.toml poetry.lock ./

# 安裝 Poetry  
RUN pip install poetry

# 安裝依賴（不建立虛擬環境，直接用系統 env）
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# 複製專案所有檔案（包含 code, data, static...）
COPY . .

# 啟動 FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
