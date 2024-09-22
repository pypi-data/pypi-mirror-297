from .embedding_methods import calculate_embedding
from .chroma_helpers import get_embeddings_by_column, create_new_chroma_collection
from langchain_community.vectorstores import Chroma
import numpy as np

def aggregate_embeddings(chroma_collection: Chroma, column_name: str, method: str = "average", weights=None, trim_percentage: float = 0.1):
    """
    Aggregate embeddings in a Chroma collection based on a metadata column.

    Parameters:
        chroma_collection (Chroma): The Chroma collection to aggregate embeddings from.
        column_name (str): The metadata field by which to aggregate embeddings.
        method (str): The aggregation method to use.
        weights (list or np.ndarray, optional): Weights for weighted methods. Defaults to None.
        trim_percentage (float, optional): Fraction to trim from each end for trimmed mean. Defaults to 0.1.

    Returns:
        Chroma: A new Chroma collection with aggregated embeddings.
    """
    embeddings_by_column, metadata_by_column = get_embeddings_by_column(chroma_collection, column_name)
    
    representative_embeddings = {}
    for column_value, embeddings in embeddings_by_column.items():
        embeddings_array = np.array(embeddings)
        representative_embeddings[column_value] = calculate_embedding(embeddings_array, method, weights, trim_percentage)
    
    new_collection = create_new_chroma_collection(representative_embeddings, metadata_by_column)
    
    return new_collection

# You may want to add more utility functions here as needed