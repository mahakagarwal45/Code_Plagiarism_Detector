# def add(x, y):
#     return x + y

# print(add(5, 3))

def matrix_multiply(A, B):
    """Performs matrix multiplication of A and B."""
    try:
        # Initialize the result matrix with zeros
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        
        # Matrix multiplication logic
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    except Exception as e:
        print(f"Error in matrix multiplication: {str(e)}")
        return None


# ✅ Test Cases
def run_test_cases():
    """Runs test cases for matrix_multiply."""
    
    # Test Case 1: Basic 2x2 matrix multiplication
    A1 = [[1, 2], [3, 4]]
    B1 = [[5, 6], [7, 8]]
    expected1 = [[19, 22], [43, 50]]
    result1 = matrix_multiply(A1, B1)
    if result1 == expected1:
        print("✅ Test Case 1 Passed!")
    else:
        print(f"❌ Test Case 1 Failed! Expected: {expected1}, Got: {result1}")

    # Test Case 3: 3x2 and 2x3 matrix multiplication
    A3 = [[1, 4], [2, 5], [3, 6]]
    B3 = [[7, 8, 9], [10, 11, 12]]
    expected3 = [[47, 52, 57], [64, 71, 78], [81, 90, 99]]
    result3 = matrix_multiply(A3, B3)
    if result3 == expected3:
        print("✅ Test Case 2 Passed!")
    else:
        print(f"❌ Test Case 2 Failed! Expected: {expected3}, Got: {result3}")

    # Test Case 4: Multiplying by identity matrix
    A4 = [[5, 7], [2, 3]]
    I4 = [[1, 0], [0, 1]]
    expected4 = [[5, 7], [2, 3]]
    result4 = matrix_multiply(A4, I4)
    if result4 == expected4:
        print("✅ Test Case 3 Passed!")
    else:
        print(f"❌ Test Case 3 Failed! Expected: {expected4}, Got: {result4}")

    # Test Case 5: Matrix with zero elements
    A5 = [[0, 0], [0, 0]]
    B5 = [[1, 2], [3, 4]]
    expected5 = [[0, 0], [0, 0]]
    result5 = matrix_multiply(A5, B5)
    if result5 == expected5:
        print("✅ Test Case 4 Passed!")
    else:
        print(f"❌ Test Case 4 Failed! Expected: {expected5}, Got: {result5}")


# Run test cases
if __name__ == "__main__":
    run_test_cases()
