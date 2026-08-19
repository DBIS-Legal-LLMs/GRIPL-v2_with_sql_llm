from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import traceback


class ChromaDatabaseClient:
    def __init__(self,
                 embedding_model: SentenceTransformer):
        self.db_path = Path(__file__).resolve().parent / "embeddings" / "dsgvo"
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.collection_name = "dsgvo_collection"
        self.embedding_model = embedding_model


    def get_collection(self):
        client = chromadb.PersistentClient(path=str(self.db_path))

        return client.get_or_create_collection(
            name=self.collection_name,
        )

    def fill_collection(self,documents: list[str] ):
        collection = self.get_collection()

        embeddings = self.embedding_model.encode(
            documents,
            convert_to_numpy=True
        ).tolist()

        ids = [str(i) for i in range(len(documents))]

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )


    def get_top_k_results(self, query):

        try:
            collection = self.get_collection()

            embedded_query = self.embedding_model.encode(query)

            results = collection.query(
                query_embeddings=[embedded_query.tolist()],
                n_results=5
            )

            return results["documents"][0]
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return []


