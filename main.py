from compare import compare_codes

with open('code1.py', 'rb') as f1:
    code1 = f1.read().decode('utf-8', errors='ignore')

with open('code2.py', 'rb') as f2:
    code2 = f2.read().decode('utf-8', errors='ignore')

# Compare the two code files
result = compare_codes(code1, code2)

# Print the similarity results
print("🔎 Code Comparison Results:\n", result)
