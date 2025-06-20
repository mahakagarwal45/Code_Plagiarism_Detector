package reference_codes;
public class java8 {
    public static void main(String[] args) {
        int n = 5;
        System.out.println(factorial(n));
    }

    static int factorial(int n) {
        if (n == 0) return 1;
        return n * factorial(n-1);
    }
}