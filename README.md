# FastAPI Search Engine

This repository is a small search service built with FastAPI that demonstrates
multiple search strategies over a small product dataset:

Architecture (high level)

The project is organised into four primary layers that follow SOLID principles
and are intentionally isolated from one another:

- API: HTTP routing and request/response models (see `src/infra/API/search.py`).
- Services: business logic and orchestration of search engines (`src/core/services`).
- SearchEngine: pluggable search engine implementations (fuzzy, vector) in
	`src/infra/search_engines/`.
- Database: persistence / data access implementations (`src/infra/db/`).

This separation keeps responsibilities narrow, makes components easy to
replace or test independently, and allows the `SearchService` layer to
compose different search strategies without leaking implementation details.

- Fuzzy text search using RapidFuzz
- Vector semantic search using SentenceTransformers + FAISS
- Exact / filter-based search over product fields
- Hybrid Search - Unite Algorythm of Vector and Fuzzy

The project includes a thin `SearchService` layer that picks between engines
and simple in-memory and SQLite-backed data access interfaces.

---

**Quick summary**

- What you get: a working HTTP API with endpoints for fuzzy, vector,
	hybrid and filter searches over the sample product dataset in
	`data_files/products.json`.
- Where to look: core logic lives under `src/infra/search_engines/`.

---

**Requirements / Notes**

- The project is configured with `pyproject.toml` and targets Python 3.13.
- Key third-party libraries used: `fastapi`, `uvicorn`, `sentence-transformers`,
	`faiss-cpu`, `rapidfuzz`, and `apexdevkit` (used to run the Uvicorn server).

---

**How to run (step-by-step)**

1. Ensure you have Python 3.13 installed.

2a. (Recommended) Using Poetry

	 - Install poetry (if you don't have it):

		 ```bash
		 pip install --user poetry
		 ```

     - clone repository:

          ```bash
         git clone https://github.com/azhgh22/FastAPI-Search-Engine.git
         cd FastAPI-Search-Engine
		 ```

	 - Install dependencies:

		 ```bash
         poetry config virtualenvs.in-project true
		 poetry install
		 ```

	 - Run the app:

		 ```bash
		 poetry run python -m src.runner.main
		 ```

3.   - After starting server visit:
        ```bash
          [text](http://0.0.0.0:8000/docs)
        ```

---

**API endpoints & example queries**

The router is mounted at `/search` and exposes these endpoints:

- `GET /search/` — simple health message
- `POST /search/vectorsearch` — vector (semantic) search
- `POST /search/fuzzysearch` — fuzzy text search
- `POST /search/hybridsearch` — a hybrid method combining fields
- `POST /search/filter` — exact/filtered matches (by price, country, brand)