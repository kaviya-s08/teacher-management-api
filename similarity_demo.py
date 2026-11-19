
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Three sentences
sentence1 = "I love programming in Python"

sentence2 = "Python is my favorite programming language"

sentence3 = "I enjoy playing cricket"

# Generate embeddings
embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

# Calculate cosine similarity
similarity1 = util.cos_sim(embedding1, embedding2)

similarity2 = util.cos_sim(embedding1, embedding3)

# Display results
print("Sentence 1:", sentence1)
print("Sentence 2:", sentence2)

print("\nSimilarity between sentence 1 and 2:")
print(round(similarity1.item(), 4))

print("\nSimilarity between sentence 1 and 3:")
print(round(similarity2.item(), 4))
