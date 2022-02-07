package com.company;

import java.util.*;

public class Graded_assignment {
    static int z = 1;
    static int dep = 0;

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("int n");
        int n = in.nextInt();
        int a[][] = new int[n][n];

        while (n - dep * 2 > 0) {
            for (int i = dep /* <-- FIRST ONE IS THIS */; i < n - dep /* <-- BECAUSE YOURE ALREADY USING LESS THAN, YOU DONT NEED THE -1 */; i++) {
                a[dep][i] = z;
                z++;
            }
            for (int j = 1 + dep; j < n - dep /* <-- BECAUSE YOURE ALREADY USING LESS THAN, YOU DONT NEED THE -1 */; j++) {
                a[j][n - dep - 1] = z;
                z++;
            }
            for (int q = n - dep - 2; q >= dep /* <-- THIS NEEDS TO BE GREATER _OR EQUAL_ */; q--) {
                a[n - dep - 1][q] = z;
                z++;
            }
            for (int w = n - dep - 2; w > dep /* <-- BECAUSE YOURE ALREADY USING GREATER THAN, YOU DONT NEED THE +1*/ ; w--) {
                a[w][dep] = z;
                z++;
            }
            dep++;
        }
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[i].length; j++) {
                System.out.print(a[i][j]);
            }
            System.out.println();
        }
    }

}