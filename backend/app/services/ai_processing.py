import json
import re
from collections import Counter
from typing import List

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# This model is small and good enough for local semantic search.
model = SentenceTransformer("all-MiniLM-L6-v2")


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
    "has", "have", "had", "not", "but", "you", "your", "its", "into", "about",
    "can", "will", "would", "there", "their", "they", "them", "then", "than",
    "also", "been", "because", "using", "use", "used", "our", "out", "all",
    "any", "each", "more", "most", "such", "may", "these", "those", "when",
    "where", "which", "what", "who", "how", "why", "a", "an", "in", "on",
    "of", "to", "is", "it", "as", "by", "or", "at", "be"
}


def generate_embedding(text: str) -> str:
    if not text or not text.strip():
        return json.dumps([])

    embedding = model.encode(text)
    return json.dumps(embedding.tolist())


def embedding_from_json(embedding_json: str) -> np.ndarray:
    values = json.loads(embedding_json)
    return np.array(values).reshape(1, -1)


def compute_similarity(query_embedding: np.ndarray, document_embedding: np.ndarray) -> float:
    return float(cosine_similarity(query_embedding, document_embedding)[0][0])


def generate_summary(text: str, max_sentences: int = 3) -> str:
    if not text or not text.strip():
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 20]

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    return " ".join(sentences[:max_sentences])


def generate_tags(text: str, max_tags: int = 5) -> str:
    if not text or not text.strip():
        return ""

    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    words = [word for word in words if word not in STOPWORDS]

    most_common = Counter(words).most_common(max_tags)
    tags = [word for word, _ in most_common]

    return ", ".join(tags)


def rank_documents_by_similarity(query: str, documents: List):
    query_embedding = model.encode(query)
    query_embedding = np.array(query_embedding).reshape(1, -1)

    ranked_results = []

    for document in documents:
        if not document.embedding:
            continue

        try:
            document_embedding = embedding_from_json(document.embedding)
            score = compute_similarity(query_embedding, document_embedding)
            ranked_results.append((document, score))
        except Exception:
            continue

    ranked_results.sort(key=lambda item: item[1], reverse=True)

    return ranked_results