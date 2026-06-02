import os
import requests
import time
import socket
import urllib3.util.connection

# Force urllib3 (used by requests) to use IPv4 only, avoiding buggy IPv6 DNS resolutions on Render
urllib3.util.connection.allowed_gai_family = lambda: socket.AF_INET

def get_embedding(text: str):
    # Use Hugging Face Inference API to keep memory under 512MB on Render.
    API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    
    # Optional HF_TOKEN from environment variables to avoid rate limits
    token = os.getenv("HF_TOKEN")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    last_exception = None
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                # Model might be loading on HF, check if estimated time is returned
                try:
                    result = response.json()
                    if isinstance(result, dict) and "estimated_time" in result:
                        wait_time = min(result["estimated_time"], 5)
                        time.sleep(wait_time)
                        continue
                except Exception:
                    pass
            
            # If not successful and not loading, raise exception to retry
            raise Exception(f"HF API returned status {response.status_code}: {response.text}")
            
        except Exception as e:
            last_exception = e
            # Wait with exponential backoff (e.g. 1s, 2s, 4s)
            time.sleep(2 ** attempt)
            
    # If all retries failed, fall back to local SentenceTransformer if possible
    print(f"HF Inference API failed after {retries} attempts ({last_exception}). Falling back to local SentenceTransformer...")
    try:
        from sentence_transformers import SentenceTransformer
        global _local_model
        if '_local_model' not in globals():
            _local_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Convert numpy array output of SentenceTransformer to list
        return _local_model.encode(text).tolist()
    except ImportError:
        # If not installed (like on Render), propagate the original API error
        raise Exception(f"HF Inference API failed and local fallback is not installed. Last Error: {last_exception}")