# codesearchnet_fetch.py
from datasets import load_dataset

def fetch_reference_codes(language: str, max_files: int = 10):
    """
    Fetches top `max_files` code snippets for `language` from CodeSearchNet
    and writes them to reference_codes/{language}_{i}.<ext>
    """
    ds = load_dataset(
        "code_search_net", 
        language, 
        split="train", 
        trust_remote_code=True
    )  # Hugging Face requires trust_remote_code for this dataset :contentReference[oaicite:1]{index=1}
    samples = ds.shuffle(seed=42).select(range(max_files))
    ext = "py" if language=="python" else "java"
    for i, ex in enumerate(samples["func_code_string"]):
        with open(f"reference_codes/{language}_{i}.{ext}", "w", encoding="utf-8") as f:
            f.write(ex)
