// package reference_codes;

// import java.util.Arrays;

// public class java5 {
//     public static int partition(int[] arr, int low, int high) {
//         int pivot = arr[high], i = low - 1;
//         for (int j = low; j < high; j++) {
//             if (arr[j] < pivot) {
//                 i++;
//                 int temp = arr[i];
//                 arr[i] = arr[j];
//                 arr[j] = temp;
//             }
//         }
//         int temp = arr[i+1];
//         arr[i+1] = arr[high];
//         arr[high] = temp;
//         return i+1;
//     }

//     public static void quickSort(int[] arr, int low, int high) {
//         if (low < high) {
//             int p = partition(arr, low, high);
//             quickSort(arr, low, p-1);
//             quickSort(arr, p+1, high);
//         }
//     }

//     public static void main(String[] args) {
//         int[] arr = {10, 7, 8, 9, 1, 5};
//         quickSort(arr, 0, arr.length-1);
//         System.out.println(Arrays.toString(arr));
//     }
// }

