from sentence_transformers import SentenceTransformer

print("Downloading model... please wait (only once)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model downloaded and cached successfully!")