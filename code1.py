# def add(a, b):
#     return a + b

# print(add(5, 3))

# Example Codes
def matrix_multiply(A, B):
    """Performs matrix multiplication with basic loops."""
    try:
        # ✅ Initialize result matrix with zeros
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

        # ✅ Matrix multiplication logic
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    except Exception as e:
        print(f"Error in matrix multiplication: {str(e)}")
        return None


# ✅ Simple Test Cases
if __name__ == "__main__":
    test_cases = [
        # Test Case 1: Basic 2x2 Matrix Multiplication
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        
        # Test Case 2: Identity Matrix Check
        ([[1, 0], [0, 1]], [[9, 8], [7, 6]], [[9, 8], [7, 6]]),

        # Test Case 3: Single Row and Single Column Matrix
        ([[5, 10, 15]], [[1], [2], [3]], [[70]]),

        # Test Case 4: 1x2 and 2x1 Matrix
        ([[3, 4]], [[5], [6]], [[39]]),

        # Test Case 6: 3x2 and 2x3 Matrix
        ([[1, 2], [3, 4], [5, 6]], [[7, 8, 9], [10, 11, 12]], [[27, 30, 33], [61, 68, 75], [95, 106, 117]]),
    ]

    for i, (A, B, expected) in enumerate(test_cases):
        result = matrix_multiply(A, B)
        if result == expected:
            print(f"✅ Test Case {i+1} Passed!")
        else:
            print(f"❌ Test Case {i+1} Failed! Expected: {expected}, Got: {result}")

