import json

def generate_report(result, output_file="report.json"):
    """Generates a JSON report of plagiarism results."""
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Report generated: {output_file}")
