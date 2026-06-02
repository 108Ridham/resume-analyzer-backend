import os
import requests
import time

def get_embedding(text: str):
    # Use Hugging Face Inference API to keep memory under 512MB on Render.
    API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    
    # Optional HF_TOKEN from environment variables to avoid rate limits
    token = os.getenv("HF_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            # Check if model is loading on HF, if so, wait and retry once
            result = response.json()
            if isinstance(result, dict) and "estimated_time" in result:
                wait_time = min(result["estimated_time"], 5)
                time.sleep(wait_time)
                response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
                if response.status_code == 200:
                    return response.json()
            raise Exception(f"HF API returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"HF Inference API failed ({e}). Falling back to local SentenceTransformer...")
        try:
            from sentence_transformers import SentenceTransformer
            global _local_model
            if '_local_model' not in globals():
                _local_model = SentenceTransformer('all-MiniLM-L6-v2')
            # Convert numpy array output of SentenceTransformer to list
            return _local_model.encode(text).tolist()
        except ImportError:
            # If not installed (like on Render), propagate the original API error
            raise Exception(f"HF Inference API failed and local fallback is not installed: {e}")