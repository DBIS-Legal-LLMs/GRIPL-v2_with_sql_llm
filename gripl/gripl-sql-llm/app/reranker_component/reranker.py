import traceback
from sentence_transformers import CrossEncoder

class Reranker:

    def __init__(self,
                 model_name: str
                 ):
        self.top_k = 3
        self.cross_encoder_model = CrossEncoder(
            model_name=model_name,
        )

    def get_reranked_results(self, query: str, documents: list[str]) -> list[str]:
        try:

            pairs = [
                [query, doc]
                for doc in documents
            ]

            scores = self.cross_encoder_model.predict(pairs)

            return [
                doc
                for _, doc in sorted(
                    zip(scores, documents),
                    reverse=True
                )[:self.top_k]
            ]

        except Exception as e:
            print("error in reranker ")
            print(traceback.format_exc())
            return []

