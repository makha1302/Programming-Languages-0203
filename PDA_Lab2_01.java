import java.util.Scanner;
import java.util.Stack;

public class PDA_Lab2_01 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter input string: ");
        String input = scanner.nextLine();

        if (validatePDA(input)) {
            System.out.println("Result: ACCEPTED");
        } else {
            System.out.println("Result: REJECTED");
        }

        scanner.close();
    }

    public static boolean validatePDA(String input) {
        // 1. Initial State: q0 และกำหนดสัญลักษณ์ก้น Stack เป็น 'Z'
        String state = "q0";
        Stack<Character> stack = new Stack<>();
        stack.push('Z');

        int i = 0;
        int len = input.length();

        // รัน Loop ตรวจสอบไปทีละตัวอักษรโดยใช้ charAt() ตามเงื่อนไขโจทย์
        while (i < len) {
            char ch = input.charAt(i);

            switch (state) {
                case "q0":
                    if (ch == 'a' && !stack.isEmpty() && stack.peek() == 'Z') {
                        stack.push('a'); // a, Z ; aZ (สัญลักษณ์ในรูปหมายถึงมี a อยู่บน Z)
                        state = "q1";
                        i++;
                    } else {
                        return false; // ตัวแรกไม่ใช่ 'a' ในขณะที่ยังมี input อยู่ (Reject)
                    }
                    break;

                case "q1":
                    if (ch == 'a' && !stack.isEmpty() && stack.peek() == 'a') {
                        stack.push('a'); // a, a ; aa
                        i++;
                    } else if (ch == 'b' && !stack.isEmpty() && stack.peek() == 'a') {
                        stack.pop(); // b, a ; lambda
                        state = "q2";
                        i++;
                    } else {
                        return false; // ขัดแย้งกับกฎใน q1
                    }
                    break;

                case "q2":
                    if (ch == 'b' && !stack.isEmpty() && stack.peek() == 'a') {
                        stack.pop(); // b, a ; lambda
                        i++;
                    } else {
                        return false; // เจอตัวอื่นที่ไม่ใช่ 'b' หรือ stack ผิดพลาด
                    }
                    break;

                default:
                    return false;
            }
        }

        // --- หลังจากอ่าน Input ครบทุกตัวแล้ว (Transition lambda) ---

        // ถ้าอยู่ที่ q0 และ stack มีแค่ 'Z' (กรณี String ว่าง "") -> ยอมรับ
        if (state.equals("q0") && stack.size() == 1 && stack.peek() == 'Z') {
            state = "q3"; // lambda, Z ; Z
            return true;
        }

        // ถ้าอยู่ที่ q2 และเคลียร์ 'a' จนเหลือแค่ 'Z' ตัวสุดท้าย -> เปลี่ยนไป q3
        // (ยอมรับ)
        if (state.equals("q2") && stack.size() == 1 && stack.peek() == 'Z') {
            state = "q3"; // lambda, Z ; Z
            return true;
        }

        return false;
    }
}