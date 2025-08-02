# translation-KG

Download the extention pack through [this link](https://drive.google.com/file/d/1yt7KNJW46KOLhjoAnSZsezYzy9b4Y7e7/view?usp=sharing).

## Knowledge Graph

[data file link](https://u.pcloud.link/publink/show?code=kZu6Ph5ZcKL2TVPtKgupG9cUmR5y98UD7Tik)

```
# data preparation
poetry run python -m scripts.csv_filter
poetry run python -m scripts.build_graph
poetry run python -m scripts.export_graph
```

## Translating

```
poetry run uvicorn api.main:app --reload
```

## Clean data

```
0 4 * * * cd /your/project/path && python -c "from routers.pdf_manage import clean_old_pdfs; clean_old_pdfs(2)"
```

## Docker
```
docker build --platform linux/amd64 -t lexilight:latest .
```