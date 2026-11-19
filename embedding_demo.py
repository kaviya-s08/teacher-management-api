
from sentence_transformers import SentenceTransformer

# Load the pretrained model
print("Loading embedding model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample sentences
sentences = [
    "Python is a programming language",
    "Java is used for software development",
    "I love learning artificial intelligence"
]

# Generate embeddings
embeddings = model.encode(sentences)

# Display results
for sentence, embedding in zip(sentences, embeddings):

    print("\nSentence:", sentence)

    print("Embedding:", embedding)

    print("Vector dimensions:", len(embedding))

print("\nEmbedding generation completed!")
