"""Practice employee policy question answering using section-attributed RAG."""

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
CHUNK_STEP = CHUNK_SIZE - CHUNK_OVERLAP
MIN_CHUNK_LENGTH = 60
N_RESULTS = 4


def load_and_chunk_document(document_path):
    """Extract sections and split their bodies into overlapping windows."""
    # TODO: implement this function.
    raise NotImplementedError("Implement load_and_chunk_document")


def retrieve_sections(question, embedding_model, collection):
    """Retrieve the four closest chunks and retain their section labels."""
    embedding = embedding_model.encode(question).tolist()
    result = collection.query(query_embeddings=[embedding], n_results=N_RESULTS)
    retrieved = [
        {
            "chunk": text,
            "section": metadata["section"],
            "similarity": round(1 - distance, 2),
        }
        for text, metadata, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]
    return sorted(retrieved, key=lambda item: item["similarity"], reverse=True)


def augment_prompt(question, retrieved_chunks):
    """Build a grounded prompt with numbered, section-labelled excerpts."""
    # TODO: implement this function.
    raise NotImplementedError("Implement augment_prompt")


def generate_answer(prompt, client):
    """Send the prompt through the supplied Gemini client."""
    # TODO: implement this function.
    raise NotImplementedError("Implement generate_answer")


def policy_qa_pipeline(question, document_path):
    """Index the handbook, retrieve context, and generate an attributed answer."""
    # TODO: implement this function.
    raise NotImplementedError("Implement policy_qa_pipeline")


if __name__ == "__main__":
    # TODO: read and strip the question; reject an empty entry.
    # TODO: call the pipeline and print the required fields.
    pass
