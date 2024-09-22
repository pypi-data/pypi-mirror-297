from langchain_community.vectorstores import Chroma
from typing import Dict, List, Tuple
import numpy as np
import chromadb
from chromadb.utils import embedding_functions

class TestEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, size: int = 10):
        self.size = size

    def __call__(self, texts: List[str]) -> List[List[float]]:
        return [np.random.rand(self.size).tolist() for _ in texts]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self(texts)

    def embed_query(self, text: str) -> List[float]:
        return np.random.rand(self.size).tolist()

def get_embeddings_by_column(chroma_collection: Chroma, column_name: str) -> Tuple[Dict[str, List[np.ndarray]], Dict[str, Dict]]:
    """
    Group embeddings and metadata by a specific column value.

    Parameters:
        chroma_collection (Chroma): The Chroma collection to extract embeddings from.
        column_name (str): The metadata field by which to group embeddings.

    Returns:
        Tuple[Dict[str, List[np.ndarray]], Dict[str, Dict]]: 
            A tuple containing two dictionaries:
            1. Embeddings grouped by column value
            2. Metadata grouped by column value
    """
    embeddings_by_column = {}
    metadata_by_column = {}

    # Get all documents from the Chroma collection
    all_data = chroma_collection._collection.get(include=['embeddings', 'metadatas'])

    for i, metadata in enumerate(all_data['metadatas']):
        column_value = metadata.get(column_name)
        if column_value is not None:
            if column_value not in embeddings_by_column:
                embeddings_by_column[column_value] = []
                metadata_by_column[column_value] = metadata
            embeddings_by_column[column_value].append(all_data['embeddings'][i])

    return embeddings_by_column, metadata_by_column

def create_new_chroma_collection(representative_embeddings: Dict[str, np.ndarray], metadata_by_column: Dict[str, Dict]) -> Chroma:
    """
    Create a new Chroma collection with aggregated embeddings.

    Parameters:
        representative_embeddings (Dict[str, np.ndarray]): Aggregated embeddings for each group.
        metadata_by_column (Dict[str, Dict]): Metadata for each group.

    Returns:
        Chroma: A new Chroma collection with aggregated embeddings.
    """
    client = chromadb.Client()
    embedding_function = TestEmbeddingFunction()
    collection = client.create_collection("aggregated_embeddings", embedding_function=embedding_function)

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for i, (column_value, embedding) in enumerate(representative_embeddings.items()):
        metadata = metadata_by_column[column_value]
        documents.append(f"Aggregated document for {column_value}")
        embeddings.append(embedding.tolist())  # Convert numpy array to list
        metadatas.append(metadata)
        ids.append(f"doc_{i}")

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    # Create a new Chroma wrapper with the aggregated embeddings
    return Chroma(client=client, collection_name="aggregated_embeddings", embedding_function=embedding_function)

# You may want to add more helper functions specific to Chroma operations here