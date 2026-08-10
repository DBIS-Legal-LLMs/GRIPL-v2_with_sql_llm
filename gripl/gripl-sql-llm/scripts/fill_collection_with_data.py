from app.chroma_database_client.chroma_db_client import ChromaDatabaseClient
from sentence_transformers import SentenceTransformer


# TODO replace with original documents
documents = [
    "Die Verarbeitung personenbezogener Daten ist nur unter bestimmten Voraussetzungen zulässig.",
    "Betroffene Personen haben das Recht auf Auskunft über ihre gespeicherten personenbezogenen Daten.",
    "Personenbezogene Daten müssen nach dem Grundsatz der Datenminimierung verarbeitet werden."
]

model = SentenceTransformer('intfloat/multilingual-e5-small')

chroma_db_client = ChromaDatabaseClient(
    model
)

chroma_db_client.fill_collection(documents)



