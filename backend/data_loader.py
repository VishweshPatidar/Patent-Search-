import os
import itertools
from typing import List, Dict, Any

import pandas as pd

from embeddings import EmbeddingModel
from milvus_client import MilvusClient


def read_csvs(csv_paths: List[str]) -> pd.DataFrame:
	frames = []
	for path in csv_paths:
		if os.path.exists(path):
			print(f"Loading data from: {path}")
			df = pd.read_csv(path)
			print(f"  - Loaded {len(df)} rows")
			frames.append(df)
		else:
			print(f"File not found: {path}")
	
	if not frames:
		print("No data files found!")
		return pd.DataFrame(columns=["title", "abstract", "year"])
	
	df = pd.concat(frames, ignore_index=True)
	print(f"Total combined rows: {len(df)}")
	
	# Basic cleaning
	df = df.dropna(subset=["title", "abstract"]).copy()
	df["year"] = pd.to_numeric(df.get("year", 0), errors="coerce").fillna(0).astype(int)
	
	# Filter out very short abstracts
	df = df[df['abstract'].str.len() >= 20]
	
	print(f"After cleaning: {len(df)} rows")
	return df


def chunk_iterable(iterable, chunk_size: int):
	it = iter(iterable)
	while True:
		chunk = list(itertools.islice(it, chunk_size))
		if not chunk:
			break
		yield chunk


def main():
	print("Starting data loading process...")
	
	data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
	
	# Use real data from OpenAlex and PatentsView APIs
	csv_paths = [
		os.path.join(data_dir, "real_data_combined.csv"),  # Combined real data
		os.path.join(data_dir, "real_papers.csv"),        # OpenAlex research papers
		os.path.join(data_dir, "real_patents.csv"),       # PatentsView patents
	]
	
	df = read_csvs(csv_paths)
	if df.empty:
		print("No real data found. Please run real_data_integration.py first.")
		print("This will fetch real data from OpenAlex and PatentsView APIs.")
		return

	print(f"Processing {len(df)} documents...")
	
	# Initialize embedding model and Milvus client
	print("Loading embedding model...")
	embedder = EmbeddingModel.get_instance()
	
	print("Connecting to Milvus...")
	milvus = MilvusClient()
	
	print("Collection ready...")
	
	# Convert to documents
	documents = []
	for _, row in df.iterrows():
		doc = {
			'id': str(row.get('id', len(documents) + 1)),
			'title': str(row['title']),
			'abstract': str(row['abstract']),
			'year': int(row['year']) if pd.notna(row['year']) else None,
			'source': row.get('source_database', row.get('source', 'unknown')),
			'document_type': row.get('document_type', 'unknown')
		}
		documents.append(doc)

	print(f"Processing {len(documents)} documents...")
	
	# Insert documents in batches
	batch_size = 500
	total_batches = (len(documents) + batch_size - 1) // batch_size
	
	for i in range(0, len(documents), batch_size):
		batch = documents[i:i + batch_size]
		batch_num = (i // batch_size) + 1
		
		print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} documents)...")
		
		# Generate embeddings for batch
		texts = [f"{doc['title']} {doc['abstract']}" for doc in batch]
		embeddings = embedder.embed_texts(texts)
		
		# Add embeddings to documents
		for i, doc in enumerate(batch):
			doc['embeddings'] = embeddings[i].tolist()
		
		# Insert into Milvus
		milvus.insert_documents(batch)
		
		print(f"Batch {batch_num} completed")
	
	print("Data loading completed successfully!")
	print(f"Total documents inserted: {len(documents)}")


if __name__ == "__main__":
	main()

