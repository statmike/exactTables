thread=[0,50]
l=50
print("thread loop report: thread {}, expects {}, looped over {}, {}".format(thread[0],thread[1], l, thread[1]==l and 'Passes' or 'Error'))
l=49
print("thread loop report: thread {}, expects {}, looped over {}, {}".format(thread[0],thread[1], l, thread[1]==l and 'Passes' or 'Error'))




i=2
a = list(range(0,10))
a
a2 = a[:i-1]
a2
import numpy as np
b = np.arange(0,10,dtype=int)
b
b2 = b[:i-1]
b2
np.all(a2==b2)






[8, 2220030, [24, 9], [70], 70, 6, 4.91]
[7, 2145441, [17, 10], [24, 8], 70, 6, 4.91]
[6, 2151907, [12, 28], [17, 9], 70, 6, 4.91]
[5, 2137520, [9, 8], [12, 27], 70, 6, 4.91]
[4, 2164240, [6, 11], [9, 7], 70, 6, 4.91]
[3, 2148377, [4, 1], [6, 10], 70, 6, 4.91]
[2, 2154089, [1, 32], [4, 0], 70, 6, 4.91]
[1, 2137786, [0], [1, 31], 70, 6, 4.91]


[9, 1998274, [25, 9], [70], 70, 6, 4.91]
[8, 1903793, [18, 17], [25, 8], 70, 6, 4.91]
[7, 1900500, [14, 5], [18, 16], 70, 6, 4.91]
[6, 1904196, [10, 25], [14, 4], 70, 6, 4.91]
[5, 1903361, [8, 1, 2], [10, 24], 70, 6, 4.91] ERROR
[4, 1899114, [5, 17], [8, 1, 1], 70, 6, 4.91] ERROR
[3, 1905681, [3, 14], [5, 16], 70, 6, 4.91]
[2, 1921666, [1, 19], [3, 13], 70, 6, 4.91]
[1, 1922805, [0], [1, 18], 70, 6, 4.91]


[10, 1764664, [26, 13], [70], 70, 6, 4.91]
[9, 1714097, [20], [26, 12], 70, 6, 4.91]
[8, 1722205, [15, 11], [19], 70, 6, 4.91]
[7, 1725162, [12, 3], [15, 10], 70, 6, 4.91]
[6, 1728770, [9, 8], [12, 2], 70, 6, 4.91]
[5, 1723470, [7, 1], [9, 7], 70, 6, 4.91]
[4, 1724646, [5], [7, 0], 70, 6, 4.91]
[3, 1729135, [3, 3, 1], [4], 70, 6, 4.91] ERROR
[2, 1710040, [1, 12], [3, 3, 0], 70, 6, 4.91] ERROR
[1, 1717201, [0], [1, 11], 70, 6, 4.91]

[11, 1607754, [27, 9], [70], 70, 6, 4.91]
[10, 1554756, [21], [27, 8], 70, 6, 4.91]
[9, 1568601, [16, 13], [20], 70, 6, 4.91]
[8, 1559091, [13, 6], [16, 12], 70, 6, 4.91]
[7, 1564610, [10, 14], [13, 5], 70, 6, 4.91]
[6, 1569751, [8, 6], [10, 13], 70, 6, 4.91]
[5, 1557410, [6, 6], [8, 5], 70, 6, 4.91]
[4, 1576167, [4, 11], [6, 5], 70, 6, 4.91]
[3, 1582399, [2, 27], [4, 10], 70, 6, 4.91]
[2, 1556835, [1, 8], [2, 26], 70, 6, 4.91]
[1, 1562016, [0], [1, 7], 70, 6, 4.91]


[12, 1494164, [28, 3], [70], 70, 6, 4.91]
[11, 1427881, [21, 18], [28, 2], 70, 6, 4.91]
[10, 1428246, [17, 11], [21, 17], 70, 6, 4.91]
[9, 1427472, [14, 6], [17, 10], 70, 6, 4.91]
[8, 1445664, [11, 15], [14, 5], 70, 6, 4.91]
[7, 1431471, [9, 8], [11, 14], 70, 6, 4.91]
[6, 1427020, [7, 9], [9, 7], 70, 6, 4.91]
[5, 1449420, [5, 16], [7, 8], 70, 6, 4.91]
[4, 1429741, [4, 1, 3], [5, 15], 70, 6, 4.91] ERROR
[3, 1425475, [2, 15], [4, 1, 2], 70, 6, 4.91] ERROR
[2, 1448165, [1, 5], [2, 14], 70, 6, 4.91]
[1, 1424671, [0], [1, 4], 70, 6, 4.91]





[8, 56, [3], [6], 6, 6, 4.91] PASS
[7, 58, [2, 0, 0, 3], [2, 4], 6, 6, 4.91] ERROR
[6, 58, [1, 1, 1, 3], [2, 0, 0, 2], 6, 6, 4.91]
[5, 58, [1, 0, 1, 0, 1], [1, 1, 1, 2], 6, 6, 4.91]
[4, 58, [0, 2, 4], [1, 0, 1, 0, 0], 6, 6, 4.91]
[3, 58, [0, 1, 1, 2, 2], [0, 2, 3], 6, 6, 4.91]
[2, 58, [0, 0, 2, 2], [0, 1, 1, 2, 1], 6, 6, 4.91]
[1, 58, [0], [0, 0, 2, 1], 6, 6, 4.91]

2003
[2 0 0 3 0 1]
[2 0 0 3 1 0]
2004
[2 0 0 4 0 0]
2010
[2 0 1 0 0 3]
[2 0 1 0 1 2]
[2 0 1 0 2 1]
[2 0 1 0 3 0]
2011
[2 0 1 1 0 2]
[2 0 1 1 1 1]
[2 0 1 1 2 0]
2012
[2 0 1 2 0 1]
[2 0 1 2 1 0]
2013
[2 0 1 3 0 0]
202
[2 0 2 0 0 2]
[2 0 2 0 1 1]
[2 0 2 0 2 0]
[2 0 2 1 0 1]
[2 0 2 1 1 0]
[2 0 2 2 0 0]
203
[2 0 3 0 0 1]
[2 0 3 0 1 0]
[2 0 3 1 0 0]
204
[2 0 4 0 0 0]
21
[2 1 0 3 0 0]
[2 1 1 0 0 2]
[2 1 1 0 1 1]
[2 1 1 0 2 0]
[2 1 1 1 0 1]
[2 1 1 1 1 0]
[2 1 1 2 0 0]
[2 1 2 0 0 1]
[2 1 2 0 1 0]
[2 1 2 1 0 0]
[2 1 3 0 0 0]
22
[2 2 1 0 0 1]
[2 2 1 0 1 0]
[2 2 1 1 0 0]
[2 2 2 0 0 0]
23
[2 3 1 0 0 0]

[2 4 0 0 0 0]

[2 3 0 0 0 0]
[2 3 0 0 0 0]
[2 2 0 0 0 0]
[2 2 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]
[2 0 0 0 0 0]