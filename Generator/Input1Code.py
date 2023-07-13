# for I/O for local system
import sys
 
# For fast I/O
input = sys.stdin.buffer.readline
# input = sys.stdin.readline
print = sys.stdout.write
 
# importing libraries
from collections import defaultdict
from random import randint

# Solver function
def solve():
    d = defaultdict(lambda : 0)
    d[0] = "permit"
    d[1] = "deny"
    for i in range(500):
        print("Ip access-list role-based rule_" + str(i + 1) + "\n")
        value = randint(1, 20)
        # print(str(value) + "\n")
        for j in range(value):
            print(str(j + 1) + " ")
            val = randint(0, 1)
            print(str(d[val]) + " ")
            val2 = randint(0, 255)
            print(str(val2) + "\n")
 
# Main 
for _ in range(int(input())):
    solve()