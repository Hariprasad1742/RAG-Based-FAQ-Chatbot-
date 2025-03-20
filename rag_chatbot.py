import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load FAQ dataset
faq_df = pd.read_csv("faq_with_embeddings.csv")

# Load FAISS index
faiss_index = faiss.read_index("faq_index.faiss")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load local language model for text generation
generator = pipeline("text-generation", model="bigscience/bloom-560m")  # Free model


def retrieve_faq_answer(user_query):
    """Retrieve the most relevant FAQ answer using FAISS."""
    query_embedding = embedding_model.encode([user_query])
    _, index = faiss_index.search(np.array(query_embedding), 1)  # Get top 1 match
    
    best_match = faq_df.iloc[index[0][0]]
    return best_match["Question"], best_match["Answer"]

def generate_rag_response(user_query):
    """Retrieve FAQ answer and generate a response using a local model."""
    retrieved_question, retrieved_answer = retrieve_faq_answer(user_query)
    
    prompt = f"""You are a helpful assistant. A user asked: "{user_query}".
    The closest FAQ is: "{retrieved_question}".
    The FAQ answer is: "{retrieved_answer}".
    Provide a detailed response:"""

    response = generator(prompt, max_length=200, truncation=True, do_sample=True)

    return response[0]["generated_text"]

# Run chatbot
while True:
    user_query = input("You: ")
    if user_query.lower() in ["exit", "quit"]:
        break
    print("Chatbot:", generate_rag_response(user_query))
