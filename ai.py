import os
from dotenv import load_dotenv

from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

pipe = pipeline("text-generation", model="meta-llama/Llama-2-7b-hf")

load_dotenv()
login(os.getenv("HF_API_TOKEN"))

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")


def get_all_code_files(repo_path, extensions=[".py", ".js"]):
    code_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files

repo_path = "./src"  # поточний репозиторій
files = get_all_code_files(repo_path)
print("Знайдено файлів:", len(files))

def read_file_in_chunks(file_path, max_lines=50):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i in range(0, len(lines), max_lines):
        yield "".join(lines[i:i+max_lines])


def analyze_code(code: str):
    model_inputs = tokenizer(["Make review for this"], return_tensors="pt").to(model.device)
    return str(model_inputs)

def review_repo(repo_path="."):
    files = get_all_code_files(repo_path)
    full_review = {}
    for file in files:
        review_texts = []
        for chunk in read_file_in_chunks(file):
            review = analyze_code(chunk)
            review_texts.append(review)
        full_review[file] = "\n\n".join(review_texts)
    return full_review

if __name__ == "__main__":
    reviews = review_repo()
    for file, review in reviews.items():
        print(f"\n=== Ревʼю {file} ===\n")
        print(review)
