// package reference_codes;

// public class java6 {
//     public static int binarySearch(int[] arr, int target) {
//         int low = 0, high = arr.length - 1;
//         while (low <= high) {
//             int mid = low + (high - low)/2;
//             if (arr[mid] == target) return mid;
//             else if (arr[mid] < target) low = mid + 1;
//             else high = mid - 1;
//         }
//         return -1;
//     }

//     public static void main(String[] args) {
//         int[] arr = {2, 3, 4, 10, 40};
//         System.out.println(binarySearch(arr, 10)); // Output: 3
//     }
// }

