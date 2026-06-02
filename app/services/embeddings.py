from sentence_transformers import SentenceTransformer

# Load once at module level (after model is cached, this is instant)
model = None

def get_model():
    global model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded")
    return model

def get_embedding(text: str):
    m = get_model()
    embedding = m.encode(text)
    return embedding