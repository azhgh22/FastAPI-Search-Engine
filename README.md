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

         git clone https://github.com/azhgh22/FastAPI-Search-Engine.git
		 ```

	 - Install dependencies:

		 ```bash
	 - Run the app:

		 ```bash
		 poetry run python -m src.runner.main

3.   - After starting server visit:
        ```bash
        ```

**API endpoints & example queries**
The router is mounted at `/search` and exposes these endpoints:

- `GET /search/` — simple health message
- `POST /search/hybridsearch` — a hybrid method combining fields
- `POST /search/filter` — exact/filtered matches (by price, country, brand)

**FastAPI UI examples**

You can paste these JSON bodies directly into the request body area in the
FastAPI docs UI (http://127.0.0.1:8000/docs) when you click "Try it out".

- Vector search request body (matches `SearchRequest`):

```json
{
	"name": "",
	"description": "wireless headphones with noise cancellation",
	"country": "",
	"brand": "",
	"price": ""
}
```

- Fuzzy search request body (matches `FuzzySearchRequest`):

```json
{
	"name": "",
	"description": "Cotn",
	"country": "",
	"brand": ""
}
```

- Hybrid search request body (matches `SearchRequest`):

```json
{
	"name": "",
	"description": "noise cancelling headphones",
	"country": "",
	"brand": "Nordic",
	"price": ""
}
```

- Filter search request body (matches `FilterRequest`):

	"max_price": 500.0,
**Detailed algorithm descriptions**

- **Fuzzy search** (`src/infra/search_engines/fuzzy_search.py`):
	- Representation: each product is converted to a single searchable string
		composed of `name`, `brand`, `description`, and `country`. `name` and
		`brand` are duplicated in the string to increase their relative weight.
	- Matching pipeline: two RapidFuzz scorers are used — `token_set_ratio`
		(for robust set-based token matching) and `partial_token_sort_ratio`
		(for partial/substring matches). The engine extracts candidates with
		both scorers, builds id→score maps, takes the intersection of strong
		matches and then fills up remaining slots from partial matches.
	- Strengths: typo tolerance, strong token matching for short names and
		brand lookups. Weaknesses: token-based only (no semantic understanding)
		and decreased quality for long descriptive text.

- **Vector (semantic) search** (`src/infra/search_engines/vectorsearch_engine.py`):
	- Representation: product texts are encoded into dense vectors using the
		SentenceTransformers model `all-MiniLM-L6-v2`.
	- Indexing: vectors are normalized (L2) and stored in a FAISS
		`IndexFlatIP` (inner-product on normalized vectors ≈ cosine similarity).
		The index and an `id_map.json` are persisted under
		`data_files/vector_search_all_MiniLM_L6_v2` so rebuilds are not required
		on every start.
	- Querying: the query string is encoded, normalized, and the FAISS index
		is searched for nearest neighbors; indices map back to product IDs and
		then to product records.
	- Strengths: captures semantic similarity (synonyms, paraphrases). Weaknesses:
		encoding and index-building cost on first run; `IndexFlatIP` is exact and
		scales linearly — consider IVF/HNSW/PQ for larger datasets.

- **Hybrid search** (`src/core/services/classes/search_service.py`):
	- Implemented flow: run a vector search with a larger `k` to collect a
		candidate set (semantic pre-filter), create a temporary in-memory DB
		seeded with those candidates, then run the fuzzy engine over this
		reduced set and return the fuzzy-ordered results.
	- Rationale: vectors broaden the candidate pool to include conceptually
		relevant items; fuzzy matching then enforces token-level precision and
		ranking (useful when users include brand or model tokens).
	- Limitation: current implementation restricts to fuzzy ordering of vector
		candidates and does not fuse or normalize vector + fuzzy scores. A
		stronger hybrid would compute both scores and merge them (weighted sum,
		reciprocal rank fusion, or learning-to-rank).

- **Filter / exact search** (`src/infra/db/inmem_db.py`, `src/infra/db/sqllite_db.py`):
	- Simple predicate-based filtering on structured fields (`name`,
		`country`, `brand`, `min_price` / `max_price`). Use this when exact
		constraints or numeric ranges are required.

Additional notes

- **Preprocessing**: inputs are normalized (lowercased / stripped). Some
	fields are repeated in the text representation as a lightweight weighting
	strategy.

**What works well and what is still weak / unfinished**

- **What works well**
	- **Hybrid search** (see `src/core/services/classes/search_service.py`): the
		current hybrid approach works reliably in practice — it first retrieves
		semantically-strong candidate products using the vector search and then
		selects/ranks the best matches among those candidates using the
		token-aware fuzzy search. This combination gives good recall from the
		semantic model and good precision for brand/model tokens or partial IDs.

- **What is still weak / unfinished**
	- **Filtering:** the filtering functionality currently relies on the DB
		layer (SQL/predicate-based filtering in `src/infra/db/*`). This works
		for structured constraints but is separate from the vector search.
		In particular, vector search alone cannot reliably enforce structured
		filters such as price ranges (semantic vectors do not encode numeric
		inequality constraints well).
	- **Improvement direction:** enhance filtering by combining classical
		DB predicates with learned components — for example, (1) apply strict
		structured filters in SQL first, then run vector/fuzzy retrieval on the
		filtered set; (2) Or, Use stronger embeding model, to gice much more importance to numberic values. Or imrove imput format, that enables model to pay attention to semantics that are not important for current model.






