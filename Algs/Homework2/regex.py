import re
# string1 = """Lucas series up to depth 45: 
# Lucas number at position 0 is 2, time taken: 0.000002 seconds
# Lucas number at position 1 is 1, time taken: 0.000000 seconds
# Lucas number at position 2 is 3, time taken: 0.000000 seconds
# Lucas number at position 3 is 4, time taken: 0.000000 seconds
# Lucas number at position 4 is 7, time taken: 0.000000 seconds
# Lucas number at position 5 is 11, time taken: 0.000000 seconds
# Lucas number at position 6 is 18, time taken: 0.000000 seconds
# Lucas number at position 7 is 29, time taken: 0.000000 seconds
# Lucas number at position 8 is 47, time taken: 0.000000 seconds
# Lucas number at position 9 is 76, time taken: 0.000002 seconds
# Lucas number at position 10 is 123, time taken: 0.000001 seconds
# Lucas number at position 11 is 199, time taken: 0.000001 seconds
# Lucas number at position 12 is 322, time taken: 0.000001 seconds
# Lucas number at position 13 is 521, time taken: 0.000002 seconds
# Lucas number at position 14 is 843, time taken: 0.000003 seconds
# Lucas number at position 15 is 1364, time taken: 0.000004 seconds
# Lucas number at position 16 is 2207, time taken: 0.000008 seconds
# Lucas number at position 17 is 3571, time taken: 0.000010 seconds
# Lucas number at position 18 is 5778, time taken: 0.000019 seconds
# Lucas number at position 19 is 9349, time taken: 0.000032 seconds
# Lucas number at position 20 is 15127, time taken: 0.000043 seconds
# Lucas number at position 21 is 24476, time taken: 0.000068 seconds
# Lucas number at position 22 is 39603, time taken: 0.000149 seconds
# Lucas number at position 23 is 64079, time taken: 0.000177 seconds
# Lucas number at position 24 is 103682, time taken: 0.000287 seconds
# Lucas number at position 25 is 167761, time taken: 0.000465 seconds
# Lucas number at position 26 is 271443, time taken: 0.000767 seconds
# Lucas number at position 27 is 439204, time taken: 0.001244 seconds
# Lucas number at position 28 is 710647, time taken: 0.001987 seconds
# Lucas number at position 29 is 1149851, time taken: 0.003258 seconds
# Lucas number at position 30 is 1860498, time taken: 0.007231 seconds
# Lucas number at position 31 is 3010349, time taken: 0.009879 seconds
# Lucas number at position 32 is 4870847, time taken: 0.014927 seconds
# Lucas number at position 33 is 7881196, time taken: 0.024515 seconds
# Lucas number at position 34 is 12752043, time taken: 0.039778 seconds
# Lucas number at position 35 is 20633239, time taken: 0.060441 seconds
# Lucas number at position 36 is 33385282, time taken: 0.102192 seconds
# Lucas number at position 37 is 54018521, time taken: 0.151310 seconds
# Lucas number at position 38 is 87403803, time taken: 0.258354 seconds
# Lucas number at position 39 is 141422324, time taken: 0.412025 seconds
# Lucas number at position 40 is 228826127, time taken: 0.666511 seconds
# Lucas number at position 41 is 370248451, time taken: 1.066291 seconds
# Lucas number at position 42 is 599074578, time taken: 1.735587 seconds
# Lucas number at position 43 is 969323029, time taken: 2.909913 seconds
# Lucas number at position 44 is 1568397607, time taken: 4.718994 seconds"""

