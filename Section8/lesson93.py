s = """\
AAA
BBB
CCC
DDD    
"""

with open("test.txt", "r") as f:
    #print(f.read())
    while True:
        #line = f.readline()
        #print(line, end="")
        chunk = 2
        line = f.read(chunk)
        print(line)
        if not line:
            break