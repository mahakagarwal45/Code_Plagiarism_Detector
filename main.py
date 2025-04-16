from plagiarism_detector import detect_plagiarism

if __name__ == "__main__":
    user_code = "uploads/user_code.py"
    reference_codes_dir = "reference_codes/"

    # Optional test cases for behavioral similarity
    test_cases = [
        {"input": [2], "expected_output": 4},
        {"input": [3], "expected_output": 9},
    ]

    results = detect_plagiarism(user_code, reference_codes_dir, test_cases)

    for result in results:
        print(f"\n📄 Compared with: {result['Reference File']}")
        
        # Print the entire result to inspect its structure
        print("Result structure:", result)

        if 'Similarity Scores' in result:
            for key, value in result["Similarity Scores"].items():
                print(f"   {key}: {value}")
        else:
            print("No similarity scores found for this result.")
