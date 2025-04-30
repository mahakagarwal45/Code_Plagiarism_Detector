# main.py
import argparse
import os
# from fetchers.gemini_fetch import fetch_gemini_code
from fetchers.github_fetch import fetch_github_code
from fetchers.gfg_fetch import fetch_gfg_code
from fetchers.codeforces_fetch import fetch_cf_info
from fetchers.codesearchnet_fetch import fetch_reference_codes
from plagiarism_detector import detect_plagiarism
def ensure_dirs():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("reference_codes/python", exist_ok=True)
    os.makedirs("reference_codes/java", exist_ok=True)
    os.makedirs("reference_codes/cpp", exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Plagiarism Detection CLI")
    parser.add_argument("--gfg", help="mahakagarwsjn")
    parser.add_argument("--cf", help="mahakagarwal25")
    parser.add_argument("--lang", help="Programming language (python/java/cpp)", default="python")
    parser.add_argument("--user_file", help="Path to user code", default="uploads/user_code.py")
    # fetch_gemini_code(form.language.data or args.lang)
    args = parser.parse_args()
    ensure_dirs()

    print("\n📥 Fetching Reference Codes...\n")

    if args.gfg:
        fetch_gfg_code(args.gfg)

    if args.cf:
        fetch_cf_info(args.cf)

    fetch_reference_codes(args.lang)
    fetch_github_code()

    if not os.path.exists(args.user_file):
        print(f"❌ User file not found at {args.user_file}")
        return

    print(f"\n📄 Reading user code from: {args.user_file}")
    with open(args.user_file, "r") as f:
        user_code = f.read()

    test_cases = [
        {"input": [2], "expected_output": 4},
        {"input": [3], "expected_output": 9},
    ]

    reference_dir = os.path.join("reference_codes", args.lang)
    if not os.path.exists(reference_dir):
        print(f"❌ Reference directory not found: {reference_dir}")
        return

    high_similarity_files = []

    print("\n🔍 Starting Plagiarism Detection...\n")
    for filename in os.listdir(reference_dir):
        if filename.endswith(f".{args.lang}"):
            ref_path = os.path.join(reference_dir, filename)
            with open(ref_path, "r", encoding="utf-8") as f:
                reference_code = f.read()

            results = detect_plagiarism(user_code, reference_code, test_cases)

            print(f"\n📘 Compared with: {filename}")
            print("Similarity Scores:")
            for k, v in results.items():
                print(f"   {k}: {v}")

            if results.get("structural_similarity", 0) > 0.7:
                high_similarity_files.append((filename, results["structural_similarity"]))

    print("\n✅ Detection Complete.")
    print("\n🧠 Highly Similar Files (threshold > 0.7):")
    for file, score in high_similarity_files:
        print(f"   🔥 {file} -> Score: {score:.2f}")

if __name__ == "__main__":
    main()
