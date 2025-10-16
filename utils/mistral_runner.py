#Mistral loop runner
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def run_mistral(prompt: str, model: str = "mistral") -> str:
    
    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False}
        )

        if res.status_code != 200:
            raise RuntimeError(f"Ollama API returned {res.status_code}: {res.text}")

        data = res.json()
        return data.get("response", "").strip()
    
    except Exception as e:
        print(f"Error running Mistral: {e}")
        return ""