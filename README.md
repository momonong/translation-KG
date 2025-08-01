# translation-KG

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

It includes components based on [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate), which is also licensed under AGPL-3.0.

If you modify and distribute this project (including making it available as a network service), please ensure your changes are made available under the same license.

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
poetry run libretranslate --load-only en,zh --url-prefix libre-translate --port 5090
poetry run uvicorn api.main:app --reload
```

## Clean data
```
0 4 * * * cd /your/project/path && python -c "from routers.pdf_manage import clean_old_pdfs; clean_old_pdfs(2)"
```