# string2 = """Lucas number at position 0 is 69, time taken: 0.000003 seconds
# Lucas number at position 1 is 420, time taken: 0.000002 seconds
# Lucas number at position 2 is 489, time taken: 0.000001 seconds
# Lucas number at position 3 is 909, time taken: 0.000001 seconds
# Lucas number at position 4 is 1398, time taken: 0.000000 seconds
# Lucas number at position 5 is 2307, time taken: 0.000000 seconds
# Lucas number at position 6 is 3705, time taken: 0.000002 seconds
# Lucas number at position 7 is 6012, time taken: 0.000000 seconds
# Lucas number at position 8 is 9717, time taken: 0.000000 seconds
# Lucas number at position 9 is 15729, time taken: 0.000001 seconds
# Lucas number at position 10 is 25446, time taken: 0.000001 seconds
# Lucas number at position 11 is 41175, time taken: 0.000002 seconds
# Lucas number at position 12 is 66621, time taken: 0.000002 seconds
# Lucas number at position 13 is 107796, time taken: 0.000003 seconds
# Lucas number at position 14 is 174417, time taken: 0.000005 seconds
# Lucas number at position 15 is 282213, time taken: 0.000007 seconds
# Lucas number at position 16 is 456630, time taken: 0.000008 seconds
# Lucas number at position 17 is 738843, time taken: 0.000010 seconds
# Lucas number at position 18 is 1195473, time taken: 0.000017 seconds
# Lucas number at position 19 is 1934316, time taken: 0.000035 seconds
# Lucas number at position 20 is 3129789, time taken: 0.000048 seconds
# Lucas number at position 21 is 5064105, time taken: 0.000076 seconds
# Lucas number at position 22 is 8193894, time taken: 0.000119 seconds
# Lucas number at position 23 is 13257999, time taken: 0.000182 seconds
# Lucas number at position 24 is 21451893, time taken: 0.000332 seconds
# Lucas number at position 25 is 34709892, time taken: 0.000476 seconds
# Lucas number at position 26 is 56161785, time taken: 0.000769 seconds
# Lucas number at position 27 is 90871677, time taken: 0.001220 seconds
# Lucas number at position 28 is 147033462, time taken: 0.001978 seconds
# Lucas number at position 29 is 237905139, time taken: 0.003198 seconds
# Lucas number at position 30 is 384938601, time taken: 0.005241 seconds
# Lucas number at position 31 is 622843740, time taken: 0.008560 seconds
# Lucas number at position 32 is 1007782341, time taken: 0.014718 seconds
# Lucas number at position 33 is 1630626081, time taken: 0.025488 seconds
# Lucas number at position 34 is 2638408422, time taken: 0.050623 seconds
# Lucas number at position 35 is 4269034503, time taken: 0.074373 seconds
# Lucas number at position 36 is 6907442925, time taken: 0.096659 seconds
# Lucas number at position 37 is 11176477428, time taken: 0.150583 seconds
# Lucas number at position 38 is 18083920353, time taken: 0.256248 seconds
# Lucas number at position 39 is 29260397781, time taken: 0.406556 seconds"""

# thelist = []


# thelist = re.findall(r"is ([0-9]+)", string2)

# thelist = [int(thelist[i]) for i in range(len(thelist))]

# sum = 0

# for i in range(len(thelist)-1):
#     sum += thelist[i+1]/thelist[i]
#     print(thelist[i+1]/thelist[i])

# sum /= (len(thelist))

# print(sum)

# print(sum([1, 14, 14, 4, 11, 7, 6, 9, 8, 10, 10, 5, 13, 2, 3, 15]))

string3 = """0       1
1       1
2       1
3       2
4       2
5       3
6       4
7       5
8       6
9       8
10      11
11      13
12      15
13      19
14      24
15      29
16      34
17      40
18      47
19      55
20      65
21      75
22      85
23      98
24      115
25      130
26      145
27      164
28      185
29      207
30      231
31      255
32      281
33      310
34      342
35      374
36      405
37      440
38      479
39      518
40      555
41      594
42      636
43      678
44      721
45      765
46      805
47      848
48      894
49      937
50      976
51      1016
52      1057
53      1096
54      1132
55      1166
56      1197
57      1227
58      1256
59      1282
60      1302
61      1318
62      1336
63      1350
64      1357
65      1361
66      1364
67      1361
68      1357
69      1350
70      1336
71      1318
72      1302
73      1282
74      1256
75      1227
76      1197
77      1166
78      1132
79      1096
80      1057
81      1016
82      976
83      937
84      894
85      848
86      805
87      765
88      721
89      678
90      636
91      594
92      555
93      518
94      479
95      440
96      405
97      374
98      342
99      310
100     281
101     255
102     231
103     207
104     185
105     164
106     145
107     130
108     115
109     98
110     85
111     75
112     65
113     55
114     47
115     40
116     34
117     29
118     24
119     19
120     15
121     13
122     11
123     8
124     6
125     5
126     4
127     3
128     2
129     2
130     1
131     1
132     1"""

thelist = re.findall(r" ([0-9]+)", string3)
thelist = [int(thelist[i]) for i in range(len(thelist))]

print(sum(thelist))