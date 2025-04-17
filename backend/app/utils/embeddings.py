from typing import List, Dict, Any, Optional
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Load model from HuggingFace
tokenizer = None
model = None

def _load_model():
    """
    Load the embedding model and tokenizer if not already loaded.
    """
    global tokenizer, model

    if tokenizer is None or model is None:
        try:
            # Use a smaller model for efficiency
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            # Fallback to random embeddings for testing
            tokenizer = "dummy"
            model = "dummy"

def _mean_pooling(model_output, attention_mask):
    """
    Mean pooling to get sentence embeddings.

    Args:
        model_output: Output from the transformer model
        attention_mask: Attention mask from tokenizer

    Returns:
        Pooled embeddings
    """
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for a text string.

    Args:
        text: The text to embed

    Returns:
        Embedding vector as a list of floats
    """
    _load_model()

    # If model loading failed, return random embeddings for testing
    if model == "dummy" or tokenizer == "dummy":
        return np.random.rand(768).astype(np.float32).tolist()

    try:
        # Tokenize and get model output
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Pool the embeddings
        embeddings = _mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize the embeddings
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

        # Convert to list and return
        return embeddings[0].numpy().tolist()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return random embeddings as fallback
        return np.random.rand(768).astype(np.float32).tolist()

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embedding vectors for a list of text strings.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    return [get_embedding(text) for text in texts]

def build_faiss_index(texts: List[str], metadata: List[Dict[str, Any]], index_path: Optional[str] = None):
    """
    Build a FAISS index from a list of texts and metadata.

    Args:
        texts: List of texts to index
        metadata: List of metadata dictionaries corresponding to each text
        index_path: Path to save the index (optional)
    """
    from app.faiss.faiss_index import FAISSIndex

    # Get embeddings for all texts
    embeddings = get_embeddings(texts)

    # Create and populate the index
    index = FAISSIndex()
    index.add_data(embeddings, metadata)

    # Save the index if a path is provided
    if index_path:
        index.save_index(index_path)

    return index