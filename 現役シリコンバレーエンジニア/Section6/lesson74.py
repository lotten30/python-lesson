from collections import defaultdict

s = "aksd;fawiohf;oawehg;aoinv"
d = defaultdict(int)

for c in s:
    d[c] += 1
print(d)

print(d["f"])