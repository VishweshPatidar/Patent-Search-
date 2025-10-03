from typing import List, Dict, Any, Optional

from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)


class MilvusClient:
    def __init__(self, host: str = "localhost", port: str = "19530", collection_name: str = "documents") -> None:
        self.host = host
        self.port = port
        self.collection_name = collection_name
        connections.connect(alias="default", host=self.host, port=self.port)
        self.collection = self._create_or_load_collection()

    def _create_or_load_collection(self) -> Collection:
        dim = 384
        if not utility.has_collection(self.collection_name):
            id_field = FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=64, is_primary=True, auto_id=False)
            title_field = FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512)
            abstract_field = FieldSchema(name="abstract", dtype=DataType.VARCHAR, max_length=4096)
            year_field = FieldSchema(name="year", dtype=DataType.INT64)
            vector_field = FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)

            schema = CollectionSchema(fields=[id_field, title_field, abstract_field, year_field, vector_field], description="Technical documents: patents and papers")
            collection = Collection(name=self.collection_name, schema=schema)

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 1024},
            }
            collection.create_index(field_name="embeddings", index_params=index_params)
            collection.load()
            return collection
        else:
            collection = Collection(self.collection_name)
            try:
                collection.indexes
            except Exception:
                index_params = {
                    "index_type": "IVF_FLAT",
                    "metric_type": "IP",
                    "params": {"nlist": 1024},
                }
                collection.create_index(field_name="embeddings", index_params=index_params)
            collection.load()
            return collection

    def insert_documents(self, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            return
        # Sort by ID as string, not int
        rows_sorted = sorted(rows, key=lambda r: str(r["id"]))
        ids = [str(r["id"]) for r in rows_sorted]
        titles = [str(r["title"]) for r in rows_sorted]
        abstracts = [str(r["abstract"]) for r in rows_sorted]
        years = [int(r["year"]) if r["year"] is not None else 0 for r in rows_sorted]
        vectors = [list(map(float, r["embeddings"])) for r in rows_sorted]
        self.collection.insert([ids, titles, abstracts, years, vectors])
        self.collection.flush()

    def search(self, query_vectors, top_k: int = 50, output_fields: Optional[List[str]] = None):
        if output_fields is None:
            output_fields = ["title", "abstract", "year"]
        search_params = {"metric_type": "IP", "params": {"nprobe": 16}}
        results = self.collection.search(
            data=query_vectors,
            anns_field="embeddings",
            param=search_params,
            limit=top_k,
            output_fields=output_fields,
        )
        return results

