import os
from typing import List, Dict, Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from embeddings import EmbeddingModel
from milvus_client import MilvusClient

app = FastAPI(title="Technical Document Search Platform")

# Allow local dev origins
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Initialize embedding model and Milvus client
_embedding_model = EmbeddingModel.get_instance()
_milvus = MilvusClient()


@app.get("/search")
async def search(query: str = Query(..., description="Natural language query"), top_k: int = 50) -> Dict[str, Any]:
	vector = _embedding_model.embed_text(query)
	results = _milvus.search([vector], top_k=top_k)

	items: List[Dict[str, Any]] = []
	seen_abstracts = set()  # Track seen abstracts to avoid duplicates
	seen_titles = set()      # Track seen titles to avoid duplicates
	
	for hits in results:
		for hit in hits:
			try:
				title = hit.entity.get("title")
				abstract = hit.entity.get("abstract")
				year = hit.entity.get("year")
			except Exception:
				title = None
				abstract = None
				year = None
			
			# Skip if we've seen this exact abstract or title before
			if abstract in seen_abstracts or title in seen_titles:
				continue
				
			# Add to seen sets
			seen_abstracts.add(abstract)
			seen_titles.add(title)
			
			# Truncate abstract if too long
			if abstract and len(abstract) > 300:
				abstract = abstract[:300] + "..."
			
			items.append({
				"id": hit.id,
				"title": title,
				"abstract": abstract,
				"year": int(year) if year is not None else None,
				"score": float(hit.distance),
			})
			
			# Limit results to avoid too many duplicates
			if len(items) >= 20:
				break

	return {"query": query, "count": len(items), "results": items}

