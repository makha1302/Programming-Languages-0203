import java.util.Scanner;
import java.util.Stack;

public class PDA_Lab2_02 {
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
        // เริ่มต้นที่สถานะ q1 และกำหนดสัญลักษณ์ก้น Stack เป็น '$'
        String state = "q1";
        Stack<Character> stack = new Stack<>();
        stack.push('$');

        int len = input.length();

        // วนลูปอ่านทีละตัวอักษรด้วย charAt() ตามเงื่อนไขโจทย์
        for (int i = 0; i < len; i++) {
            char ch = input.charAt(i);

            if (state.equals("q1")) {
                if (ch == 'a') {
                    if (!stack.isEmpty() && stack.peek() == '$') {
                        stack.push('0'); // a, $ -> 0$ (หมายถึง push '0' ลงไปอยู่บน '$')
                    } else if (!stack.isEmpty() && stack.peek() == '0') {
                        stack.push('0'); // a, 0 -> 00
                    } else if (!stack.isEmpty() && stack.peek() == '1') {
                        stack.pop(); // a, 1 -> lambda
                    } else {
                        return false;
                    }
                } else if (ch == 'b') {
                    if (!stack.isEmpty() && stack.peek() == '$') {
                        stack.push('1'); // b, $ -> 1$
                    } else if (!stack.isEmpty() && stack.peek() == '1') {
                        stack.push('1'); // b, 1 -> 11
                    } else if (!stack.isEmpty() && stack.peek() == '0') {
                        stack.pop(); // b, 0 -> lambda
                    } else {
                        return false;
                    }
                } else {
                    // ถ้ามีตัวอักษรอื่นที่ไม่ใช่ a หรือ b หลุดเข้ามา
                    return false;
                }
            }
        }

        // --- หลังจากอ่านข้อมูลครบทุกตัวแล้ว เช็กการเปลี่ยนสถานะด้วย lambda (\lambda, $
        // -> $) ---
        if (state.equals("q1") && stack.size() == 1 && stack.peek() == '$') {
            state = "q2";
            return true; // ย้ายไป q2 สำเร็จและยอมรับคำนี้
        }

        return false; // ถ้าใน Stack ยังเหลือ 0 หรือ 1 ค้างอยู่ หรือ Stack ว่างเปล่า จะ Reject
    }
}