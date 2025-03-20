from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

# Load FAQ dataset
faq_df = pd.read_csv("faq_dataset.csv")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert questions to embeddings
faq_questions = faq_df["Question"].tolist()
question_embeddings = embedding_model.encode(faq_questions)

# Store embeddings in FAISS
dimension = question_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(np.array(question_embeddings))


# Save FAISS index
faiss.write_index(faiss_index, "faq_index.faiss")
faq_df.to_csv("faq_with_embeddings.csv", index=False)

print("✅ FAQ Questions indexed in FAISS and saved!")
