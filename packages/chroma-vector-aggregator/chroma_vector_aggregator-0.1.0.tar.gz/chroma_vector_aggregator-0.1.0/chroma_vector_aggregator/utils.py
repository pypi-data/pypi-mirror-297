import numpy as np

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Normalize a vector to unit length.

    Parameters:
        vector (np.ndarray): Input vector.

    Returns:
        np.ndarray: Normalized vector.
    """
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two vectors.

    Parameters:
        vec1 (np.ndarray): First vector.
        vec2 (np.ndarray): Second vector.

    Returns:
        float: Cosine similarity between the two vectors.
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Add more utility functions as needed