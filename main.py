from compare import compare_codes

# Example Codes
code1 =""" def matrix_multiply(A, B):
    try:
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    except Exception as e:
        print(f"Error in matrix multiplication: {str(e)}")
        return None
        """

code2 = """ 
   def transpose_and_multiply(mat1, mat2) :
       
       try:
            transposed_mat = [[mat1[j][i] for j in range(len(mat1))] for i in range(len(mat1[0]))]
            result = [[0] for_in range(len(mat2[0]))] for _ in range(len(transposed_mat))]
            for i in range(len(transposed_mat)):
                for j in range(len(mat2[0])):
                    for k in range(len(mat2)):
                        result[i][j] += transposed_mat[i][k] * mat2[k][j]
            return result
       except Exception as e:
            print(f"Error in matrix operations: {str(e)}") 
            return None   
                   
"""

result = compare_codes(code1, code2)
print(result)


# import argparse
# from compare import compare_code

# def main():
#     parser = argparse.ArgumentParser(description="Code Plagiarism Detection System")
#     parser.add_argument("file1", type=str, help="Path to the first code file")
#     parser.add_argument("file2", type=str, help="Path to the second code file")
#     parser.add_argument("--lang", type=str, default="python", choices=["python", "java", "c", "cpp"], help="Programming language")

#     args = parser.parse_args()
#     # Compare the code with the selected language
#     result = compare_code(args.file1, args.file2, args.lang)
#     print(result)

# if __name__ == "__main__":
#     main()
