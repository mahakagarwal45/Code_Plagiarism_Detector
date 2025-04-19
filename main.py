from plagiarism_detector import detect_plagiarism
from codesearchnet_fetch import fetch_reference_codes

if __name__ == "__main__":
    user_code_path = "uploads/user_code.py"
    with open(user_code_path, 'r') as f:
        user_code = f.read()

    test_cases = [
        {"input": [2], "expected_output": 4},
        {"input": [3], "expected_output": 9},
    ]

    references = fetch_reference_codes(language="python", max_files=5)

    for ref in references:
        reference_code = ref["code"]
        results = detect_plagiarism(user_code, reference_code, test_cases)

        print(f"\n📄 Compared with: {ref['repo']} → {ref['path']}")
        print("Similarity Scores:")
        for key, value in results.items():
            print(f"   {key}: {value}")
